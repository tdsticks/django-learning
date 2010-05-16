from django.conf.urls.defaults import *

urlpatterns = patterns('project.polls.views',
    (r'^$', 'list'),
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)