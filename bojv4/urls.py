from django.conf.urls import include, url, patterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib import admin

from rest_framework import routers
from problem.views import ProblemViewSet, ProblemDataInfoViewSet, ScoreViewSet
from problem.views import FileViewSet
from submission.views import SubmissionViewSet
from contest.views import ContestViewSet
from ojuser.views import UserProfileViewSet, GroupProfileViewSet, GroupViewSet
from .views import HomepageView
from lib.views import QueryUser, SelfInfo, GetProblemList, GetProblem, GetAnnouncement, GetAnnouncementList,test

router = routers.DefaultRouter()
#  router.register(r'profiles', UserProfileViewSet)
router.register(r'users', UserProfileViewSet)
router.register(r'inline-groups', GroupViewSet)
router.register(r'groups', GroupProfileViewSet)
router.register(r'files', FileViewSet)
router.register(r'problems', ProblemViewSet)
router.register(r'cases', ScoreViewSet)
router.register(r'datainfo', ProblemDataInfoViewSet)
router.register(r'submissions', SubmissionViewSet)
router.register(r'contest', ContestViewSet)

urlpatterns = [
    url(r"^$", HomepageView.as_view(), name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^accounts/", include("ojuser.urls")),
    url(r"^problem/", include("problem.urls", namespace="problem")),
    url(r"^contest/", include("contest.urls", namespace="contest")),
    url(r"^submission/", include("submission.urls", namespace="submission")),
    url(r"^cheat/", include("cheat.urls", namespace="cheat")),
    url(r'^select2/', include('django_select2.urls')),
    url(r"^filer/", include("filer.urls")),
    url(r'^avatar/', include('avatar.urls')),
    url(r"^api/", include(router.urls)),
    url(r"^announcement/", include("announcement.urls", namespace="announcement")),
    url(r"^api-auth/", include('rest_framework.urls', namespace="rest_framework")),


    url(r"^rinne/QueryUser/", QueryUser),
    url(r"^rinne/SelfInfo/", SelfInfo),
    url(r"^rinne/GetProblemList/", GetProblemList),
    url(r"^rinne/GetProblemDetails/", GetProblem),
    url(r"^rinne/GetAnnouncementList/", GetAnnouncementList),
    url(r"^rinne/GetAnnouncementDetails/", GetAnnouncement),
    url(r"^rinne/test/", test),

    
    url(r'^', include('filer.server.urls')),
]
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
