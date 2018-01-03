#! /usr/bin/env python3

import sys
import os
from hashlib import sha1
import base64
import time
from getpass import getuser

class Gpy(object):
    
    def __init__(self):
        self.path = os.getcwd()
        self.t = time.time()
        self.time_ = time.asctime(time.localtime(self.t))
        self.user = getuser()
    
    
    def init(self):
        
        try:
            # Creando directorios
            os.mkdir(self.path+"/.gpy")
            os.mkdir(self.path+"/.gpy/files")  # Carpeta donde se guardaran las ramas...
            os.mkdir(self.path+"/.gpy/commits")  # Carpeta donde se guardaran los commits...

            # Creando archivo de la rurta
            with open(self.path+"/.gpy/path", "w") as fl:
                fl.write(self.path)

            with open(self.path+"/.gpy/commits/commits", "w"):
                pass

            return "Init creado."
        except FileExistsError as e:
            return "Repositorio ya inicializado..."
            
    
    def status(self):
        r = []

        with open(self.path+"/.gpy/path", "r") as fl:
            files = fl.readlines()

        files = [_.replace("\n", "") for _ in files[1:]]
        tmp = {}
        for x in files:
            tmp[x] = self.clasify(x)[-1].split("\n")[1]

        for y in tmp:
            with open(y, "r") as fl:
                datos = fl.read()
            with open(self.path+"/.gpy/files/"+tmp[y], "r") as fl:
                datos_c = fl.read()

            if datos != datos_c:
                r.append(y.split("/")[-1])

        return (r, tmp)


    def diff(self):
        r, tmp = self.status()
        changes = {}
        if len(r) > 0: 
            for key in tmp:
                if key.split()[-1] not in changes:
                    changes[key.split("/")[-1]] = ""
                with open(key, "r") as fl:
                    datos = fl.readlines()
                    datos = [_.replace("\n", "") for _ in datos]
                    datos = [_ for _ in datos if _ ]
                with open(self.path+"/.gpy/files/"+tmp[key], "r") as fl:
                    datos_c = fl.readlines()
                    datos_c = [_.replace("\n", "") for _ in datos_c]
                    datos_c = [_ for _ in datos_c if _ ]

                if len(datos) > len(datos_c):
                    for i, s in enumerate(datos):
                        if s not in datos_c:
                            changes[key.split("/")[-1]] += "+{0}\n\t".format(s)
                                
                elif len(datos) <= len(datos_c):
                    for i, s in enumerate(datos_c):
                        
                        if s not in datos:
                            changes[key.split("/")[-1]] += "-{0}\n\t".format(s)
                            changes[key.split("/")[-1]] += "+{0}\n\t".format(datos[i])


        return changes

    def log(self):
        with open(self.path+"/.gpy/commits/commits", "r") as fl:
            logs = fl.read()
        return logs
    
    
    def review(self, file, id_commit):
        ruta_absoluta = os.path.abspath(file)
        if ruta_absoluta not in self.status()[0]:
            try:
                if os.path.isfile(ruta_absoluta):
                    logs = self.clasify(ruta_absoluta)
                    file_commit = ""

                    if len(logs) > 0:
                        if id_commit == "-n":
                            
                            with open(self.path+"/.gpy/files/"+logs[-1].split("\n")[1], "r") as fl:
                                datos = fl.read()

                            with open(ruta_absoluta, "w") as fl:
                                fl.write(datos)
                        else:
                            for _ in logs:
                                if id_commit in _ and ruta_absoluta in _:
                                    file_commit = _

                            if file_commit:
                                with open(self.path+"/.gpy/files/"+id_commit, "r") as fl:
                                    datos = fl.read()
                                
                                with open(ruta_absoluta, "w") as fl:
                                    fl.write(datos) 
                                
                            else:
                                return "No coinciden el id y el archivo"
                        
                        return "Viaje completado"
                    
                    else:
                        return "No hay commits en este archivo"

                else:
                    return "Tiene que ser un archivo"

            except FileNotFoundError as e:
                return "Repositorio no inicializado"
        else:
            return "Debe incluir los cambios y los commit"

    def add(self, file):
        try:
            ruta_absoluta = os.path.abspath(file)
            commit_hash = sha1(str(self.t).encode("utf-8")).hexdigest()
            logs_f = self.clasify(ruta_absoluta)
            datos_b = ""

            with open(self.path+"/.gpy/path", "r") as fl:
                files = fl.readlines()
            with open(self.path+"/.gpy/path", "a") as fl:
                if ruta_absoluta not in files:
                    fl.write("\n"+ruta_absoluta)

            if len(logs_f) > 0:
                ultimo_commit = logs_f[-1].split("\n")[1]
                
                with open(self.path+"/.gpy/files/"+ultimo_commit, "r") as fl:
                    datos_b = fl.read()
               
            if os.path.isfile(ruta_absoluta):
                with open(ruta_absoluta, "r") as fl:
                    datos = fl.read()


                if datos_b:
                    if datos_b != datos:
                        with open(self.path+"/.gpy/files/"+commit_hash, "w") as fl:
                            fl.write(datos)
                    
                        self.commit(ruta_absoluta, logs_f, commit_hash)
                else:
                    with open(self.path+"/.gpy/files/"+commit_hash, "w") as fl:
                        fl.write(datos)
                    
                    self.commit(ruta_absoluta, logs_f, commit_hash)
                
                return "Anadido"
                    
            else:
                return "Tiene que ser un archivo"
        except FileNotFoundError as e:
            return "Repositorio no inicializado"

    def commit(self, ruta_absoluta, logs_f, commit_hash):
        m = str(input("Escribe el mensaje del commit: "))
        commit = "\n{0}\n{2} | {1} ({5})\n Path: {4}\n{3}\n\t".format(
            commit_hash,
            self.time_,
            self.user,
            m,
            ruta_absoluta,
            len(logs_f)+1)
        
        with open(self.path+"/.gpy/commits/commits", "a") as fl:
            fl.write(commit)
        
        print("\n"+commit+"\n")


    def clasify(self, file):
        logs = []
        for _ in self.log().split("\t"):
            if file in _:
                logs.append(_)
        return logs



if __name__ == "__main__":
    gpy = Gpy()
    
    if sys.argv[1] == "init":
        print(gpy.init())
    elif sys.argv[1] == "add":
        print(gpy.add(sys.argv[2]))
    elif sys.argv[1] == "log":
        logs = gpy.log()
        for _ in logs.split("\t"):
            print(_)
    elif sys.argv[1] == "review":
        print(gpy.review(sys.argv[2], sys.argv[3]))
    elif sys.argv[1] == "status":
        changes = gpy.status()[0]
        if changes:
            print("\nFueron cambiados:\n")
            for x in changes:
                print("\t"+x)
        else:
            print("No hay cambios")
    elif sys.argv[1] == "diff":
        changes = gpy.diff()
        for _ in changes:
            print("File: " + _)
            print("\t"+changes[_])
