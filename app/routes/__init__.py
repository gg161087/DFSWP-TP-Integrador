from flask import render_template,request, redirect, url_for, session
from app.auth import login_required
from app import app
from app.handlers import *

@app.route('/')

def relogin():    
    return redirect(url_for('login'))


@app.route('/index')
@login_required
def index():    
    user = session['usuario']
    if request.args.get('eliminar'):        
        delet_person(int(request.args.get('eliminar')))
        people = get_people()          
        return redirect(url_for('index'))
    return render_template('index.html', titulo='Inicio', user=user, h2=f'Bienvenido al Registro de Personas, {user}', people=get_people())


@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method=='POST':
        if request.form['contraseña'] == request.form['repeat_contraseña']:
            pwd = hashear_password(request.form['contraseña'])
            data = {
                "name": request.form['nombre_completo'],
                "user": request.form['usuario'],
                "pwd": pwd,                  
            }
            users = get_users()
            for user in users:
                if data['user'] == user['user']:
                    return render_template('registrarse.html', title='Registrarse', message='Nombre de usuario no disponible')
                register_user(data)
                return render_template('registrarse.html', title='Registrarse', message='Usuario Registrado exitosamente')
            return redirect(url_for('index'))
        return render_template('registrarse.html', title='Registrarse', message='Las Contraseñas no coinciden')
    else:           
        return render_template('registrarse.html', titulo='Registrarse')


@app.route('/registrar_persona', methods=['GET', 'POST'])
@login_required
def registrar_persona():
    if request.method=='POST':
        data = {
            "fecha": request.form['fecha'],
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],  
            "dni": request.form['dni'],
            "motivo":request.form['motivo']
        }     
        register_person(data)
        return render_template('registrar_persona.html', title='Registrar Persona', h2='Registrar persona', message='Persona agregada exitosamente')                        
    return render_template('registrar_persona.html', title='Registrar Persona', h2='Registrar persona')

@app.route('/editar_persona/<int:person_id>', methods=['GET', 'POST'])
@login_required
def editar_persona(person_id):          
    if request.method=='POST':                     
        data = {
            "fecha": request.form['fecha'],
            "nombre": request.form['nombre'],
            "apellido": request.form['apellido'],  
            "dni": request.form['dni'] ,
            "motivo":request.form['motivo'],            
            "id": person_id
        }              
        delet_person(person_id)           
        register_person(data)                            
        return redirect(url_for('index'))
    person = get_person(person_id)       
    return render_template('editar_persona.html', title='Persona', person=person)


@app.route('/login', methods=['GET', 'POST'])
def login():       
    if request.method=='POST':        
        user = request.form['usuario']
        pwd = request.form['contraseña']
        
        if validate_user(user, pwd):
            session['usuario'] = user                     
            return redirect(url_for('index'))                                
        return render_template('login.html', title="Acceso", message='Usuario o contraseña incorrecto!') 

    else:
        return render_template('login.html', title="Acceso")    

@app.route('/logout')
@login_required
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))