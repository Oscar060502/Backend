# pylint:disable=all
import socket
import threading
import sys
import os
import pickle

class Cliente():
    def __init__(self, host="localhost", port=7000):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((str(host), int(port)))
            msg_recv = threading.Thread(target=self.msg_recv)
            msg_recv.daemon = True 
            msg_recv.start()
            while True:
                msg = input('cliente> ')
                if msg == 'salir':
                    self.sock.close()
                    sys.exit()
                elif msg.startswith("/"):  # Si el mensaje es un comando (empieza con "/")
                    self.send_command(msg[1:])
                else:
                    self.send_msg(msg)
        except Exception as e:
            print("Error al conectar el socket:", e)

    def msg_recv(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    data = pickle.loads(data)
                    if isinstance(data, dict) and "file_data" in data:  #Si se recibe un archivo
                        self.guardar_archivo(data["filename"], data["file_data"])
                    else:
                        print(f"Servidor: {data}")  # Mensaje o respuesta del servidor
            except Exception as e:
                print("Error en la recepción de datos:", e)
                break


    def send_msg(self, msg):
        try:
            paquete = {"type": "message", "content": msg}
            self.sock.send(pickle.dumps(paquete))
        except Exception as e:
            print('Error al enviar el mensaje:', e)

    def send_command(self, command):
        try:
            paquete = {"type": "command", "content": command}
            self.sock.send(pickle.dumps(paquete))
        except Exception as e:
            print('Error al enviar el comando:', e)

    def guardar_archivo(self, filename, file_data):
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        with open(os.path.join("downloads", filename), 'wb') as f:
            f.write(file_data)
        print("Guardando el archivo espere....")
        print(f"Archivo guardado como {filename} en la carpeta 'downloads'.")


if __name__ == "__main__":
    cliente = Cliente()
