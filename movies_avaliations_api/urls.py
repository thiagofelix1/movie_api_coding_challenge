from django.contrib import admin
from django.urls import path
from application import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movie', views.get_movie),
    path('signup', views.sign_up),
    path('signin', views.sign_in),
    path('score', views.create_score),
    path('comment', views.create_comment),
    path('comment-delete', views.delete_comment),
    path('comment-repeat',  views.mark_comment_repeat),
    path('replay-comment', views.create_replay_comment),
    path('like-comment', views.create_like),
    path('quote-comment', views.create_quote_comment),
    path('make-moderator', views.make_moderator),
    path('openapi', get_schema_view(
        title="Authorization Api",
        description="Authorization api for comment and score system Code challenge Itaú",
        version="1.0.0"
    ), name='openapi-schema'),
    path('documentation', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
