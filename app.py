from flask import Flask, request, render_template, redirect, url_for, abort, jsonify
from werkzeug.utils import secure_filename
from library.Network_config import Net_config, File_search, Time_config, Gps_time, Ntp_config, Watchdog_config, Reboot_system
from library.getLog import get, main
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
            os.system("cp ./ini/default.ini /home/pi/ini/" +
                      data["ini_file_name"]+".ini")
            os.system("sed -i s:DCPSBit=1/0:DCPSBit=" +
                      data["DCPSBit"]+": /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i s:Scheduler=SCHED_OTHER/SCHED_RR/SCHED_FIFO:Scheduler=" +
                      data["Scheduler"]+": /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i '1,8 s:TTL=1～10:TTL=" +
                      data["discovery_TTL"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i s:transport_type=rtps_udp/tcp/udp:transport_type=" +
                      data["transport_type"]+": /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i '9,14 s:TTL=1～10:TTL=" +
                      data["transportConf_TTL"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
        else:
            if(data["endpoint_type"] == "reader"):
                os.system("cp ./ini/staticReader.ini /home/pi/ini/" +
                          data["ini_file_name"]+".ini")
            elif(data["endpoint_type"] == "writer"):
                os.system("cp ./ini/staticWriter.ini /home/pi/ini/" +
                          data["ini_file_name"]+".ini")
            os.system("sed -i s:DCPSBit=1/0:DCPSBit=" +
                      data["DCPSBit"]+": /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i s:Scheduler=SCHED_OTHER/SCHED_RR/SCHED_FIFO:Scheduler=" +
                      data["Scheduler"]+": /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i '1,8 s:TTL=1～10:TTL=" +
                      data["discovery_TTL"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i 's:history.kind=KEEP_LAST/KEEP_ALL:history.kind=" +
                      data["history_kind"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i 's:reliability.kind=RELIABLE/BEST_EFFORT:reliability.kind=" +
                      data["reliability_kind"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
            os.system("sed -i '24,26 s:TTL=1～10:TTL=" +
                      data["transportConf_TTL"]+":' /home/pi/ini/" + data["ini_file_name"]+".ini")
        pass
    except:
        return None, 404
        pass
    if os.path.isfile("/home/pi/ini/" + data["ini_file_name"]+".ini"):
        return json.dumps({'success': '建檔成功'}), 200, {'ContentType': 'application/json'}
    else:
        return json.dumps({'error': '建檔失敗'}), 400


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
    f.save('/Users/liwensheng/Documents/python/flask_dds/ini/file/' +
           secure_filename(f.filename))
    return redirect(url_for('iniUpdate'))


@app.route("/deleteFile", methods=['POST'])
def deleteFile():
    if not request.json:
        return abort(400)
    else:
        print(request.json['filename'])
        try:
            os.system(
                'rm -r /home/pi/ini/' + request.json['filename'])
            return json.dumps(request.json)
        except:
            return abort(400)


# @app.route('/iniSelect')
# def iniSelect():
#     return render_template('iniSelect.html')


# @app.route('/iniBuild')
# def iniBuild():
#     return render_template('iniBuild.html')


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
    print(main())
    data = main()
    return render_template('logs.html', data=data)


@app.route('/logsData', methods=['POST'])
def logsData():
    print(main())
    return jsonify({'pubLogs': get(choose="pub"), 'subLogs': get(choose="sub")})


@app.route('/sendTest')
def sendTest():
    file = File_search().ini_list()
    print(file)
    fileList = ['rtps.ini']
    for i in range(len(file)):
        if (len(file[i].split('.')) == 2 and file[i].split('.')[1] == 'ini'):
            fileList.append(file[i])
    return render_template('sendTest.html', fileList=fileList)


@app.route('/rpiSetting')
def rpiSetting():
    nowTime = Time_config().get_now()
    status = Watchdog_config().watchdog_status()
    print(status)
    # nowTime = 123
    # status = [1, 2, 3, 4, 5, 6, 7]
    return render_template('rpiSetting.html', nowTime=nowTime, ntpVal='TIME.google.com', watchDogVal1=(status[0] == 'Enable' and status[1] or status[0]), watchDogVal5=(status[2] == 'Enable' and status[3] or status[2]), watchDogVal15=(status[4] == 'Enable' and status[5] or status[4]), watchDogValTemp=status[6])


@app.route('/setRpiTime', methods=['POST'])
def setRpiTime():
    if not request.json:
        return abort(400)
    else:
        dateMethod = request.json['dateMethod']
        if dateMethod == 'manual':
            date = request.json['date']
            time = request.json['time']
            print(dateMethod, date.split('-'), time.split(':'))
            # return jsonify({'status': 'ok'})
            try:
                setDateStatus = Time_config().date_set(date.split(
                    '-')[0], date.split('-')[1], date.split('-')[2])
                print('date_set', date.split('-')
                      [0], date.split('-')[1], date.split('-')[2])
                setTimeStatus = Time_config().time_set(
                    time.split(':')[0], time.split(':')[1], '0')
                print('time_set', time.split(':')[0], time.split(':')[1], '0')
                if setDateStatus == 'OK' and setTimeStatus == 'OK':
                    return jsonify({'status': 'ok'})
                else:
                    return abort(400)
            except:
                return abort(400)
        elif dateMethod == 'gps':
            print(dateMethod)
            gps = Gps_time().get_time()
            if gps == 'OK':
                return jsonify({'status': 'ok'})
            elif gps == 'GPS Pending':
                return jsonify({'status': 'GPS Pending'})
            else:
                return abort(400)
        elif dateMethod == 'ntp':
            ntp_host = request.json['ntp']
            print(dateMethod, ntp_host)
            ntp = Ntp_config().ntp_set(ntp_host)
            if ntp == 'OK':
                return jsonify({'status': 'ok'})
            else:
                return abort(400)
        return abort(404)


@app.route('/setWatchDog1', methods=['POST'])
def setWatchDog1():
    if not request.json:
        return abort(400)
    else:
        try:
            setWatchDogVal1 = request.json['setWatchDogVal1']
            if int(setWatchDogVal1) >= 24 and int(setWatchDogVal1) <= 100:
                status = Watchdog_config().set_cpu_load_short(setWatchDogVal1)
                print(setWatchDogVal1, status)
                return jsonify({'status': status})
            else:
                return jsonify({'status': '輸入值請在指定範圍內'})
        except:
            return abort(400)


@app.route('/watchDogCancel1', methods=['POST'])
def setWatchDogCancel1():
    if not request.json:
        return abort(400)
    else:
        try:
            statusVal = request.json['status']
            status = Watchdog_config().remove_cpu_load_short()
            print(statusVal, status)
            return jsonify({'status': status})
        except:
            return abort(400)


@app.route('/setWatchDog5', methods=['POST'])
def setWatchDog5():
    print(1)
    if not request.json:
        print(2)
        return abort(400)
    else:
        print(3)
        try:
            print(4)
            setWatchDogVal5 = request.json['setWatchDogVal5']
            print(type(setWatchDogVal5))
            if int(setWatchDogVal5) >= 20 and int(setWatchDogVal5) <= 100:
                # print(type(setWatchDogVal5), setWatchDogVal5)
                status = Watchdog_config().set_cpu_load_middle(setWatchDogVal5)
                print(status)
                return jsonify({'status': status})
            else:
                return jsonify({'status': '輸入值請在指定範圍內'})
        except:
            return abort(400)


@app.route('/watchDogCancel5', methods=['POST'])
def setWatchDogCancel5():
    if not request.json:
        return abort(400)
    else:
        try:
            statusVal = request.json['status']
            status = Watchdog_config().remove_cpu_load_middle()
            print(statusVal, status)
            return jsonify({'status': status})
        except:
            return abort(400)


@app.route('/setWatchDog15', methods=['POST'])
def setWatchDog15():
    if not request.json:
        return abort(400)
    else:
        try:
            setWatchDogVal15 = request.json['setWatchDogVal15']
            if int(setWatchDogVal15) >= 20 and int(setWatchDogVal15) <= 100:
                status = Watchdog_config().set_cpu_load_long(setWatchDogVal15)
                print(setWatchDogVal15, status)
                return jsonify({'status': status})
            else:
                return jsonify({'status': '輸入值請在指定範圍內'})
        except:
            return abort(400)


@app.route('/watchDogCancel15', methods=['POST'])
def setWatchDogCancel15():
    if not request.json:
        return abort(400)
    else:
        try:
            statusVal = request.json['status']
            status = Watchdog_config().remove_cpu_load_long()
            print(statusVal, status)
            return jsonify({'status': status})
        except:
            return abort(400)


@app.route('/setWatchDogTemp', methods=['POST'])
def setWatchDogTemp():
    if not request.json:
        return abort(400)
    else:
        try:
            setWatchDogValTemp = request.json['setWatchDogValTemp']
            if int(setWatchDogValTemp) >= 40 and int(setWatchDogValTemp) <= 100:
                status = Watchdog_config().set_cpu_temperature(setWatchDogValTemp)
                print(setWatchDogValTemp, status)
                return jsonify({'status': status})
            else:
                return jsonify({'status': '輸入值請在指定範圍內'})
        except:
            return abort(400)


@app.route('/reboot', methods=['POST'])
def reboot():
    try:
        Reboot_system().reboot()
        return jsonify({'status': '成功'})
    except:
        return abort(400)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0', port=5000, debug=True)
