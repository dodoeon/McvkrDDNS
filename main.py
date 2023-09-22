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
    global isINIT
    if isINIT == True:  # 최초 실행시
        ipman.savePublicIP(ipman.getPublicIP())  # 실행시 공인 IP 저장
        isINIT = False
        print("init complete")
    else:
        print("init already done")


def sync():
    print("Start Sync Module")
    if ipman.checkIP(ipman.getPublicIP(), ipman.loadStandardIP()) == 1:  # 공인 IP 대조군과 비교
        print("Sync...")
        loginData = syncman.loadConfig()
        syncman.syncIP(loginData, ipman.getPublicIP())
        pass

    else:
        print("Continue...")
        pass


def main():
    sync()
    schedule.every().day.at("04:00:00").do(sync)
    while True:
        schedule.run_pending()
        time.sleep(1)


# main()
syncman.syncNow(syncman.loadConfig(), ipman.getPublicIP())
