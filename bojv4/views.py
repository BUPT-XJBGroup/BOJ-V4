from django.views.generic import TemplateView
from announcement.models import Announcement


class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super(HomepageView, self).get_context_data(**kwargs)
        context['announcements'] = Announcement.objects.order_by('-is_sticky', '-update_time').all()[:6]
        return context