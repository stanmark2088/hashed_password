from flask import Flask, render_template, request, session, redirect, url_for, flash
import password_manager

app = Flask(__name__)
app.secret_key = '6w:`tFm%mBLY}ty*QcRRpD+,Jga@Fy\XFxjhga'


@app.route('/')
def index():
    return render_template('index.html', state='default')


@app.route('/hash', methods=['POST'])
def hash_pw():
    plain_text_pw = request.form.get('password')
    hashed_pw = password_manager.hash_password(plain_text_pw)
    session['result'] = hashed_pw
    return redirect(url_for('index'))


@app.route('/verify', methods=['POST'])
def verify_pw():
    session['plain_text_pw'] = request.form.get('password')
    session['hashed_pw'] = request.form.get('hash')

    try:
        is_match = password_manager.verify_password(session.get('plain_text_pw'), session.get('hashed_pw'))
    except ValueError:
        is_match = False

    state = 'verified' if is_match else 'failed'

    return render_template('index.html', state=state)



if __name__ == '__main__':
    app.run(debug=True,
            port=5000)