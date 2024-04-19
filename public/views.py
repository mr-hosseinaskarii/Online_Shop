from django.views import generic


class ComingSoonView(generic.TemplateView):
    template_name = 'coming-soon.html'
