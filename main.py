#from flask import Flask, render_template
import socket
from struct import unpack

MSGLEN_BYTE = 24        # int (64) + float (64) + float (64) = 8 + 8 + 8 = 24 byte
SERVERPORT = 2500

# app = Flask(__name__)

# @app.route('/')
# def index():
#     # Leggi i dati dalla socket e passali al template HTML
#     temperature, humidity = read_data_from_socket()
#     return render_template('index.html', temperature=temperature, humidity=humidity)

# def read_data_from_socket():
#     # Connessione alla socket e lettura dei dati
#     # Inserisci qui la logica per leggere i dati dalla socket
#     # Ritorna i dati di temperatura e umidità
#     pass

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')

def ReceiveData(sock: socket.socket) -> bytes:
    chunks = []
    bytesReceived = 0
    while bytesReceived < MSGLEN_BYTE:
        chunk = sock.recv(min(MSGLEN_BYTE - bytesReceived, 2048))
        if chunk == b'':
            raise RuntimeError("socket connection broken")
        chunks.append(chunk)
        bytesReceived = bytesReceived + len(chunk)
    return b''.join(chunks)


def ParseData(bytes: bytes) -> (int, float, float):
    timestamp, temp, hum = unpack('<iff', bytes)
    return timestamp, temp, hum


print("Raspberry Pi Server init")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket((socket.gethostname(), SERVERPORT))
serverSocket.listen()
print("Init done")

