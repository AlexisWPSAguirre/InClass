from flask import render_template, request, redirect, url_for, flash
from src import app
from src.models.user import userModel
from src.models.acortador import shortLinkModel
from src.config.correo import verificarEmail
import src.controllers.session as usuario
import hashlib
import os

SHORTLINKMODEL= shortLinkModel()
USERMODEL = userModel()
datosSesion = {}
@app.route('/Inicio/Sesion', methods=['GET','POST'])
def inicioSesion():
    if request.method == 'GET':
        return render_template('usuario/inicioSesion.html')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    crypt = hashlib.new('sha512', contrasena.encode('utf8'))
    datos = {
        'correo': correo,
        'contrasena': crypt.hexdigest()
    }
    inicio = USERMODEL.InicioSesion(datos)
    if(inicio==None):
        flash('Correo y contraseña no coinciden', 'error')
        return redirect(url_for('inicioSesion'))
    usuario.session['usuario'] = inicio
    return redirect(url_for('inicio'))

@app.route('/Registro/Usuario', methods=['GET','POST'])
def registrarUsuario():
    if request.method == 'GET':
        return render_template('usuario/registroUsuario.html')
    nombre = request.form.get('nombre')
    correo = request.form.get('correo')
    contrasena = request.form.get('contrasena')
    crypt = hashlib.new('sha512', contrasena.encode('utf8'))
    global datosSesion
    datosSesion = {
        'nombre': nombre,
        'correo': correo,
        'contrasena': crypt.hexdigest()
    }
    if(USERMODEL.VerificarEmail(datosSesion['correo'])==None):
        flash('Confirma tu registro en tu correo electronico', 'success')
        verificarEmail(correo,datosSesion)
        return redirect(url_for('inicioSesion'))
    flash('El correo se encuentra en uso', 'error')
    return redirect(url_for('registrarUsuario'))
    

@app.route('/Cerrar/Sesion')
def cerrarSesion():
    usuario.session.clear()
    return redirect(url_for('inicio'))

@app.route('/Eliminar/Link/<link>')
def eliminarLink(link):
    USERMODEL.EliminarLink(link,usuario.session['usuario'])
    return redirect(url_for('inicio'))

@app.route('/Editar/Link/<link>', methods=['GET','POST'])
def editarLink(link):
    linkFn = SHORTLINKMODEL.buscarLink(link)
    if request.method == 'GET':
        linksUsuario = SHORTLINKMODEL.linksUsuario(usuario.session)
        return render_template('inicio.html', linksUsuario = linksUsuario, session = usuario.session, link = linkFn )
    datos = {
        'id': linkFn[0],
        'shortenedLink': request.form.get('shortenedLink'),
        'linkOriginal': request.form.get('linkOriginal')
    }
    try:
        USERMODEL.EditarLink(datos)
    except:
        flash('El link acortado debe ser único','error')
        return redirect(url_for('editarLink', link = link))
    LinksUsuario = SHORTLINKMODEL.linksUsuario(usuario.session)
    return redirect(url_for('inicio'))

@app.route('/Verificar/Registro/<correo>', methods=['GET','POST'])
def verificarRegistro(correo):
    if(correo!='None'): 
        try:
            USERMODEL.RegistrarUsuario(datosSesion)
        except:
            flash('Ha ocurrido un error inesperado en el registro de correo', 'error')
            return redirect(url_for('registrarUsuario'))
        flash('Registro completado exitosamente', 'success')
        return redirect(url_for('inicioSesion'))   
    flash('Registro cancelado', 'error')
    return redirect(url_for('registrarUsuario'))
        



