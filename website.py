from flask import Flask, send_file, request, redirect, render_template, url_for, session, escape
import main
import dbhandler
import os

app = Flask(__name__)
app.secret_key = b'jbd5#jfb-=23!()F"'
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%*()?/{}[]|-_+=`~><,.'


@app.route('/')
def run():
    if 'username' in session:
        if os.path.isfile('Output/' + session['username'] + '.pdf'):
            ans = open('Data/files/answer.txt', 'r')
            txt = ans.read().replace('\n\n', '\n').replace('\n\n', '\n')
            session['text'] = txt
            ans.close()
            return render_template('app1.html', session=session)
        return render_template('app2.html', session=session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        ans = open('Data/files/answer.txt', 'r')
        txt = ans.read().replace('\n\n', '\n').replace('\n\n', '\n')
        ans.close()
        return render_template('app1.html', session=session)
    if request.method == 'POST':
        name, pwd = request.form['username'], request.form['pwd']
        if len(name) > 10:
            return render_template('login.html', error='Username should not exceed 10 Characters!')
        if len(pwd) > 10:
            return render_template('login.html', error='Password should not exceed 10 Characters!')
        for i in name:
            if i not in chars:
                return render_template('login.html', error='Username contains Invalid Character!')
        for i in pwd:
            if i not in chars:
                return render_template('login.html', error='Password contains Invalid Character!')

        try:
            mail = request.form['mail']
            status = dbhandler.dump(name, mail, pwd)
            if status:
                session['username'] = name
                return render_template('app2.html', session=session)
        except:
            if dbhandler.check(name, pwd):
                session['username'] = name
                if os.path.isfile('Output/' + name + '.pdf'):
                    ans = open('Data/files/answer.txt', 'r')
                    txt = ans.read().replace('\n\n', '\n').replace('\n\n', '\n')
                    ans.close()
                    session['text'] = txt
                    return render_template('app1.html', session=session)
                return render_template('app2.html', session=session)
        return render_template('login.html', error='Invalid Username or Password!')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('run'))


@app.route('/app')
def application():
    html = open('templates/app1.html', 'r')
    txt = html.read()
    html.close()
    return txt


@app.route('/viewer')
def viewer():
    name = session['username']
    if os.path.isfile('Output/'+name+'.pdf'):
        return send_file('Output/'+name+'.pdf', mimetype='application/pdf')
    return '<div style="font-family: Raleway, sans-serif;font-size: 30px;position: absolute;top: 300px;left: 200px;' \
           'font-weight: 540;text-align: center;color: white;z-index: 1;">GENERATE YOUR ANSWERS!</div>'


@app.route('/submit', methods=['POST'])
def submit():
    name, col, hw = request.form['text'].replace('-', ' '), request.form['colour'], request.form['hw']
    uname = session['username']
    main.run(name, col, uname, hw, 1)
    return redirect('/')

@app.route('/edit', methods=['POST'])
def edit():
    name, col, hw = request.form['text'].replace('-', ' '), request.form['colour'], request.form['hw']
    uname = session['username']
    session['text'] = name.replace('\n\n', '\n').replace('\n\n', '\n')
    main.run(name, col, uname, hw, 2)
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    uname = session['username']
    os.remove('Output/'+uname+'.pdf')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
