from django.conf.urls import patterns, include, url
from django.views.generic.base import TemplateView
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'junction.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', TemplateView.as_view(
        template_name='index.html',
    ), name='home'),
    url(r'^profile/$', TemplateView.as_view(
        template_name='profile.html',
    ), name='profile_home'),        
    url(r'^speakers/$', TemplateView.as_view(
        template_name='speakers.html',
    ), name='speakers-static'),
    url(r'^schedule/$', TemplateView.as_view(
        template_name='schedule.html',
    ), name='schedule-static'),
    url(r'^venue/$', TemplateView.as_view(
        template_name='venue.html',
    ), name='venue-static'),
    url(r'^sponsors/$', TemplateView.as_view(
        template_name='sponsors.html',
    ), name='sponsors-static'),
    url(r'^blog/$', TemplateView.as_view(
        template_name='blog-archive.html',
    ), name='blog-archive'),
    url(r'^coc/$', TemplateView.as_view(
        template_name='coc.html',
    ), name='coc-static'),
    url(r'^faq/$', TemplateView.as_view(
        template_name='faq.html',
    ), name='faq_static'),
)
