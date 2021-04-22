from flask import render_template, request, redirect, url_for, flash
from src import app
from string import ascii_letters, digits
from random import choice
import src.controllers.session as usuario
from src.models.acortador import shortLinkModel
import os

@app.context_processor  
def funcionHTML(): 
    def example(arreglo): 
        return len(arreglo)
    return dict(myexample=example)

@app.route('/', methods=['GET','POST'])
def inicio():
    RUTA = 'http://localhost:5000/'
    LINKMODEL = shortLinkModel()
    if request.method == 'GET':
        linksUsuario = LINKMODEL.linksUsuario(usuario.session)
        return render_template('inicio.html', linksUsuario = linksUsuario, session = usuario.session )
    flash('Link Generado Correctamente', 'success')
    linkOriginal = request.form.get('link')
    shortenedLink = ''.join([choice(ascii_letters + digits) for i in range(4)])
    if not 'usuario' in usuario.session:
        datos = {
        'linkOriginal': linkOriginal,
        'shortenedLink': shortenedLink,
        'user_id': None
        }
    else:
        datos = {
            'linkOriginal': linkOriginal,
            'shortenedLink': shortenedLink,
            'user_id': usuario.session['usuario'][0]
        }
    LINKMODEL.guardarLink(datos)
    linksUsuario = LINKMODEL.linksUsuario(usuario.session)
    shortenedLink = RUTA + shortenedLink    
    return render_template('inicio.html', shortenedLink = shortenedLink, session = usuario.session, linksUsuario = linksUsuario)

@app.route('/<link>')
def URL(link):
    LINKMODEL = shortLinkModel()
    links = LINKMODEL.buscarLink(link)
    if (links==None):
        return redirect(url_for('inicio'))
    return redirect(links[2])










