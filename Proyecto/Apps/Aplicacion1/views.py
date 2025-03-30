from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password, check_password
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404


from .models import Usuario, Rol, PlanMembresia, Equipo

def home(request):
    planes = PlanMembresia.objects.all()
    return render(request, 'home.html', {'planes': planes})

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
    planes = PlanMembresia.objects.all()
    equipos = Equipo.objects.all()

    context = {
        'roles': roles,
        'empleados': empleados,
        'planes': planes,
        'equipos': equipos,
        'total_usuarios': empleados.count(),
        'total_roles': roles.count(),
        'total_membresias': planes.count(),
        'total_equipos': equipos.count(),
    }
    return render(request, 'dash_admin.html', context)

def eliminar_empleado(request, id):
    empleado = get_object_or_404(Usuario, id=id)
    empleado.delete()
    messages.success(request, "Empleado eliminado exitosamente.")
    return redirect('dashboard_admin')

def editar_empleado(request, id):
    empleado = get_object_or_404(Usuario, id=id)
    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.cedula = request.POST.get('cedula')
        empleado.telefono = request.POST.get('telefono')
        empleado.direccion = request.POST.get('direccion')
        empleado.correo = request.POST.get('email')
        rol_id = request.POST.get('rol')
        if rol_id:
            empleado.rol = get_object_or_404(Rol, id=rol_id)
        empleado.save()
        messages.success(request, "Empleado actualizado exitosamente.")
        return redirect('dashboard_admin')
    return render(request, 'editar_empleado.html', {'empleado': empleado})

def registrar_plan_membresia(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        duracion_meses = request.POST.get('duracion_meses')
        imagen = request.FILES.get('imagen', None)

        
        if not nombre or not descripcion or not precio or not duracion_meses:
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('registrar_plan_membresia')
        
        if PlanMembresia.objects.filter(nombre=nombre).exists():
            messages.error(request, "El plan ya existe.")
            return redirect('registrar_plan_membresia')
        
        try:
            precio = float(precio)
            duracion_meses = int(duracion_meses)
        except ValueError:
            messages.error(request, "Precio o duración inválidos.")
            return redirect('registrar_plan_membresia')
        
        nuevo_plan = PlanMembresia(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            duracion_meses=duracion_meses,
            imagen=imagen
        )
        nuevo_plan.save()
        messages.success(request, "Plan de membresía registrado exitosamente.")
        return redirect('dashboard_admin')
    
    planes = PlanMembresia.objects.all()
    return render(request, 'registrar_plan_membresia.html', {'planes': planes})

def editar_plan(request, id):
    plan = get_object_or_404(PlanMembresia, id=id)
    if request.method == 'POST':
        plan.nombre = request.POST.get('nombre')
        plan.descripcion = request.POST.get('descripcion')
        plan.precio = request.POST.get('precio')
        plan.duracion_meses = request.POST.get('duracion_meses')
        plan.save()
        messages.success(request, "Plan actualizado exitosamente.")
        return redirect('dashboard_admin')
    return render(request, 'editar_plan.html', {'plan': plan})

def eliminar_plan(request, id):
    plan = get_object_or_404(PlanMembresia, id=id)
    plan.delete()
    messages.success(request, "Plan eliminado exitosamente.")
    return redirect('dashboard_admin')

def registrar_equipo(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        tipo = request.POST.get('tipo')
        estado = request.POST.get('estado')
        cantidad = request.POST.get('cantidad')
        fecha_ultima_revision = request.POST.get('fecha_ultima_revision') or None

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            messages.error(request, "La cantidad debe ser un número entero.")
            return redirect('registrar_equipo')

        nuevo_equipo = Equipo(
            nombre=nombre,
            descripcion=descripcion,
            tipo=tipo,
            estado=estado,
            cantidad=cantidad,
            fecha_ultima_revision=fecha_ultima_revision
        )
        nuevo_equipo.save()
        messages.success(request, "Equipo registrado exitosamente.")
        return redirect('dashboard_admin')

    equipos = Equipo.objects.all()
    return render(request, 'registrar_equipo.html', {'equipos': equipos})

def eliminar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    equipo.delete()
    messages.success(request, "Equipo eliminado exitosamente.")
    return redirect('dashboard_admin')

def editar_equipo(request, id):
    equipo = get_object_or_404(Equipo, id=id)
    if request.method == 'POST':
        estado = request.POST.get('estado')
        cantidad = request.POST.get('cantidad')
        fecha_ultima_revision = request.POST.get('fecha_ultima_revision') or None
        
        try:
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            messages.error(request, "La cantidad debe ser un número entero.")
            return redirect('dashboard_admin')  
        
        equipo.estado = estado
        equipo.cantidad = cantidad
        equipo.fecha_ultima_revision = fecha_ultima_revision
        equipo.save()
        
        messages.success(request, "Equipo actualizado exitosamente.")
        return redirect('dashboard_admin')
    
    return render(request, 'editar_equipo.html', {'equipo': equipo})