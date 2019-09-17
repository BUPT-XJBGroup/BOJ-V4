from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^$", views.AnnouncementListView.as_view(), name="list"),
    url(r"^add", views.AnnouncementAddView.as_view(), name="add"),
    url(r"^(?P<pk>[0-9]+)/$", views.AnnouncementView.as_view(), name="view"),
    url(r"^(?P<pk>[0-9]+)/update/$", views.AnnouncementUpdateView.as_view(), name="update"),
    url(r"^(?P<pk>[0-9]+)/delete/$", views.AnnouncementDeleteView.as_view(), name="delete"),
]