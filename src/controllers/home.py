from flask import render_template, request, redirect, url_for
from src import app
from string import ascii_letters, digits
from random import choice
from src.models.acortador import shortLinkModel



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    url = request.form.get('link')
    #''.join las comillas son el delimitador es decir caracter puesto despues de cada concatenación
    # choice elige un dijito o letra random 
    shortLink = ''.join([choice(ascii_letters + digits) for i in range(4)])
    Data = {
        'link': url,
        'shortlink': shortLink
    }
    linkModel = shortLinkModel()
    linkModel.saveData(Data)
    return render_template('index.html', shortLink = shortLink)

@app.route('/<link>')
def find(link):
    linkModel = shortLinkModel()
    links = linkModel.findLink(link)
    return redirect(links[2])






