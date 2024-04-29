from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.views import generic
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.accounts.models import Opt
from django.contrib import messages
from public.utils import send_otp_email, generate_code


class SignupView(generic.CreateView):
    model = get_user_model()
    template_name = 'accounts/authentication.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('shop:index'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the user already exists
        if self.model.objects.filter(email=email).exists():
            messages.warning(request, "An account with this email already exists")
            return redirect(reverse_lazy('accounts:signin'))

        self.model.objects.create(email=email, password=password)

        messages.add_message(request, messages.SUCCESS, "You have signed up successfully")
        return redirect(reverse_lazy("accounts:verify", kwargs={'email': email}))


class VerifyEmailView(generic.TemplateView):
    template_name = 'accounts/verify-opt.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('shop:index'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = kwargs.get('email')
        user = get_user_model().objects.get(email=email)
        opt = Opt.objects.filter(user=user).last()
        if opt:
            opt.code = generate_code()
            opt.save()
        else:
            opt = Opt.objects.create(
                user=user,
                code=generate_code(),
                expired_at=timezone.now() + timezone.timedelta(minutes=2)
            )
        send_otp_email(user.email, opt.code)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = kwargs.get('email')
        user = get_user_model().objects.get(email=email)
        user_opt = Opt.objects.filter(user=user).last()

        if user_opt.expired_at < timezone.now():
            messages.warning(request, "This code is expired")
            return redirect(reverse_lazy("accounts:verify", kwargs={'email': user.email}))

        if str(user_opt.code) == request.POST.get('opt'):
            # valid opt
            user.is_active = True
            user.is_verified = True
            user.save()
            login(request, user, backend='apps.accounts.backends.EmailBackend')
            messages.success(request, "Your account was activated successfully!")
            return redirect(reverse_lazy("shop:index"))
        else:
            # invalid opt
            messages.warning(request, "You have entered wrong code!")
            return redirect(reverse_lazy("accounts:verify", kwargs={'email': user.email}))


class SigninView(View):
    template_name = 'accounts/authentication.html'

    def __init__(self, *args, **kwargs):
        self.next = None
        super().__init__(*args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('shop:index'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = get_user_model().objects.get(email=email, password=password)
        # user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user, backend='apps.accounts.backends.EmailBackend')
                messages.success(request, "You are logged in successfully")
                return redirect(reverse_lazy("accounts:verify", kwargs={'email': email}))
            else:
                messages.warning(request, "This Email is not verified")
                return redirect(reverse_lazy("accounts:verify", kwargs={'email': email}))
        else:
            messages.warning(request, "Email or Password in incorrect")
        return render(request, self.template_name)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have logged out successfully")
        return redirect('shop:index')
