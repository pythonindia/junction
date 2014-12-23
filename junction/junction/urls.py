from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

urlpatterns = patterns(
    '',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^(?P<conference_slug>[\w-]+)/proposals/', include('proposals.urls')),

    url(r'^accounts/', include('allauth.urls')),
    url('^markdown/', include('django_markdown.urls')),

    # Static Pages
    url(r'^speakers/$', TemplateView.as_view(template_name='static-content/speakers.html',), name='speakers-static'),
    url(r'^schedule/$', TemplateView.as_view(template_name='static-content/schedule.html',), name='schedule-static'),
    url(r'^venue/$', TemplateView.as_view(template_name='static-content/venue.html',), name='venue-static'),
    url(r'^sponsors/$', TemplateView.as_view(template_name='static-content/sponsors.html',), name='sponsors-static'),
    url(r'^blog/$', TemplateView.as_view(template_name='static-content/blog-archive.html',), name='blog-archive'),
    url(r'^coc/$', TemplateView.as_view(template_name='static-content/coc.html',), name='coc-static'),
    url(r'^faq/$', TemplateView.as_view(template_name='static-content/faq.html',), name='faq_static'),
    url(r'^$', TemplateView.as_view(template_name='static-content/index.html',), name='home'),

)
