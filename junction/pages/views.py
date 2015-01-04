# -*- coding: utf-8 -*-

# Third Party Stuff
from django.views.generic import TemplateView
from conferences.models import Conference


class HomePageView(TemplateView):
    template_name = "pages/homepage.html"

    def get_conferences(self):
        qs = Conference.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        kwargs['conferences'] = self.get_conferences()
        return super(HomePageView, self).get_context_data(**kwargs)
