# SYNC MANAGER for McvkrDDNS
import json
import requests
initHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Connection": "keep-alive",
    "Host": "mcv.kr",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

beforePayload = {"action": "login"}  # POST 요청 시 보낼 데이터를 이 딕셔너리에 추가하세요.

beforeHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ko-KR,ko;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Content-Length": "12",  # 실제 데이터 길이에 맞게 수정하세요.
    "Content-Type": "application/x-www-form-urlencoded",
    "Host": "mcv.kr",
    "Origin": "https://mcv.kr",
    "Referer": "https://mcv.kr/",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
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
    loginUrl = 'https://mcv.kr/'
    consoleSession = requests.Session()  # 세션 생성
    consoleSession = requests.get(loginUrl, headers=initHeaders)  # 메인페이지 접속
    consoleSession = requests.post(
        loginUrl, headers=beforeHeaders, data=beforePayload, allow_redirects=True)  # 로그인페이지 접속
    consoleSession = requests.post(
        loginUrl, headers=beforeHeaders, data=loginData, allow_redirects=True)  # 로그인 요청
    syncIP(targetIP, consoleSession)


def syncIP(targetIP, consoleSessions):  # MCVKR DDNS 동기화
    pipeUrl = 'https://mcv.kr/dns/pipefilter.php'
    mainUrl = 'https://mcv.kr/dns/'
    print(f'Sync IP {targetIP} start.')
    syncData = {
        'serviceupdatedivmode': 'tcp',
        'enabletcp': 'true',
        'serviceupdate-ipaddr': targetIP,
        'serviceupdate-port': '25565',
        'serviceupdate-ipaddr-udp': '1.1.1.1',
        'serviceupdate-port-udp': '8080',
        'serviceupdate': '시스템 업데이트'
    }
    consoleSession = requests.get(mainUrl, headers=initHeaders)
    consoleSession = requests.get(pipeUrl, headers=initHeaders)
    consoleSession = requests.post(pipeUrl, headers=initHeaders, data=syncData)

    if consoleSession.status_code == 200:
        print('MCVKR DDNS Sync Done.')
    else:
        print('MCVKR DDNS Sync Failed.')
        exit()


print(syncNow(loadConfig(), '39.118.219.109'))
