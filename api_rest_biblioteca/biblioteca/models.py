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
    GENEROS ={
        ('Ficción','Ficción'),
        ('no_ficcion','No ficción'),
        ('fantasia','Fantasía'),
        ('ciencia','Ciencia'),
        ('historia','Historia'),
        }
    
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, RELATED_NBAME='Libros')
    isbn = models.CharField(max_length=100, unique=True)
    fecha_publicacion = models.DateField()
    genero = models.CharField(max_length=100, choices=GENEROS)
    paginas = models.PositiveBigIntegerField()
    dosponible = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo

class Prestamo (models.Model):
    
