from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def index():
    # Leggi i dati dalla socket e passali al template HTML
    temperature, humidity = read_data_from_socket()
    return render_template('index.html', temperature=temperature, humidity=humidity)

def read_data_from_socket():
    # Connessione alla socket e lettura dei dati
    # Inserisci qui la logica per leggere i dati dalla socket
    # Ritorna i dati di temperatura e umidità
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')