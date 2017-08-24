from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', views.RecordListView.as_view(), name='record-list'),
    url(r'^(?P<cpk>[0-9]+)/(?P<pk>[0-9]+)$', views.RecordDetailView.as_view(), name='record-detail'),
 ]
