from flask import Flask,request,render_template,redirect,url_for
from werkzeug.utils import secure_filename
from library.Network_config import  Net_config,File_search
import subprocess
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ipSettingMain')
def ipSettingMain():
    return render_template('ipSettingMain.html')

@app.route('/setIpMain', methods=['POST'])
def setIpMain():
    print(request.form)
    if request.form['ipMethod'] == 'dhcpIP':
        print('dhcp')
        Net_config().eth0_dhcp()
    elif request.form['ipMethod'] == 'staticIP':
        staticIP = request.form['staticIP']
        staticMask = request.form['staticMask']
        staticGateway = request.form['staticGateway']
        print(staticIP,staticMask,staticGateway)
        Net_config().eth0_static(staticIP, staticMask, staticGateway)
    return redirect('/ipSettingMain')

@app.route('/dnsMain', methods=['POST'])
def dnsMain():
    print(request.form)
    if request.form['DNS'] == 'autoDNS':
        Net_config().eth0_auto_dns()
        print('autoDNS')
    elif request.form['DNS'] == 'staticDNS':
        defaultDNS = request.form['defaultDNS']
        otherDNS = request.form['otherDNS']
        if otherDNS == '' :
            Net_config().eth0_dns(defaultDNS)
        else :
            Net_config().eth0_dual_dns(defaultDNS,otherDNS)
        print(defaultDNS,otherDNS)
    return redirect('/ipSettingMain')

@app.route('/ipSettingSecond')
def ipSettingSecond():
    return render_template('ipSettingSecond.html')

@app.route('/setIpSecond', methods=['POST'])
def setIpSecond():
    print(request.form)
    if request.form['ipMethod'] == 'dhcpIP':
        print('dhcp')
        Net_config().eth1_dhcp()
    elif request.form['ipMethod'] == 'staticIP':
        staticIP = request.form['staticIP']
        staticMask = request.form['staticMask']
        staticGateway = request.form['staticGateway']
        print(staticIP,staticMask,staticGateway)
        Net_config().eth1_static(staticIP, staticMask, staticGateway)
    return redirect('/ipSettingSecond')

@app.route('/dnsSecond', methods=['POST'])
def dnsSecond():
    print(request.form)
    if request.form['DNS'] == 'autoDNS':
        Net_config().eth1_auto_dns()
        print('autoDNS')
    elif request.form['DNS'] == 'staticDNS':
        defaultDNS = request.form['defaultDNS']
        otherDNS = request.form['otherDNS']
        if otherDNS == '' :
            Net_config().eth1_dns(defaultDNS)
        else :
            Net_config().eth1_dual_dns(defaultDNS,otherDNS)
        print(defaultDNS,otherDNS)
    return redirect('/ipSettingSecond')

@app.route("/iniUpdate")
def iniUpdate():
    file = File_search().ini_list()
    fileList = []
    for i in range(len(file)):
        fileList.append({
            'num':i,
            'name':file[i].split('.')[0],
            'format':(len(file[i].split('.'))==2) and file[i].split('.')[1] or ''
        })
    return render_template('iniUpdate.html',fileList = fileList)

@app.route("/upload",methods=['POST'])
def upload():
    f = request.files['file']
    f.save('/etc/network/'+ secure_filename(f.filename))
    return redirect(url_for('iniUpdate'))

@app.route('/iniSelect')
def iniSelect():
    return render_template('iniSelect.html')

@app.route('/iniBuild')
def iniBuild():
    return render_template('iniBuild.html')

@app.route('/ping')
def ping():
    return render_template('ping.html')

@app.route('/ping',methods=['POST'])
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
    return render_template('logs.html')

@app.route('/sentTest')
def sentTest():
    return render_template('sentTest.html')

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
