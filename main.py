#from flask import Flask, render_template
import socket
from struct import unpack
import threading
import sys

MSGLEN_BYTE = 12        # int (64) + float (64) + float (64) = 8 + 8 + 8 = 24 byte
SERVERPORT = 2500

DISCONNECT_MESSAGE = "!DISCONNECT!"
FORMAT             = 'utf-8'

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
    print("Received " + str(bytesReceived) + " bytes")
    return b''.join(chunks)


def ParseData(bytes: bytes) -> (int, float, float):
    timestamp, temp, hum = unpack('<iff', bytes)
    return timestamp, temp, hum


def ClientHandle(clientConnection: socket.socket, clientAddress):
    print(f"\n[THREAD][NEW CONNECTION] {clientAddress} connected.")

    connected = True

    while connected:
        bytes = ReceiveData(clientConnection)
        print(f"\n[THREAD][DATA] {bytes} - {bytes.decode(FORMAT)} - {bytes.decode(FORMAT) == DISCONNECT_MESSAGE} - {DISCONNECT_MESSAGE}")
        if bytes.decode(FORMAT) == DISCONNECT_MESSAGE:
            print("Disconnect message received")
            connected = False
        else:
            tim, t, h = ParseData(bytes)
            # TODO gestione della memorizzazione dei dati
            print(f"[{tim}] - Temperature = {t}, Humidity = {h}")

    print("\nClosing the connection")
    clientConnection.close()


print("[MAIN]Raspberry Pi Server init")
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
ipAddr = socket.gethostname()
ipAddr = "192.168.178.32"   # FIXME test ip
serverSocket.bind((ipAddr, SERVERPORT))
serverSocket.listen()
print(f"[MAIN]Listening on {ipAddr}:{SERVERPORT}")

while (True):
    try:
        clientConnection, clientAddress = serverSocket.accept()
        thread = threading.Thread(target=ClientHandle, args=(clientConnection, clientAddress))
        thread.start()
        print(f"\n[MAIN][ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    except KeyboardInterrupt:
        serverSocket.close()
        print("\nKeyboard Interrupt received. Closing socket and halting the applcation")
        sys.exit(0)