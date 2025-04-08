from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date, timedelta

from django.core.exceptions import ValidationError

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
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

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
    

class AccessLog(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name="Usuario")
    correo = models.EmailField(verbose_name="Correo del Usuario")
    fecha_ingreso = models.DateField(auto_now_add=True, verbose_name="Fecha de Ingreso")
    hora_ingreso = models.TimeField(auto_now_add=True, verbose_name="Hora de Ingreso")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Dirección IP")

    def __str__(self):
        return f"Acceso de {self.usuario.nombre} el {self.fecha_ingreso} a las {self.hora_ingreso}"
    

class ClaseGrupal(models.Model):
    class DiaSemana(models.TextChoices):
        LUNES = 'LU', _('Lunes')
        MARTES = 'MA', _('Martes')
        MIERCOLES = 'MI', _('Miércoles')
        JUEVES = 'JU', _('Jueves')
        VIERNES = 'VI', _('Viernes')
        SABADO = 'SA', _('Sábado')
        DOMINGO = 'DO', _('Domingo')

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    dia = models.CharField(max_length=2, choices=DiaSemana.choices, help_text="Día en que se dicta la clase")
    hora = models.TimeField(help_text="Hora de inicio de la clase")
    cupo_maximo = models.PositiveIntegerField(help_text="Número máximo de asistentes")
    instructor = models.ForeignKey(
        'Usuario', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        help_text="Entrenador encargado de la clase"
    )
    imagen = models.ImageField(upload_to='clases_grupales/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_dia_display()} a las {self.hora}"

    def get_next_date(self):
        dias_semana = {
            'Lunes': 0,
            'Martes': 1,
            'Miércoles': 2,
            'Jueves': 3,
            'Viernes': 4,
            'Sábado': 5,
            'Domingo': 6,
        }
        today = date.today()
        target_weekday = dias_semana.get(self.get_dia_display(), None)
        if target_weekday is None:
            return None

        days_ahead = target_weekday - today.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        next_date = today + timedelta(days=days_ahead)
        return next_date
    
    @property
    def espacios_restantes(self):
        inscritos = self.inscripciones.count()
        return self.cupo_maximo - inscritos
  
    
class InscripcionClase(models.Model):
    clase = models.ForeignKey(ClaseGrupal, on_delete=models.CASCADE, related_name='inscripciones')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.clase.nombre} - {self.cliente.nombre}"

    def clean(self):
        inscripciones_actuales = self.clase.inscripciones.exclude(pk=self.pk).count()
        if inscripciones_actuales >= self.clase.cupo_maximo:
            raise ValidationError("La clase ha alcanzado su cupo máximo.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class SesionPersonalizada(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]
    cliente = models.ForeignKey('Usuario', on_delete=models.CASCADE, related_name='sesiones_personalizadas')
    entrenador = models.ForeignKey('Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='sesiones_entrenadas')
    fecha = models.DateField(help_text="Fecha de la sesión")
    hora = models.TimeField(help_text="Hora de inicio de la sesión")
    comentarios = models.TextField(blank=True, null=True, help_text="Comentarios adicionales")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sesión de {self.cliente.nombre} con {self.entrenador.nombre if self.entrenador else 'Sin asignar'} el {self.fecha} a las {self.hora}"

    def clean(self):
        if self.fecha < date.today():
            raise ValidationError("La fecha de la sesión no puede ser anterior al día de hoy.")