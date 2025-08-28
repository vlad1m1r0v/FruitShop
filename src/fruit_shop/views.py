from django.views.generic import TemplateView

class PageView(TemplateView):
    template_name = 'main.html'
