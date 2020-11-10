from flask import Flask, jsonify, request    #jsonify, transforma un arreglo a un formato Json
from flask_cors import CORS
from ClaseUsuario import usuario
from ClaseAdmin import admin
from ClaseCancion import cancion
from ClasePlaylist import playlist

app =Flask(__name__)
CORS(app)   ##sirve para el frontend

ArregloAdmins=[] #Se crea un arreglo para los administradores
ArregloUsuarios=[] #Se crea un arreglo para los usuarios
ArregloCanciones=[]    #Se crea un arreglo para las canciones
ArregloPlaylist=[]
cont_canciones=0    #ya que las canciones pueden contener el mismo nombre, se diferenciaran con un id unico, el cual
                    #sera dado por un contador

ArregloAdmins.append(admin('usuario','maestro','admin','admin','admin'))
ArregloUsuarios.append(usuario('samuel','pajoc','sam','123','123'))
ArregloUsuarios.append(usuario('alejandro','raymundo','ale','1234','1234'))
ArregloUsuarios.append(usuario('anna','gomez','annita','12345','12345'))            #Se creo 3 usuarios nuevos dentro del arreglo "Usuarios"

@app.route('/Personas', methods=['GET'])    #Consultar todos los datos de los usuarios
def ObtenerPersonas():
    Datos = []      #Es necesario meterlo en un arreglo, para que luego se puedan mostrar todos los datos
    global ArregloUsuarios
    for usu in ArregloUsuarios:
        Dato={
            'nombre':usu.getNombre(),
            'apellido':usu.getApellido(),
            'usuario':usu.getUsuario(),
            'password':usu.getPassword(),
            'confirmpass': usu.getConfirmPass()
        }

        Datos.append(Dato)
        respuesta=jsonify(Datos)
    return (respuesta)      #Se muestra todos los usuarios existentes en el arreglo de Usuarios


#======================================== acciones para el usuario =============================================

@app.route('/NuevaPersona', methods=['POST'])   #Se ingresa nuevo usuario
def AgregarUsuario():
    global ArregloUsuarios
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    username=request.json['usuario']
    password=request.json['password']
    confirmpass = request.json['confirmpass']
    encontrado=False

    if nombre != "" and apellido !="" and username != "" and password !="" and confirmpass !="":
        for usu in ArregloUsuarios:
            if usu.getUsuario()==username:
                encontrado=True
                break

        if encontrado==True:
            return jsonify({
                "message":"Failed",
                "reason":"Existing user...Try a diferent User Name"
            })
        else:
            if password != confirmpass:
                return jsonify({
                    "message": "Failed",
                    "reason": "Must confirm your password"
                })
            else:
                nuevo= usuario(nombre,apellido,username,password,confirmpass)
                ArregloUsuarios.append(nuevo)
                return jsonify({
                    "message":"Success",
                    "reason":"The User was added"
                })
    else:
        return jsonify({
            "message": "Failed",
            "reason": "Debe llenar todos los campos"
        })

@app.route('/ConsultarPersona/<string:NombreUsuario>', methods=['GET'])    #consulta de un solo usuario
def MostrarPersona(NombreUsuario):
    global ArregloUsuarios
    for usu in ArregloUsuarios:
        if usu.getUsuario()==NombreUsuario:
            Dato={
                'nombre': usu.getNombre(),
                'apellido':usu.getApellido(),
                'usuario':usu.getUsuario(),
                'password':usu.getPassword(),
                'confirmpass':usu.getConfirmPass()
                }
            respuesta = jsonify(Dato)
            break

        else:respuesta=jsonify({"message":"Doesn´t exist that User"})
    return (respuesta)

@app.route('/EditarPersona/<string:NombreUsuario>', methods=['PUT'])    #Editar un solo usuario
def EditarPersona(NombreUsuario):
    band=False
    global ArregloUsuarios
    for indice in range(len(ArregloUsuarios)):
        if NombreUsuario==ArregloUsuarios[indice].getUsuario():
            if request.json['nombre'] !="" and request.json['apellido'] != "" and request.json['usuario'] !="" and request.json['password'] !="" and request.json['confirmpass'] and request.json['password'] == request.json['confirmpass']:
                ArregloUsuarios[indice].setNombre(request.json['nombre'])
                ArregloUsuarios[indice].setApellido(request.json['apellido'])
                ArregloUsuarios[indice].setUsuario(request.json['usuario'])
                ArregloUsuarios[indice].setPassword(request.json['password'])
                ArregloUsuarios[indice].setConfirmPass(request.json['confirmpass'])
                band=True

            elif request.json['password'] != request.json['confirmpass']:
                respuesta=jsonify({"message":"You Must confirm the Password"})

            else:
                respuesta = jsonify({"message": "You Must fill out all the requirements"})

            if band==True:
                respuesta = jsonify({"message":"User Modified"})
            break

        else:respuesta=jsonify({"message":"You can´t change your username"})
    return (respuesta)

@app.route('/EliminarPersona/<string:NombreElim>', methods=['DELETE'])  #Eliminar a un usuario
def EliminarUsuario(NombreElim):
    global ArregloUsuarios
    for i in range(len(ArregloUsuarios)):
        if NombreElim==ArregloUsuarios[i].getUsuario():
            del ArregloUsuarios[i]
            respuesta=jsonify({"message":"Usuario eliminado"})
            break

        else: respuesta=jsonify({"message":"Usuario no existente..."})
    return (respuesta)

#============================= Inicio de secion ===============================================
@app.route('/Login', methods=['POST'])
def Login():
    global ArregloAdmins
    global ArregloUsuarios
    username= request.json['usuario']
    password= request.json['password']

    for usu in ArregloAdmins:
        if usu.getUsuario()== username and usu.getPassword()==password:
            Dato={
                "message":"SuccessAdmin",
                "usuario": usu.getUsuario()
                }
            break

        else:
            for usu in ArregloUsuarios:
                if usu.getUsuario()== username and usu.getPassword()==password:
                    Dato={
                        "message":"Success",
                        "usuario": usu.getUsuario()
                        }
                    break

                else:
                    Dato={
                        "message":"Failed",
                        "usuario":""
                        }

    respuesta=jsonify(Dato)
    return (respuesta)

@app.route('/RecuperarPassword/<string:username>',methods=['GET'])
def RecuperarPass(username):
    global ArregloAdmins
    global ArregloUsuarios
    for usu in ArregloAdmins:
        if usu.getUsuario() == username:
            Dato = {
                "message": "Success",
                "password": usu.getPassword()
            }
            break

        else:
            for usu in ArregloUsuarios:
                if usu.getUsuario() == username:
                    Dato = {
                        "message": "Success",
                        "password": usu.getPassword()
                    }
                    break

                else:
                    Dato = {
                        "message": "Failed",
                        "password": ""
                    }

    respuesta = jsonify(Dato)
    return (respuesta)


#================== acciones para las canciones ======================

@app.route('/Cancion',methods=['POST']) #Se crea una nueva cancion en la clase cancion
def GuardarCancion():
    global ArregloCanciones, cont_canciones
    id=cont_canciones
    nombreCancion=request.json['cancion']
    artista=request.json['artista']
    album=request.json['album']
    fecha=request.json['fecha']
    imagen=request.json['imagen']
    spotify=request.json['spotify']
    youtube=request.json['youtube']
    nuevaCancion= cancion(id, nombreCancion, artista, album, fecha, imagen, spotify, youtube)
    ArregloCanciones.append(nuevaCancion)
    cont_canciones +=1
    return jsonify({
        "message":"Success",
        "razon":"The song was added"
    })

@app.route('/MostrarCancion',methods=['GET'])   #Muestra todas las canciones pero sin el ID
def ObtenerCancion():
    global ArregloCanciones, cont_canciones
    Datos=[]
    for cancion in ArregloCanciones:
        Dato={
            'cancion':cancion.getCancion(),
            'artista':cancion.getArtista(),
            'album':cancion.getAlbum(),
            'fecha':cancion.getFecha(),
            'imagen':cancion.getImagen(),
            'spotify':cancion.getSpotify(),
            'youtube':cancion.getYoutube()
            }
        Datos.append(Dato)
    respuesta=jsonify(Datos)
    return (respuesta)

@app.route('/MostrarCancionSimple',methods=['GET']) #Muestra las canciones cargadas, pero con poca informacion
def ObtenerCancionID():
    global ArregloCanciones, cont_canciones
    Datos=[]
    for cancion in ArregloCanciones:
        Dato={
            'id':cancion.getId(),
            'spotify':cancion.getSpotify(),
            }
        Datos.append(Dato)
    respuesta=jsonify(Datos)
    return (respuesta)

@app.route('/ConsultarCancion/<int:IdCancion>', methods=['GET'])    #consulta de una cancion
def MostrarCancion(IdCancion):
    global ArregloCanciones
    Datos=[]
    for song in ArregloCanciones:
        if song.getId() == IdCancion:
            Dato={
                'cancion':song.getCancion(),
                'artista':song.getArtista(),
                'album':song.getAlbum(),
                'fecha':song.getFecha(),
                'imagen':song.getImagen(),
                'youtube':song.getYoutube()
                }
            Datos.append(Dato)
            respuesta = jsonify(Datos)
            break
        else:respuesta = jsonify({"message": "Doesn´t exist that User"})
    return (respuesta)
#======================================== acciones para el Admin =============================================
@app.route('/NuevoAdmin', methods=['POST'])   #Se ingresa nuevo Admin
def AgregarAdmin():
    global ArregloAdmins
    nombre=request.json['nombre']
    apellido=request.json['apellido']
    username=request.json['usuario']
    password=request.json['password']
    confirmpass = request.json['confirmpass']
    encontrado=False

    if nombre != "" and apellido !="" and username != "" and password !="" and confirmpass !="":
        for usu in ArregloAdmins:
            if usu.getUsuario()==username:
                encontrado=True
                break

        if encontrado==True:
            return jsonify({
                "message":"Failed",
                "reason":"Existing user..."
            })
        else:
            if password != confirmpass:
                return jsonify({
                    "message": "Failed",
                    "reason": "Must confirm your password"
                })
            else:
                nuevo= admin(nombre,apellido,username,password,confirmpass)
                ArregloAdmins.append(nuevo)
                return jsonify({
                    "message":"Success",
                    "reason":"The Admin was added"
                })
    else:
        return jsonify({
            "message": "Failed",
            "reason": "Must fill out all the requirements"
        })

@app.route('/VerAdmins', methods=['GET'])  # Consultar todos los datos de administrador
def ObtenerAdmins():
    global ArregloAdmins
    for usu in ArregloAdmins:
        Dato = {
            'nombre': usu.getNombre(),
            'apellido': usu.getApellido(),
            'usuario': usu.getUsuario(),
            'password': usu.getPassword(),
            'confirmpass': usu.getConfirmPass()
        }

        respuesta = jsonify(Dato)
    return (respuesta)  # Se muestra todos los usuarios existentes en el arreglo de Admins

#==========================Agregar a la Playlist==========================================================
@app.route('/AddPlaylist',methods=['POST']) #Se agrega una nueva cancion en la clase playlist
def AlmacenarPlaylist():
    global ArregloPlaylist
    id=request.json['id']
    nombreCancion=request.json['cancion']
    artista=request.json['artista']
    album=request.json['album']
    fecha=request.json['fecha']
    imagen=request.json['imagen']
    spotify=request.json['spotify']
    youtube=request.json['youtube']
    nuevaPlaylist= cancion(id, nombreCancion, artista, album, fecha, imagen, spotify, youtube)
    ArregloPlaylist.append(nuevaPlaylist)
    return jsonify({
        "message":"Success",
        "razon":"The Playlist was updated"
    })

@app.route('/MostrarPlaylist',methods=['GET'])   #Muestra todas las canciones pero sin el ID
def ObtenerPlaylist():
    global ArregloPlaylist
    Datos=[]
    for cancion in ArregloPlaylist:
        Dato={
            'id':cancion.getId(),
            'cancion':cancion.getCancion(),
            'artista':cancion.getArtista(),
            'album':cancion.getAlbum(),
            'fecha':cancion.getFecha(),
            'imagen':cancion.getImagen(),
            'spotify':cancion.getSpotify(),
            'youtube':cancion.getYoutube()
            }
        Datos.append(Dato)
    respuesta=jsonify(Datos)
    return (respuesta)

if __name__=="__main__":
    app.run(port=3000, debug=True)