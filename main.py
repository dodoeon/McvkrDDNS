# MCVKR Pipefilter ip DDNS Client
import requests
import json
from datetime import datetime
import ipman
import syncman
import schedule
import time

isINIT = True


def init():
    if isINIT == True:  # 최초 실행시

        loginData = syncman.loadConfig()  # 로그인 정보 로드
        ipman.savePublicIP(ipman.getPublicIP())  # 실행시 공인 IP 저장
        isINIT = False
        print("init complete")
    else:
        print("init already done")


def sync():
    print("Start Sync")
    nowIP = ipman.getPublicIP()  # 공인 IP 로드
    if ipman.checkIP(nowIP, ipman.loadStandardIP):  # 공인 IP 대조군과 비교
        syncman.login(syncman.loginConfig)  # MCVKR 로그인
        syncman.syncIP(nowIP)  # MCVKR DDNS 동기화
    else:
        print("Continue")


init()  # Initialization

schedule.every().day.at("04:00:00").do(sync)  # 오전 4시에 동기화 작업 실행

while True:
    schedule.run_pending()
    time.sleep(1)
