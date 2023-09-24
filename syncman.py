# SYNC MANAGER for McvkrDDNS
import json
import requests
Header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'mcv.kr',
    'Referer': 'https://mcv.kr/',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}
Header_DNS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'id=ldw5635; accountstatus=aaa',
    'Host': 'mcv.kr',
    'Referer': 'https://mcv.kr/',
    'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}


def loadConfig():  # 로그인 정보 로드
    with open('./settings.json', 'r', encoding='UTF8') as f:
        settings = json.load(f)
    print("init complete")
    loginData = {
        'action': 'login',
        'ID': settings['account']['mcvkrID'],
        'Password': settings['account']['mcvkrPW'],
    }
    print(f"AcountID: {loginData['ID']}")
    return loginData


def syncNow(loginData, targetIP):  # MCVKR 로그인
    url = 'https://mcv.kr/'
    consoleSession = requests.post(url, data=loginData, headers=Header)
    consoleSession = requests.get(url, headers=Header)
    if consoleSession.status_code == 200:
        print(f'MCVKR Console Login Done {consoleSession.status_code}')
        print(consoleSession.text)
        '''consoleSession = requests.get('https://mcv.kr/dns/')
        print(consoleSession.text)'''
        syncIP(targetIP, consoleSession)
    else:
        print(f'MCVKR Console Login Failed {consoleSession.status_code}')
        exit()


def syncIP(targetIP, consoleSession):  # MCVKR DDNS 동기화
    url = 'https://mcv.kr/dns/pipefilter.php'
    print(f'Sync IP {targetIP}')
    syncData = {
        'serviceupdatedivmode': 'tcp',
        'enabletcp': 'true',
        'serviceupdate-ipaddr': targetIP,
        'serviceupdate-port': '25565',
        'serviceupdate-ipaddr-udp': '1.1.1.1',
        'serviceupdate-port-udp': '8080',
        'serviceupdate': '%EC%8B%9C%EC%8A%A4%ED%85%9C+%EC%97%85%EB%8D%B0%EC%9D%B4%ED%8A%B8'
    }
    consoleSession = requests.post(url, headers=Header, data=syncData)
    if consoleSession.status_code == 200:
        print('MCVKR DDNS Sync Done.')
    else:
        print('MCVKR DDNS Sync Failed.')
        exit()
