# -*- coding: utf-8 -*-

from django.views.generic import TemplateView

from junction.conferences.models import Conference


class HomePageView(TemplateView):
    template_name = "pages/home_page.html"

    def get_context_data(self, **kwargs):
        kwargs['conferences'] = Conference.objects.filter(deleted=False)
        return super(HomePageView, self).get_context_data(**kwargs)
