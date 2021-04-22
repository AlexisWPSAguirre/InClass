from src.config.db import DB
import requests

class shortLinkModel():
    def guardarLink(self, datos):
        cursor = DB.cursor()
        cursor.execute("INSERT INTO shortlinks(shortened_link,original_link,user_id) VALUES (?,?,?)",(datos['shortenedLink'],datos['linkOriginal'],datos['user_id'],))
        cursor.close()
    
    def buscarLink(self,shortened_link):
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM shortlinks WHERE shortened_link = ?",(shortened_link,))
        link = cursor.fetchone()
        cursor.close()
        return link

    def linksUsuario(self,usuario):
        links = []
        if 'usuario' in usuario:
            cursor = DB.cursor()
            cursor.execute("SELECT * FROM shortlinks WHERE user_id = ?",(usuario['usuario'][0],))
            links = cursor.fetchall()
            cursor.close()
        return links


