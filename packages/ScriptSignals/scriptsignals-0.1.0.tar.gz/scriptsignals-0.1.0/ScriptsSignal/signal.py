import json
import random
import threading
import time

class signal:
    @staticmethod
    def send(a, mensaje, datos, name, func):
        
        with open("server.txt", "r+") as f:
            data = json.load(f)
            id = random.randint(1,9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
            lista = []
            for e, fo in data.items():
                lista.append(fo["id"])
            while id in lista:
                id = random.randint(1,9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
            data[a] = {"mensaje": [mensaje, name, datos], "id": id}
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)
            def revise():
                while True:
                    with open("client.txt", "r+") as file:
                        info = json.load(file)
                        for e in info:
                            if e == name:
                                func(info[e]["mensaje"])
                                break
                        print(info)
                        time.sleep(1)
            hilo = threading.Thread(target=revise)
            hilo.start()
    @staticmethod
    def respond(to, mensaje, datos, name):
        with open("client.txt", "r+") as f:
            data = json.load(f)
            data[to] = {"mensaje": [mensaje, name, datos]}
            f.seek(0)
            f.truncate(0)
            json.dump(data, f, indent=4)
    @staticmethod
    def create_server(func, name):
        def gon():
            while True:
                with open("server.txt", "r+") as file:
                    info = json.load(file)
                    for e in info:
                        if e == name:
                            func(info[e]['mensaje'])
                
                
                
                time.sleep(1)
        hilo = threading.Thread(target=gon)
        hilo.start()