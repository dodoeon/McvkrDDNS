# SYNC MANAGER for McvkrDDNS
import json
import requests


def loadConfig():  # 로그인 정보 로드
    with open('./config.json', 'r', encoding='UTF8') as f:
        settings = json.load(f)
    print("init complete")
    loginData = {
        'action': 'login',
        'ID': settings['account']['mcvkrID'],
        'Password': settings['account']['mcvkrPW'],
    }
    print(f"AcountID: {loginData['ID']}")
    return loginData


def login(loginData):  # MCVKR 로그인
    url = 'https://mcv.kr/'
    consoleSession = requests.post(url, data=loginData)
    if consoleSession.status_code == 302:
        print('MCVKR Console Login Done.')
    else:
        print('MCVKR Console Login Failed.')
        exit()


def syncIP(targetIP):  # MCVKR DDNS 동기화
    url = 'https://mcv.kr/api/ddns'
    ddnsData = {
        'action': 'update',
        'ip': targetIP
    }
    ddnsSession = requests.post(url, data=ddnsData)
    if ddnsSession.status_code == 200:
        print('MCVKR DDNS Sync Done.')
    else:
        print('MCVKR DDNS Sync Failed.')
        exit()
