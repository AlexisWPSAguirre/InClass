from src.config.db import DB
import requests

class shortLinkModel():
    def saveData(self, Data):
        cursor = DB.cursor()
        cursor.execute("INSERT INTO shortlinks(shortlink,link) VALUES (?,?)",(Data['shortlink'],Data['link'],))
        cursor.close()
    
    def findLink(self,shortLink):
        cursor = DB.cursor()
        cursor.execute("SELECT * FROM shortlinks WHERE shortlink = ?",(shortLink,))
        links = cursor.fetchone()
        cursor.close()
        return links


