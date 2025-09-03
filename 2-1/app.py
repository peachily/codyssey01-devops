from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test1')
def test1():
    return render_template('test1.html')
@app.route('/test3')
def test3():
    return render_template('test3.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
