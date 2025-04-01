from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password
from django.utils.dateparse import parse_date
import qrcode
from io import BytesIO
from django.core.files import File

from .models import Usuario, Rol, PlanMembresia, Equipo, AccessLog, ClaseGrupal

def home(request):
    planes = PlanMembresia.objects.all()
    clases_grupales = ClaseGrupal.objects.all()
    
    context = {
        'planes': planes,
        'clases_grupales': clases_grupales
    }
    return render(request, 'home.html', context)

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

def generar_qr(usuario):
    data = f"http://127.0.0.1:8000/acceso/{usuario.id}-{usuario.correo}"
    qr_img = qrcode.make(data)
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    buffer.seek(0)
    file_name = f"qr_{usuario.id}.png"
    usuario.qr_code.save(file_name, File(buffer), save=True)

def reg_clientes(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        email = request.POST.get('email')
        password = request.POST.get('password')
        aceptar_condiciones = request.POST.get('terminos') is not None

        foto = request.FILES.get('foto', None)

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
            foto_perfil=foto,
            fecha_nacimiento=fecha_nacimiento,
            aceptar_condiciones=aceptar_condiciones,
            rol=Rol.objects.get(nombre='Clientes')
        )
        nuevo_usuario.save()
        generar_qr(nuevo_usuario)
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

        foto = request.FILES.get('foto', None)

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

        rol = get_object_or_404(Rol, id=rol_id)

        nuevo_usuario = Usuario(
            nombre=nombre,
            cedula=cedula,
            telefono=telefono,
            direccion=direccion,
            correo=email,
            contraseña=make_password(password),
            foto_perfil=foto,
            fecha_nacimiento=fecha_nacimiento,
            aceptar_condiciones=aceptar_condiciones,
            rol=rol,
        )
        nuevo_usuario.save()
        generar_qr(nuevo_usuario)
        
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
            elif usuario.rol.nombre == 'Entrenador':
                return redirect('dashboard_entrenador')
            else:
                return redirect('dashboard_cliente')
        else:
            messages.error(request, "Credenciales inválidas")
    
    return render(request, 'login_clientes.html')

def dashboard_admin(request):
    roles = Rol.objects.all()
    empleados = Usuario.objects.all()
    planes = PlanMembresia.objects.all()
    equipos = Equipo.objects.all()
    access_logs = AccessLog.objects.order_by('-fecha_ingreso')


    context = {
        'roles': roles,
        'empleados': empleados,
        'planes': planes,
        'equipos': equipos,
        'total_usuarios': empleados.count(),
        'total_roles': roles.count(),
        'total_membresias': planes.count(),
        'total_equipos': equipos.count(),
        'access_logs': access_logs,

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

def registrar_acceso(request, token):
    try:
        usuario_id, correo = token.split("-")
        usuario = get_object_or_404(Usuario, id=usuario_id, correo=correo)
    except Exception:
        messages.error(request, "Código QR inválido.")
        return redirect('login_clientes')
    
    AccessLog.objects.create(
        usuario=usuario,
        correo=usuario.correo,
        ip_address=request.META.get('REMOTE_ADDR')
    )
    
    messages.success(request, f"Bienvenido, {usuario.nombre}. Acceso registrado.")
    return redirect('acceso_usuario')

def dashboard_entrenador(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login_clientes')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect('login_clientes')
    
    clases = ClaseGrupal.objects.filter(instructor=usuario)
    
    context = {
        'usuario': usuario,
        'clases': clases,
    }
    return render(request, 'dash_entrenador.html', context)

def registrar_clase_grupal(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        descripcion = request.POST.get("descripcion")
        dia = request.POST.get("dia")    
        hora = request.POST.get("hora")         
        cupo_maximo = request.POST.get("cupo_maximo")
        
        try:
            cupo_maximo = int(cupo_maximo)
        except (TypeError, ValueError):
            messages.error(request, "El cupo máximo debe ser un número entero válido.")
            return redirect("registrar_clase_grupal")
        
        usuario_id = request.session.get('usuario_id')
        if not usuario_id:
            messages.error(request, "No se encontró sesión del usuario. Inicia sesión.")
            return redirect("login_clientes")
        
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            messages.error(request, "El usuario no existe.")
            return redirect("login_clientes")
        
        if usuario.rol.nombre != "Entrenador":
            messages.error(request, "No tienes permisos para registrar una clase grupal.")
            return redirect("dashboard_entrenador")
        
        imagen = request.FILES.get("imagen")
        
        ClaseGrupal.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            dia=dia,
            hora=hora,
            cupo_maximo=cupo_maximo,
            instructor=usuario,
            imagen=imagen
        )
        messages.success(request, "Clase grupal registrada exitosamente.")
        return redirect("dashboard_entrenador")     
    return render(request, "dash_entrenador.html")

def eliminar_clase_grupal(request, id):
    clase = get_object_or_404(ClaseGrupal, id=id)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "No se encontró sesión del usuario. Inicia sesión.")
        return redirect("login_clientes")
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect("login_clientes")
    
    if clase.instructor != usuario:
        messages.error(request, "No tienes permisos para eliminar esta clase.")
        return redirect("dashboard_entrenador")
    
    clase.delete()
    messages.success(request, "Clase grupal eliminada exitosamente.")
    return redirect("dashboard_entrenador")

def editar_clase_grupal(request, id):
    clase = get_object_or_404(ClaseGrupal, id=id)
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "No se encontró sesión del usuario. Inicia sesión.")
        return redirect("login_clientes")
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect("login_clientes")
    
    if clase.instructor != usuario:
        messages.error(request, "No tienes permisos para editar esta clase.")
        return redirect("dashboard_entrenador")
    
    if request.method == "POST":
        clase.nombre = request.POST.get("nombre")
        clase.descripcion = request.POST.get("descripcion")
        clase.dia = request.POST.get("dia")
        clase.hora = request.POST.get("hora")
        try:
            clase.cupo_maximo = int(request.POST.get("cupo_maximo"))
        except (TypeError, ValueError):
            messages.error(request, "El cupo máximo debe ser un número entero válido.")
            return redirect("dashboard_entrenador")
        
        clase.save()
        messages.success(request, "Clase grupal actualizada exitosamente.")
        return redirect("dashboard_entrenador")
    
    return render(request, "editar_clase.html", {"clase": clase})

def dashboard_cliente(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión.")
        return redirect('login_clientes')
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect('login_clientes')
    
    context = {'cliente': usuario}
    return render(request, 'dash_cliente.html', context)

def acceso_usuario(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        messages.error(request, "Debes iniciar sesión para ver esta página.")
        return redirect('login_clientes')
    
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        messages.error(request, "El usuario no existe.")
        return redirect('login_clientes')
    
    return render(request, 'acceso_usuario.html', {'usuario': usuario})

