from flask import Flask, send_file, request, redirect
import main
app = Flask(__name__)
prep = True


@app.route('/')
def run():
    html = open('Data/assets/test.html', 'r')
    txt = html.read()
    html.close()
    return txt


@app.route('/viewer')
def viewer():
    if prep:
        return send_file('Output/solved.pdf', mimetype='application/pdf')
    return ' '


@app.route('/submit', methods=['POST'])
def submit():
    name, col = request.form['text'], request.form['color']
    main.run(name, col)
    return redirect('/')

if __name__ == '__main__':
    app.run()