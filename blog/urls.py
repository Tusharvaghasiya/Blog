from django.urls import path, include
from blog.views import post_list_view, post_detail_view, shareByEmail, about, signup, createPost
urlpatterns = [
    path('', post_list_view, name='home'),
    path('<int:year>/<int:month>/<int:day>/<str:post>/', post_detail_view, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list_view, name='tag-similar'),
    path('<int:id>/share', shareByEmail, name='share'),
    path('about/', about, name='about'), 
    path('signup/', signup, name='signup'), 
    path('create/', createPost, name='create'),
    path('verification/', include('verify_email.urls')),
]
