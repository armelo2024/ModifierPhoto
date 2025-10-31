
from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path("studio/", views.studio, name="studio"),
    path("photos/", views.gallery, name="gallery"),
    path("photos/<uuid:pk>/", views.photo_detail, name="photo_detail"),
    path("photos/<uuid:pk>/delete/", views.photo_delete, name="photo_delete"),
    
]
