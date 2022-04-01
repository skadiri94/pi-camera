from flask import Flask, render_template, make_response,Response, request,session, jsonify, redirect, url_for,flash
import jwt
from flask_qrcode import QRcode
from datetime import datetime, timedelta
from functools import wraps
from camera import VideoCamera
import threading
import os
from key_gen import generate_key, get_generated_key, get_keys
from blockchain import Blockchain

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down. 





# App Globals (do not edit)
app = Flask(__name__)
app.config['SECRET_KEY'] = "Secrete_key"
QRcode(app)
print(Blockchain())
def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in session:
            token = session['token']
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            keys = get_generated_key()
            public_key = keys[1]
            public_key = public_key
            data = jwt.decode(token, public_key, algorithms=['RS256'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
@token_required
def index():
    return render_template('index.html') 

@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard !  '

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    public_key = get_keys(get_generated_key())
    keys = get_generated_key()
    if keys != None:
        private_key = keys[0]
    
    if request.method == "POST":

        if request.form['publickey'] == public_key:
            
            token = jwt.encode({
                'user': " Testing",
                'exp': datetime.now() + timedelta(seconds=30)
            }, private_key, algorithm='RS256').decode('utf-8')

            session['token'] = token
            return redirect(url_for('index'))  
        else:
            return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})
    return render_template("login.html")
 
 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        public_key = get_keys(generate_key())
        if public_key == None:
            return 'User exist in this device'
        else:
            return jsonify({'Public Key': public_key})
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
    


