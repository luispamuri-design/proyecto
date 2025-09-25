from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Tipo
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required 

User = get_user_model()
# Create your views here.

def vista_login(request):
    return render(request, 'Login/index.html')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
            messages.error(request, 'El usuario no existe.')  
        if user:  # Si el usuario existe
            user_authenticated = authenticate(request,username=username, password=password)  
            if user_authenticated is not None:
                if user_authenticated.is_active:  
                    login(request, user_authenticated)  
                    return redirect('home')  
                else:
                    messages.error(request, 'Tu cuenta de usuario está inactiva.')  
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'Login/index.html') 

@login_required(login_url='custom_login')
def home(request):
    return render(request, 'home/index.html', {'usuario': request.user})

def custom_logout(request):
    logout(request) #Cierra la sesión del usuario
    response = redirect('custom_login') # Redirige a la página de login
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate' # Evita que el navegador almacene caché
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@login_required(login_url='custom_login')
def vista_usuario(request):
    roles=Tipo.objects.exclude(nombre__in=['root','cliente'])
    return render(request, 'usuario/index.html',{'usuario': request.user,'roles':roles})

@login_required(login_url='custom_login')
def crear_usuario(request):

    if request.method == 'POST':

        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        username = request.POST['username']
        password = request.POST['password']
        tipo_id = request.POST['rol']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "el nombre ya existe .")
            return redirect('vista_usuario')
        
        if not nombre or not apellido or not username or not password or not tipo_id :
            messages.error(request, "todos los campos son obligatorios .")
            return redirect('vista_usuario')
        
        try: 
            tipo = Tipo.objects.get(id=tipo_id)
        except Tipo.DoesNotExist:
            messages.error(request, "el rol seleccionado no es valido .")
            return redirect('vista_usuario')
        
        user = User.objects.create(
            first_name=nombre,
            last_name=apellido,
            username=username,
            password=make_password(password),
            tipo=tipo
        )
        messages.error(request, "usuario creado exxitosamene .")
        return redirect('vista_usuario')
    
    usuarios = User.objects.all()
    roles = Tipo.objects.all()
    usuarios_con_rol = [(usuario, usuario.tipo.nombre if usuario.tipo else 'sin rol') for usuario in usuarios]

    context = {

        'username':request.user.username,
        'role_name':request.user.tipo.nombre if request.user.tipo else 'sin rol', 
        'usuarios_con_rol': usuarios_con_rol,
        'roles':roles,   
        }
        
        
    #return render(request, 'usuario/index.html', {'usuario': request.user})
    return render(request, 'usuario/crear.html', context)
