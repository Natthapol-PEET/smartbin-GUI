import config
import requests
import json
import base64
from mimetypes import guess_type

def login_uname(uname):
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/login/uname'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = { 'uname': uname }
    res = requests.post(url, headers=headers, data=data, verify=False)

    if 'access_token' in res.text:
        access_token = json.loads(res.text)['access_token']
        return access_token
    else:
        return -1

def decode_token(access_token):
    data = access_token.split('.')[1]
    byte = base64.b64decode(data + '=' * (-len(data) % 4))
    # uname = json.loads(byte)['name'][1:]
    uname = json.loads(byte)['name']

    return uname

def login_qrCode():
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/login/qrcode'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT,
        'Content-Type': 'application/json'
    }

    res = requests.get(url, headers=headers, verify=False)

    # get binary and save image
    fp = open("login_qrCode.png", "wb")
    fp.write(res.content)
    fp.close()

def get_qrcode_accessTK():
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/login/check'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT,
        'Content-Type': 'application/json'
    }

    res = requests.get(url, headers=headers, verify=False)

    # user scan qr-coded
    if 'access_token' in res.text:
        access_token = json.loads(res.text)['access_token']
        return access_token
    # wait user to scan qr-code
    else:
        return -1


def update_bin(canned_cc_cap, pet_cc_cap, plastic_cc_cap, unknown_cc_cap):
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/quantities'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT
    }

    data = { 'data': '0:'+str(canned_cc_cap)+'/1:'+str(pet_cc_cap)+ \
        '/2:'+str(plastic_cc_cap)+'/3:'+str(unknown_cc_cap)+'' }

    requests.post(url, headers=headers, json=data, verify=False)

def report_error():
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/status'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT
    }

    data = {
        "code": 1,  # ถังขยะเต็ม = 1, ถังขยะเสีย = 3
        "message": "ถังขยะเต็มเฉพาะถังที่ 1" # ไม่สามารถเชื่อมต่อกล้องได้, ถังขยะเต็มเฉพาะถังที่ 1
    }

    requests.post(url, headers=headers, json=data, verify=False)

def get_data_type():
    url = 'https://kusesmartbin.csc.ku.ac.th/api/v1/bin/secret/types'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT
    }

    res = requests.get(url, headers=headers, verify=False)
    data = json.loads(res.text)['data']

    # points, names = [], []
    # for x in data:
    #     names.append(x['name'])
    #     points.append(x['points'])
    # return names, points
    return data

def prediction_login(image_name, AccessToken):
    url = 'https://kusesmartbin.csc.ku.ac.th/api/prediction/'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT,
        'Authorization': f'Bearer {AccessToken}'
    }

    image_type = guess_type(image_name)[0]
    files = {'image': (image_name, open(image_name, 'rb'), image_type)}
    res = requests.request('POST', url, files=files, headers=headers, verify=False)

    return res

def prediction_donate(image_name):
    url = 'https://kusesmartbin.csc.ku.ac.th/api/prediction/?mode=donate'
    headers = {
        'X-Bin-ID': config.X_BIN_ID,
        'X-Bin-Client': config.X_BIN_CLIENT,
    }

    image_type = guess_type(image_name)[0]
    files = {'image': (image_name, open(image_name, 'rb'), image_type)}
    res = requests.request('POST', url, files=files, headers=headers, verify=False)
    return res

