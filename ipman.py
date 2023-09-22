# IP MANAGER for McvkrDDNS
import requests
import json
from datetime import datetime


def getPublicIP():  # 공인 IP 로드
    response = requests.get('https://httpbin.org/ip')
    publicIpv4 = response.json()['origin']
    return publicIpv4


def savePublicIP(ipaddr):  # 대조군 설정을 위한 공인 IP 저장
    ipStandardTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'standardTime': ipStandardTime,
        'standardIP': ipaddr
    }
    with open('standardIP.json', 'w') as json_file:
        json.dump(data, json_file)
    print(f'IP Saved {ipaddr}')
    exit()


def loadStandardIP():  # 대조군 설정을 위한 공인 IP 로드
    with open('standardIP.json', 'r') as json_file:
        data = json.load(json_file)
    standardIP = data['standardIP']
    return (standardIP)


def checkIP(publicIP, standardIP):  # 공인 IP 대조군과 비교
    if publicIP == standardIP:
        print(
            f'IP Still {publicIP} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        return False  # IP가 변동이 없으면 False 반환
    else:
        print(
            f'IP changed {standardIP} -> {publicIP} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        savePublicIP(publicIP)
        return True  # IP가 변동이 있으면 True 반환
