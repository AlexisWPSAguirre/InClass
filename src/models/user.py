from src.config.db import DB

class userModel():
    def RegistrarUsuario(self, datos):
        cursor = DB.cursor()
        cursor.execute("INSERT INTO users(name,email,password) VALUES (?,?,?)",(datos['nombre'],datos['correo'],datos['contrasena'],))
        cursor.close()
    
    def InicioSesion(self, datos):
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?",(datos['correo'],datos['contrasena'],))
        inicio = cursor.fetchone()
        cursor.close()
        return inicio

    def EliminarLink(self, link, session):
        cursor = DB.cursor()
        cursor.execute("DELETE FROM shortlinks WHERE user_id = ? AND shortened_link = ?",(session[0],link,))
        cursor.close()
        return link

    def EditarLink(self,datos):
        cursor = DB.cursor()
        cursor.execute("UPDATE shortlinks SET shortened_link = ?, original_link = ? WHERE id = ?",(datos['shortenedLink'], datos['linkOriginal'], datos['id'],))
        cursor.close()
        return datos

    def VerificarEmail(self,correo):
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?",(correo,))
        validar = cursor.fetchone()
        cursor.close()
        return validar

    
        

    
    
    