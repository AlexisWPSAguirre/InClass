from flask import Flask, render_template
from flask_mail import Mail, Message
import os
from src import app
import src.controllers.session as usuario

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'arusmort@gmail.com',
    "MAIL_PASSWORD": os.environ['PASSWORD_EMAIL']
}

app.config.update(mail_settings)
mail = Mail(app) 

def verificarEmail(correo, datosSesion):
    with app.app_context():
        msg = Message(subject="Confirm Registration to URL Shortener", 
        sender=app.config.get("MAIL_USERNAME"),
        recipients=[correo])
        msg.html = render_template('usuario/correo.html', session = datosSesion)
        mail.send(msg)
    

    