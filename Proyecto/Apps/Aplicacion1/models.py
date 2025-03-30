from django.db import models

class Rol(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField()
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    foto_perfil = models.ImageField(upload_to='fotos_perfil/', blank=True, null=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    aceptar_condiciones = models.BooleanField(default=False)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    usuario = models.OneToOneField('Usuario', on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)
    certificaciones = models.FileField(upload_to='certificaciones/', blank=True, null=True)

    def __str__(self):
        return f'{self.usuario.nombre} - {self.puesto}'

class PlanMembresia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_meses = models.IntegerField()
    imagen = models.ImageField(upload_to='planes_membresia/', null=True, blank=True)
    def __str__(self):
        return self.nombre

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ('DISP', 'Disponible'),
        ('MTTO', 'En mantenimiento'),
        ('FUERA', 'Fuera de servicio'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: Cardio, Pesas, Funcional, etc.")
    estado = models.CharField(max_length=5, choices=ESTADO_CHOICES, default='DISP')
    cantidad = models.PositiveIntegerField(default=1)
    fecha_ultima_revision = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.get_estado_display()})"