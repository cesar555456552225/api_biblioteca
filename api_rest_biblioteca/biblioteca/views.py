from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Autor, Libro, Prestamo
from.serializadores import AutorSerializer, LibroSerializer, PrestamoSerializer
from rest_framework.filters import OrderingFilter
# Create your views here.

class AutorViewsSet(viewsets.ModelViewSet):
    queryset = Autor.objects.all()
    serializer_class = AutorSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['nacionalidad']
    search_fields = ['nombre', 'apellido']
    ordering_fields = ['nombre', 'apellido']
    ordering=['apellido','nombre']

class LibroViewsSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    filter_backends  = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['genero', 'disponible']
    search_fields = ['titulo', 'autor__nombre', 'autor__apellido']
    ordering_fields = ['titulo', 'fecha_publicacion']
    ordering = ['-fecha_publicacion']

    @action(detail=True, methods=['get'])
    def disponibles(self, request):
        libros_disponibles = self.queryset.filter(disponible=True)
        serializer=self.get_serializer(libros_disponibles, many =True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def prestar(self, request, pk=None):
        libro = self.get_object()
        if not libro.disponible:
            return Response(
                {'error':'libro no disponible'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Prestamo=Prestamo.objects.create(
            libro=libro,
            usuario=request.user
        )
        libro.disponible=False
        libro.save()

        return Response({'mensaje':f'libro "{libro.titulo}" prestado con exito'})

class PrestamoViewSet (viewsets.ModelViewSet):
        serializer_class = PrestamoSerializer
        filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
        filterset_fields = ['disponible', 'usuario']
        ordering = ['-fecha_prestamo']

        def get_queryset(self):
            if self.request.user.is_staff:
                return Prestamo.objects.all()
            return Prestamo.objects.filter(usuario=self.request.user)
        
        @action(detail=True, methods=['post'])
        def devolver (self, request, pk=None):
            prestamo = self.get_object()
            if prestamo.devuelto:
                return Response(
                    {'error':'este libro ya fue devuelto'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            prestamo.devuelto = True
            prestamo.libro.disponible = True
            prestamo.libro.save()
            prestamo.save()

            return Response({'mensaje':f'Libro devuelto con exito'})