from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'autores', views.AutorViewsSet, basename='autor')
router.register(r'libros', views.LibroViewsSet, basename='libro')
router.register(r'prestamos', views.PrestamoViewSet, basename='prestamo')

urlpatterns = [
    path('api/', include(router.urls)),
]
