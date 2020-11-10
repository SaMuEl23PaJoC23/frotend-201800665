class admin:
    def __init__(self, nombre, apellido, usuario, password, confirmpass):
        self.nombre = nombre
        self.apellido = apellido  ##se creo un metodo constructor para la clase admin
        self.usuario = usuario
        self.password = password
        self.confirmpass = confirmpass
        # ----------metodos get---------------

    def getNombre(self):
        return self.nombre

    def getApellido(self):
        return self.apellido

    def getUsuario(self):
        return self.usuario

    def getPassword(self):
        return self.password

    def getConfirmPass(self):
        return self.confirmpass

        # --------------metodos set--------------

    def setNombre(self, nombre):
        self.nombre = nombre

    def setApellido(self, apellido):
        self.apellido = apellido

    def setUsuario(self, usuario):
        self.usuario= usuario

    def setPassword(self, password):
        self.password = password

    def setConfirmPass(self, confirmpass):
        self.confirmpass = confirmpass