#!/usr/bin/env python3
#
#  Pull Latest Binance Crypto Rate for a Given Pair
# ==================================================
#  Author:  Veronica Berglyd Olsen
#  Date:    04.04.2018
#  URL:     https://github.com/vkbo/Scripts
#

import json, sys, os, signal
import numpy        as np

from urllib.request import Request, urlopen
from time           import time, sleep
from datetime       import datetime

# Settings
maxHist = 500

# Make JSON API Call
def getJSON(apiCall):
    urlReq = Request(apiCall)
    urlReq.add_header("User-Agent","Mozilla/5.0 (compatible; Python script)")
    urlReq.add_header("Content-Type","application/json")
    urlData = urlopen(urlReq)
    return json.loads(urlData.read().decode())

def signalHandler(signal, frame):
    print("\n\nCtrl+C pressed. Exiting ...")
    sys.exit(0)

signal.signal(signal.SIGINT, signalHandler)

# Linux Terminal Colours
RED       = "\033[0;31m"
GREEN     = "\033[0;32m"
YELLOW    = "\033[0;33m"
BLUE      = "\033[0;34m"
PURPLE    = "\033[0;35m"
CYAN      = "\033[0;36m"
BOLD      = "\033[0;1m"
UNDERLINE = "\033[0;4m"
END       = "\033[0;0m"

if len(sys.argv) < 3:
    print("Error: No currency pair specified")
    exit(1)
else:
    inTemp   = sys.argv[1]
    theCoins = sys.argv[2:]
    inSplit  = inTemp.split("/")
    theWait  = float(inSplit[0])
    if len(inSplit) > 1:
        theTrend = float(inSplit[1])
    else:
        theTrend = theWait*24

theHist = {}
theTime = {}
for theCoin in theCoins:
    if not theCoin == "":
        theHist[theCoin] = []
        theTime[theCoin] = []

tSpan = 0

while True:
    
    toPrint  = "Every %.1f seconds:" % theWait
    toPrint += " "*(65-len(toPrint))
    toPrint += datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')+"\n"
    toPrint += "\n"
    
    for theCoin in theCoins:
        
        if theCoin == "":
            continue
        
        apiCall = "http://api.binance.com/api/v1/ticker/24hr?symbol=%s" % theCoin
        apiJSON = getJSON(apiCall)
        
        theSymbol = apiJSON["symbol"]
        lastPrice = float(apiJSON["lastPrice"])
        lowPrice  = float(apiJSON["lowPrice"])
        highPrice = float(apiJSON["highPrice"])
        openPrice = float(apiJSON["openPrice"])
        change24h = 100*(lastPrice-openPrice)/openPrice
        
        timeNow   = time()
        theHist[theCoin].append(lastPrice)
        theTime[theCoin].append(timeNow)
        
        nHist = len(theHist[theCoin])
        yFit  = (0,0)
        if nHist > 1:
            xTimes = [i for i in theTime[theCoin] if i >= timeNow-theTrend]
            nTimes = len(xTimes)
            xData  = np.linspace(0,theWait*(nTimes-1),nTimes)
            yFit   = np.polyfit(xData,theHist[theCoin][-nTimes:],1)
            tSpan  = timeNow-xTimes[0]
        if nHist > maxHist:
            theHist[theCoin].pop(0)
            theTime[theCoin].pop(0)
        
        if   theSymbol[-3:] == "BTC":
            fmtNum = "%10.8f"
        elif theSymbol[-3:] == "ETH":
            fmtNum = "%10.7f"
        elif theSymbol[-3:] == "BNB":
            fmtNum = "%10.6f"
        elif theSymbol[-4:] == "USDT":
            fmtNum = "%10.4f"
        else:
            fmtNum = "%10.6f"
        
        toPrint += (BOLD+"%-8s: "+END) % theSymbol
        toPrint += (CYAN+fmtNum+" "+END) % lastPrice
        toPrint += (YELLOW+"(L:"+fmtNum+" H:"+fmtNum+" O:"+fmtNum+") "+END) % (lowPrice,highPrice,openPrice)
        if change24h > 0:
            toPrint += (GREEN+"%+7.2f%%"+END) % change24h
        else:
            toPrint += (RED+"%+7.2f%%"+END) % change24h
        toPrint += " [%+7.2f %%/h]" % (360000*yFit[0]/lastPrice)
        
        toPrint += "\n"
    
    toPrint += "\n"
    toPrint += "Trend calculated over %.2f seconds. " % tSpan
    
    os.system("clear")
    print(toPrint)
    sleep(theWait)
        
