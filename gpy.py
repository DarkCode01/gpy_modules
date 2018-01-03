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
            os.mkdir(self.path+"/.gpy/files")  # Carpeta donde se guardaran las copias de los archivos...
            os.mkdir(self.path+"/.gpy/commits")  # Carpeta donde se guardaran los commits...

            # Creando archivo de la rurta
            self.file_ope(".gpy/path", "w", self.path
            self.file_ope("gpy/commits/commits", "w", "pass"):

            return "Init creado."
        
        except FileExistsError as e:
            return "Repositorio ya inicializado..."
            
    
    def status(self):
        result = []
        files = self.file_ope(".gpy/path", "r").split("\n")
        files = [file_.replace("\n", "") for file_ in files[1:]]
        tmp = {file_: self.clasify(file_)[-1].split("\n")[1]}
        for file_hash in tmp:
            datos = fl.self.file_ope(file_hash, "r")
            datos_c self.file_ope(".gpy/files/" + tmp[file_hash], "r")
                
            if datos != datos_c:
                r.append(file_hash.split("/")[-1])

        return (result, tmp)


    def diff(self):
        r, tmp = self.status()
        changes = {}
        if len(r) > 0: 
            for key in tmp:
                if key.split()[-1] not in changes:
                    changes[key.split("/")[-1]] = ""

                datos = self.file_ope(key, "").split("\n")
                datos = [_.replace("\n", "") for _ in datos]
                datos = [_ for _ in datos if _ ]

                datos_c = self.file_ope(".gpy/files/" + tmp[key], "r").split("\n")
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
        commits = self.file_ope(".gpy/commits/commits", "r")
        return commits
    
    
    def review(self, file_, id_commit):
        ruta_absoluta_archivo = os.path.abspath(file_)
        if ruta_absoluta_archivo not in self.status()[0]:
            try:
                if os.path.isfile(ruta_absoluta_archivo):
                    logs = self.clasify(ruta_absoluta_archivo)
                    file_commit = ""

                    if len(logs) > 0:
                        if id_commit == "-n":
                            datos = self.file_ope(".gpy/files/" + logs[-1].split("\n")[1], "r")
                            self.file_ope(ruta_absoluta_archivo, "w", datos)
                        else:
                            for log in logs:
                                if id_commit in log and ruta_absoluta_archivo in _:
                                    file_commit = log

                            if file_commit:
                                datos = self.file_ope(".gpy/files/" + id_commit, "r")
                                self.file_ope(ruta_absoluta_archivo, "w", datos) 
                                
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

    def add(self, file_):
        try:
            ruta_absoluta_archivo = os.path.abspath(file_)
            commit_hash = sha1(str(self.t).encode("utf-8")).hexdigest()
            logs_f = self.clasify(ruta_absoluta_archivo)
            datos_b = ""
            files = self.file_ope(".gpy/path", "r").split("\n")
            
            if ruta_absoluta_archivo not in files:
                self.file_ope(".gpy/path", "a", ruta_absoluta_archivo)

            if len(logs_f) > 0:
                ultimo_commit = logs_f[-1].split("\n")[1]
                datos_b = self.file_ope(".gpy/files/" + ultimo_commit, "r")
               
            if os.path.isfile(ruta_absoluta_archivo):
                datos = self.file_ope(ruta_absoluta_absoluta, "r")
                    
                if datos_b:
                    if datos_b != datos:
                        self.file_ope(".gpy/files/" + commit_hash, "w", datos)
                        self.commit(ruta_absoluta_archivo, logs_f, commit_hash)
                else:
                    self.file_ope(".gpy/files/" + commit_hash, "w", datos)
                    self.commit(ruta_absoluta_archivo, logs_f, commit_hash)
                
                return "Anadido"
                    
            else:
                return "Tiene que ser un archivo"
        
        except FileNotFoundError as e:
            return "Repositorio no inicializado"


    def commit(self, ruta_absoluta_archivo, logs_f, commit_hash):
        mensaje_commit = str(input("Escribe el mensaje del commit: "))
        
        commit = "\n{0}\n{2} | {1} ({5})\n Path: {4}\n{3}\n\t".format(
            commit_hash,
            self.time_,
            self.user,
            mensaje_commit,
            ruta_absoluta_archivo,
            len(logs_f)+1)
        
        self.file_ope(".gpy/commits/commits", "a", commit)
        
        print("\n" + commit + "\n")


    def clasify(self, file_):
        commits = []
        for commit in self.log().split("\t"):
            if file_ in commit:
                logs.append(commit)
        return commits
    
    def file_ope(self, file_, argv):
        ruta_absoluta_archivo = os.path.abspath(file_)
        with open(ruta_absoluta_archivo, argv, string=None) as fl:
            if string:
                fl.write(string if string != "pass" else "")
            elif argv in ("r"):
                result = fl.read()
        return result
        
        
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
