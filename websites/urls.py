import account.urls
from django.conf.urls import include, url

import users.views
import websites.views
from dashboard.views import VideoIndexView, VideoDetailView
from websites.views import HomeView

urlpatterns = [
    # Root URL for client sites /
    url(r"^$", HomeView.as_view(), name="home"),

    # Authentication URLs, /signup and /login
    url(r"^signup/$", websites.views.WebsiteSignupView.as_view(), name="account_signup"),
    url(r"^login/$", users.views.LoginView.as_view(), name="account_login"),

    # /videos
    url(r'^videos/', include([
        # /videos/
        url(r'^$', VideoIndexView.as_view(), name='index'),

        # /videos/{video_id}
        url(r'^(?P<pk>[0-9]+)/$', VideoDetailView.as_view(), name="detail"),

    ], namespace='videos')),
]

urlpatterns += account.urls.urlpatterns
