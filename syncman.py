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
    url = 'https://mcv.kr/dns/pipefilter.php'
    syncData = {
        'serviceupdatedivmode': 'tcp',
        'enabletcp': 'true',
        'serviceupdate-ipaddr': targetIP,
        'serviceupdate-port': '25565',
        'serviceupdate-ipaddr-udp': '1.1.1.1',
        'serviceupdate-port-udp': '8080',
        'serviceupdate': '%EC%8B%9C%EC%8A%A4%ED%85%9C+%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8'
    }
    ddnsSession = requests.post(url, data=syncData)
    if ddnsSession.status_code == 200:
        print('MCVKR DDNS Sync Done.')
    else:
        print('MCVKR DDNS Sync Failed.')
        exit()
