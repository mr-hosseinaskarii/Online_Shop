from django.views import generic, View
from django.shortcuts import render


class AboutUsView(generic.TemplateView):
    template_name = 'public/about-us.html'


class ContactUsView(generic.TemplateView):
    template_name = 'public/contact-us.html'


class Error404View(View):
    def get(self, request, exception=None):
        return render(request, 'public/404.html', status=404)


class Error500View(View):
    def get(self, request, exception=None):
        return render(request, "public/500.html", status=500)


# Coming Soon
# class ComingSoonView(generic.TemplateView):
#     template_name = 'public/coming-soon.html'
#
