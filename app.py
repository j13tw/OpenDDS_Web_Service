from flask import Flask, request, render_template, redirect, url_for, abort, jsonify
from werkzeug.utils import secure_filename
from library.Network_config import Net_config, File_search
import subprocess
import json
import os

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
        print(staticIP, staticMask, staticGateway)
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
        if otherDNS == '':
            Net_config().eth0_dns(defaultDNS)
        else:
            Net_config().eth0_dual_dns(defaultDNS, otherDNS)
        print(defaultDNS, otherDNS)
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
        print(staticIP, staticMask, staticGateway)
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
        if otherDNS == '':
            Net_config().eth1_dns(defaultDNS)
        else:
            Net_config().eth1_dual_dns(defaultDNS, otherDNS)
        print(defaultDNS, otherDNS)
    return redirect('/ipSettingSecond')


@app.route("/iniCreate")
def iniCreate():
    return render_template('iniCreate.html')


@app.route("/createFile", methods=['POST'])
def createFile():
    print(request.json)
    data = request.json
    print(data["ini_file_name"])
    try:
        if (data["transport_type"] != "rtps_udp" or data["transport_type"] == "rtps_udp" and data["endpoint_type"] == "default"):
            os.system("cp ./ini/default.ini ./ini/file/" +
                      data["ini_file_name"]+".ini")
            os.system("sed -i '' s:DCPSBit=1/0:DCPSBit=" +
                      data["DCPSBit"]+": ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' s:Scheduler=SCHED_OTHER/SCHED_RR/SCHED_FIFO:Scheduler=" +
                      data["Scheduler"]+": ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' '1,8 s:TTL=1～10:TTL=" +
                      data["discovery_TTL"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' s:transport_type=rtps_udp/tcp/udp:transport_type=" +
                      data["transport_type"]+": ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' '9,14 s:TTL=1～10:TTL=" +
                      data["transportConf_TTL"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
        else:
            if(data["endpoint_type"] == "reader"):
                os.system("cp ./ini/staticReader.ini ./ini/file/" +
                          data["ini_file_name"]+".ini")
            elif(data["endpoint_type"] == "writer"):
                os.system("cp ./ini/staticWriter.ini ./ini/file/" +
                          data["ini_file_name"]+".ini")
            os.system("sed -i '' s:DCPSBit=1/0:DCPSBit=" +
                      data["DCPSBit"]+": ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' s:Scheduler=SCHED_OTHER/SCHED_RR/SCHED_FIFO:Scheduler=" +
                      data["Scheduler"]+": ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' '1,8 s:TTL=1～10:TTL=" +
                      data["discovery_TTL"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' 's:history.kind=KEEP_LAST/KEEP_ALL:history.kind=" +
                      data["history_kind"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' 's:reliability.kind=RELIABLE/BEST_EFFORT:reliability.kind=" +
                      data["reliability_kind"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
            os.system("sed -i '' '24,26 s:TTL=1～10:TTL=" +
                      data["transportConf_TTL"]+":' ./ini/file/" + data["ini_file_name"]+".ini")
        pass
    except:
        return None, 404
        pass
    if os.path.isfile("./ini/file/" + data["ini_file_name"]+".ini"):
        return json.dumps({'success': '建檔成功'}), 200, {'ContentType': 'application/json'}
    else:
        return jsonify({'error': '建檔失敗'}), 400


@app.route("/iniUpdate")
def iniUpdate():
    file = File_search().ini_list()
    fileList = []
    for i in range(len(file)):
        fileList.append({
            'num': i,
            'name': (file[i].split('.')[0] != '') and file[i].split('.')[0] or '.'+file[i].split('.')[1],
            'format': (len(file[i].split('.')) == 2) and ((file[i].split('.')[0] != '') and file[i].split('.')[1] or '特殊檔案') or ''
        })
    return render_template('iniUpdate.html', fileList=fileList)


@app.route("/upload", methods=['POST'])
def upload():
    f = request.files['file']
    f.save('/home/pi/ini/' + secure_filename(f.filename))
    return redirect(url_for('iniUpdate'))


@app.route("/selectFile", methods=['POST'])
def selectFile():
    if not request.json:
        abort(400)
    print(request.json['filename'])
    os.system('echo '+os.getcwd()+'/' +
              request.json['filename']+'> ./db/selectIniPath.txt')
    return redirect(url_for('iniUpdate'))
    # return json.dumps(request.json)


@app.route('/iniSelect')
def iniSelect():
    return render_template('iniSelect.html')


@app.route('/iniBuild')
def iniBuild():
    return render_template('iniBuild.html')


@app.route('/ping')
def ping():
    return render_template('ping.html')


@app.route('/ping', methods=['POST'])
def pings():
    ip = request.form.get('ip')
    try:
        response = subprocess.check_output(
            ['ping', '-c', '1', ip],
            stderr=subprocess.STDOUT,  # get all output
            universal_newlines=True  # return string not bytes
        )
    except:
        response = "From " + ip + " Destination Host Unreachable"
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
