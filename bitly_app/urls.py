from django.conf import settings
from django.urls import path, re_path

from bitly_app.views import IndexView, ShortUrlRedirectView

urlpatterns = [
    path(r'', IndexView.as_view(), name='index'),
    re_path(r'^(?P<short_key>[\w\d]{{{}}})/?$'.format(settings.SHORT_KEY_LENGTH),
            ShortUrlRedirectView.as_view(), name='redirect')
]
