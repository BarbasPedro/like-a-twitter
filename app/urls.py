from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accounts.views import login_view, logout_view, register_view
from twitter.views import FeedView, NewPostCreateView, follow_user, like_post

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("register/", register_view, name="register"),
    path("feed/", FeedView.as_view(), name="feed"),
    path("new_post/", NewPostCreateView.as_view(), name="new_post"),
    path('feed/like/<int:post_id>/', like_post, name='like_post'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
