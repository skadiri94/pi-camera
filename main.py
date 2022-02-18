#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, make_response,Response, request,session, jsonify, redirect, url_for,flash
import jwt
from flask_qrcode import QRcode
from datetime import datetime, timedelta
from functools import wraps
from camera import VideoCamera
import threading
import os
from key_gen import generate_key

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

secrete_keys = generate_key()
private_key = secrete_keys[0]
public_key = secrete_keys[1]
private_key = private_key.replace('-----BEGIN ENCRYPTED PRIVATE KEY-----\n', '')
private_key = private_key.replace('\n-----END ENCRYPTED PRIVATE KEY-----\n', '')
public_key= public_key.replace('-----BEGIN PUBLIC KEY-----\n', '')
public_key = public_key.replace('\n-----END PUBLIC KEY-----\n', '')
public_key = public_key.replace('\n', '')
public_key = public_key.replace(' ', '')

print(public_key)
# App Globals (do not edit)
app = Flask(__name__)
app.config['SECRET_KEY'] = private_key
QRcode(app)

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
        # You can use the JWT errors in exception
        # except jwt.InvalidTokenError:
        #     return 'Invalid token. Please log in again.'
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
def index():
    if not session.get("logged_in"):
        return redirect(url_for('login'))
    return render_template('index.html') #you can customze index.html here

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == "POST":
    #     first_set = set(public_key)
    #     second_set = set(request.form['publickey'])
    #     difference = first_set.symmetric_difference(second_set)
    #     lk = str(request.form['publickey']).replace(' ','').strip()
    #     lk = lk.replace('\n', '')
        if request.form['publickey'] == public_key:
            
            session['logged_in'] = True
            
            token = jwt.encode({
                'user': request.form['publickey'],
                # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
                'expiration': str(datetime.utcnow() + timedelta(seconds=60))
            },
                app.config['SECRET_KEY'])
            return jsonify({'token': token.decode('utf-8')})
        else:
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
    return render_template("login.html")
 
 
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")   
    
def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(ssl_context=('cert.pem', 'key.pem'), host='0.0.0.0', debug=False)
    


