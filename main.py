from flask import Flask, render_template, make_response,Response, request,session, jsonify, redirect, url_for,flash
import jwt
import uuid
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
from uuid import getnode as get_mac
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
mac_addr = get_mac()
bindingInfo = Blockchain().getBindingInfo(str(mac_addr))
one_time_nonce = None
w3 = Web3(Web3.HTTPProvider(""))
print(bindingInfo)

def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if 'token' in session:
            token = session['token']
        if not token:
            return render_template("login.html"), 401

        try:
            keys = get_generated_key()
            public_key = keys[1]
            public_key = public_key
            data = jwt.decode(token, public_key, algorithms=['RS256'])
            
        except:
            return render_template("login.html"), 403
        return func(*args, **kwargs)
    return decorated


@app.route('/')
@token_required
def index():
    return render_template('index.html') 

@app.route('/nonce', methods=['GET'])
def nonce():
    global one_time_nonce
    one_time_nonce  = generate_nonce()
    return jsonify({'Message' : one_time_nonce}),200 

@app.route('/auth', methods=['POST'])
def auth():
    global one_time_nonce
    msg = 'Singning one-time nonce:' + str(one_time_nonce )
    if request.method == "POST":
        data = request.get_json()
        temp_signature = data['signature']
    # We now are in possession of msg, publicAddress and signature. We
    # can perform an elliptic curve signature verification with ecrecover
        mesage = encode_defunct(text=msg)
        address = w3.eth.account.recover_message(mesage,signature=HexBytes(temp_signature ))
        if address.lower() == bindingInfo[0].lower():
            keys = get_generated_key()
            if keys != None:
                private_key = keys[0]
                token = jwt.encode({
                    'user': " Testing",
                    'exp': datetime.now() + timedelta(seconds=30)
                }, private_key, algorithm='RS256').decode('utf-8')

                session['token'] = token
                return redirect(url_for('index'))  
        
        
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate': 'Basic realm: "Authentication Failed "'})

@app.route('/login', methods=['GET', 'POST'])
@token_required
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
        if bindingInfo[1] == False:
            userAdd = request.form['address']
            res = Blockchain().bindCam(str(mac_addr),userAdd)
            if res == 1:
                return render_template("login.html")
            else:
                return jsonify({'Message' : 'User exist in this device'})
        else:
            return jsonify({'Message' :'Device is corrently binded'})
    return render_template("register.html")   

def generate_nonce():
    """Generate pseudorandom number."""
    return uuid.uuid4().hex
    
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
    


