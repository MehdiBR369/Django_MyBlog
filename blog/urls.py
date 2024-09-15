from django.urls import path
from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('post/new', views.PostNewView.as_view(), name='new-post'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name='update'),
    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name='delete'),
]