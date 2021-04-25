from django.urls import path, include
from blog.views import post_list_view, post_detail_view, shareByEmail
urlpatterns = [
    path('', post_list_view, name='home'),
    path('<int:year>/<int:month>/<int:day>/<str:post>/', post_detail_view, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list_view, name='tag-similar'),
    path('<int:id>/share', shareByEmail, name='share')
    
]
