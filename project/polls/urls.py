from django.conf.urls.defaults import *

urlpatterns = patterns('project.polls.views',
    (r'^$', 'list'),
    (r'^json', 'json_dump'),
    (r'^xml', 'xml_dump'),
    (r'^(?P<poll_id>\d+)/$', 'detail'),
    (r'^(?P<poll_id>\d+)/results/$', 'results'),
    (r'^(?P<poll_id>\d+)/vote/$', 'vote'),
)