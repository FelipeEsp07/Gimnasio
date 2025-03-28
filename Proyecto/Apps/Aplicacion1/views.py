from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404


from .models import Usuario, Rol

def home(request):
    return render(request, 'home.html')

def inicio(request):
    return render(request, 'inicio.html')

def authenticate_user(correo, password):
    """Autenticación personalizada de usuario."""
    try:
        usuario = Usuario.objects.get(correo=correo)
        if check_password(password, usuario.contraseña):
            return usuario
        return None
    except Usuario.DoesNotExist:
        return None
    
def crear_rol(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        if not nombre:
            messages.error(request, "El nombre del rol es obligatorio.")
            return redirect('crear_rol')
        
        if Rol.objects.filter(nombre=nombre).exists():
            messages.error(request, "El rol ya existe.")
            return redirect('crear_rol')
        
        nuevo_rol = Rol(nombre=nombre)
        nuevo_rol.save()
        
        messages.success(request, "Rol creado exitosamente.")
        return redirect('dashboard_admin')
    
    return render(request, 'crear_rol.html')

def eliminar_rol(request, id):
    rol = get_object_or_404(Rol, id=id)
    rol.delete()
    messages.success(request, "Rol eliminado exitosamente.")
    return redirect('dashboard_admin')

def reg_clientes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        password = request.POST.get('password')
        aceptar_condiciones = request.POST.get('terminos') is not None

        foto_url = None
        if 'foto' in request.FILES:
            foto = request.FILES['foto']
            fs = FileSystemStorage()
            filename = fs.save(foto.name, foto)
            foto_url = fs.url(filename)

        errores = []

        if '@' not in email:
            errores.append("El correo electrónico debe contener un '@'.")
        if Usuario.objects.filter(correo=email).exists():
            errores.append("El correo ya está registrado. Por favor, elige otro.")

        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        fecha_nacimiento = parse_date(fecha_nacimiento_str) if fecha_nacimiento_str else None
        if fecha_nacimiento:
            fecha_actual = datetime.now().date()
            if fecha_nacimiento >= fecha_actual:
                errores.append("La fecha de nacimiento no puede ser la fecha actual ni una fecha futura.")

        if not aceptar_condiciones:
            errores.append("Debes aceptar los términos y condiciones.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return redirect('reg_clientes')

        nuevo_usuario = Usuario(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=email,
            contraseña=make_password(password),
            foto_perfil=foto_url,
            fecha_nacimiento=fecha_nacimiento,
            aceptar_condiciones=aceptar_condiciones,
            rol=Rol.objects.get(nombre='Clientes')
        )
        nuevo_usuario.save()

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('login_clientes')

    return render(request, 'reg_clientes.html')

def reg_empleados(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        password = request.POST.get('password')
        aceptar_condiciones = request.POST.get('terminos') is not None

        foto_url = None
        if 'foto' in request.FILES:
            foto = request.FILES['foto']
            fs = FileSystemStorage()
            filename = fs.save(foto.name, foto)
            foto_url = fs.url(filename)

        errores = []

        if '@' not in email:
            errores.append("El correo electrónico debe contener un '@'.")
        if Usuario.objects.filter(correo=email).exists():
            errores.append("El correo ya está registrado. Por favor, elige otro.")

        fecha_nacimiento_str = request.POST.get('fecha_nacimiento')
        fecha_nacimiento = parse_date(fecha_nacimiento_str) if fecha_nacimiento_str else None
        if fecha_nacimiento:
            fecha_actual = datetime.now().date()
            if fecha_nacimiento >= fecha_actual:
                errores.append("La fecha de nacimiento no puede ser la fecha actual ni una fecha futura.")

        if not aceptar_condiciones:
            errores.append("Debes aceptar los términos y condiciones.")

        rol_id = request.POST.get('rol')
        if not rol_id:
            errores.append("Seleccione un rol.")

        if errores:
            for error in errores:
                messages.error(request, error)
            return redirect('reg_empleados')

        rol = Rol.objects.get(id=rol_id)

        nuevo_usuario = Usuario(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=email,
            contraseña=make_password(password),
            foto_perfil=foto_url,
            fecha_nacimiento=fecha_nacimiento,
            aceptar_condiciones=aceptar_condiciones,
            rol=rol,
        )
        nuevo_usuario.save()

        messages.success(request, 'Usuario registrado exitosamente.')
        return redirect('dashboard_admin')

    roles = Rol.objects.all()
    return render(request, 'reg_empleados.html', {'roles': roles})

def login_clientes(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        usuario = authenticate_user(email, password)

        if usuario is not None:
            request.session['usuario_id'] = usuario.id
            request.session['cedula_cliente'] = usuario.cedula  

            if usuario.rol.nombre == 'Administrador':
                return redirect('dashboard_admin') 
            else:
                return redirect('inicio')
        else:
            messages.error(request, "Credenciales inválidas")
    
    return render(request, 'login_clientes.html')

def dashboard_admin(request):
    roles = Rol.objects.all()
    empleados = Usuario.objects.all() 
    return render(request, 'dash_admin.html', {'roles': roles, 'empleados': empleados})

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Usuario, id=id)
    empleado.delete()
    messages.success(request, "Empleado eliminado exitosamente.")
    return redirect('dashboard_admin')


