from flask import Flask,request,render_template
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html');

@app.route('/ipSetting')
def ipSetting():
    return render_template('ipSetting.html');

@app.route("/iniUpdate/")
@app.route("/iniUpdate",methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        f.save('/home/titan/Titan/github/python/flask/fileUpload/file/'+ secure_filename(f.filename))
    return render_template('iniUpdate.html');

@app.route('/iniSelect')
def iniSelect():
    return render_template('iniSelect.html');

@app.route('/iniBuild')
def iniBuild():
    return render_template('iniBuild.html');

@app.route('/ping')
def ping():
    return render_template('ping.html');

@app.route('/pings',methods=['POST'])
def pings():
    ip = request.form.get('ip')
    try:
        response = subprocess.check_output(
            ['ping', '-c', '1', ip],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
            )
    except :
        response = "From "+ ip +" Destination Host Unreachable"
    return response

@app.route('/logs')
def logs():
    return render_template('logs.html');

@app.route('/sentTest')
def sentTest():
    return render_template('sentTest.html');

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
