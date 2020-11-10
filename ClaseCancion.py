class cancion:
    def __init__(self, id, cancion, artista, album, fecha, imagen, spotify, youtube):
        self.id=id
        self.cancion=cancion
        self.artista=artista
        self.album=album
        self.fecha=fecha
        self.imagen=imagen
        self.spotify=spotify
        self.youtube=youtube

# ----------metodos get---------------
    def getId(self):
        return self.id

    def getCancion(self):
        return self.cancion

    def getArtista(self):
        return self.artista

    def getAlbum(self):
        return self.album

    def getFecha(self):
        return self.fecha

    def getImagen(self):
        return self.imagen

    def getSpotify(self):
        return self.spotify

    def getYoutube(self):
        return self.youtube
# --------------metodos set--------------
    def setId(self, id):
        self.id=id

    def setCancion(self, cancion):
        self.cancion=cancion

    def setArtista(self, artista):
        self.artista=artista

    def setAlbum(self, album):
        self.album=album

    def setFecha(self, fecha):
        self.fecha=fecha

    def setImagen(self, imagen):
        self.imagen=imagen

    def setSpotify(self, spotify):
        self.spotify=spotify

    def setYoutube(self, youtube):
        self.youtube=youtube