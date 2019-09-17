from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r"^groups/$", views.GroupListView.as_view(), name="mygroup-list"),
    url(r"^groups/add$", views.GroupCreateView.as_view(), name="mygroup-create"),
    url(r'^groups/(?P<pk>[0-9]+)/$', views.GroupDetailView.as_view(), name='mygroup-detail'),
    url(r'^groups/(?P<pk>[0-9]+)/update/$', views.GroupUpdateView.as_view(),
        name='mygroup-update'),
    url(r'^groups/(?P<pk>[0-9]+)/delete/$', views.GroupDeleteView.as_view(),
        name='mygroup-delete'),
    url(r'^groups/(?P<pk>[0-9]+)/members/$', views.GroupMemberView.as_view(),
        name='mygroup-add-member'),
    url(r'^groups/(?P<pk>[0-9]+)/reset/$', views.GroupResetView.as_view(),
        name='mygroup-reset-password'),
    url(r'^groups/(?P<group>[0-9]+)/(?P<pk>[0-9]+)/$', views.UserDeleteView.as_view(), name='group-user-delete'),
    url(r'^myusers/add/$', views.UserAddView.as_view(), name='user-add'),
    url(r'^myusers/query/$', views.UserQueryView.as_view(), name='user-query'),
    url(r"^signup/$", views.OjUserSignupView.as_view(), name="account_signup"),
    url(r"^profiles/$", views.OjUserProfilesView.as_view(), name="account-profile"),
    url(r"^", include("account.urls")),
]

