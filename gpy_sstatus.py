#! /usr/bin/env python3

__all__ = """
        Este archivo se encargara de reotrnar el estado de los archivo, si ahn sido cambiados o no...
"""
import clasify

class Status(object):
    def __init_(self, path):
        self.path = path
        self.cl = clasify()
    
    
    def status(self):
        result = []

        with open(self.path+"/.gpy/path", "r") as fl:
            files = fl.readlines()
        
        files_hash = [_.replace("\n", "") for _ in files[1:]]
        files_n_h = {}
        for file_hash in files_hash:
            tmp[file_hash] = cl.find(file_hash)[-1].split("\n")[1]

        for file_ in files_n_h:
            with open(file_, "r") as fl:
                datos = fl.read()
            with open(self.path + "/.gpy/files/" + files_n_h[file_], "r") as fl:
                datos_c = fl.read()

            if datos != datos_c:
                r.append(file_.split("/")[-1])

        return (result, files_n_h)