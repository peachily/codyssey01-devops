from flask import Flask, render_template
import socket

app = Flask(__name__)

@app.route('/')
def home():
    if app.debug:
      hostname = '컴퓨터(인스턴스) : ' + socket.gethostname()
    else:
      hostname = ' '
    return render_template('index.html', computername=hostname)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)