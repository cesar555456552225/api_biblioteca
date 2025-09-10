from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Libro(models.Model):
    GENEROS = [
        ('Ficción','Ficción'),
        ('no_ficcion','No ficción'),
        ('fantasia','Fantasía'),
        ('ciencia','Ciencia'),
        ('historia','Historia'),
        ]
    
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='Libros')
    isbn = models.CharField(max_length=100, unique=True)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=100, choices=GENEROS)
    paginas = models.PositiveBigIntegerField()
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Prestamo (models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(auto_now_add=True)
    fecha_devolucion = models.DateField(null=True, blank=True)
    disponible = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.libro.titulo} - {self.usuario.username}"