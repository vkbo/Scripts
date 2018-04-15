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

def signalHandler(theSignal, theFrame):
    print("\nExiting ...")
    sys.exit(0)

def stringToSeconds(timeString):
    if len(timeString) >= 2:
        if   timeString[-1] == "s":
            return float(timeString[:-1])
        elif timeString[-1] == "m":
            return float(timeString[:-1])*60
        elif timeString[-1] == "h":
            return float(timeString[:-1])*3600
    print("Error: Could not parse time string '%s'" % timeString)
    print("       Format is 00s, 00m or 00h")
    sys.exit(0)
    return

# Capture ctrl+c
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

# Get initial info
okPairs = {}
apiCall = "https://api.binance.com/api/v1/exchangeInfo"
apiJSON = getJSON(apiCall)
for exPair in apiJSON["symbols"]:
    okPairs[exPair["symbol"]] = exPair["quoteAsset"]

if len(sys.argv) < 3:
    print("Error: No currency pair specified")
    print("Usage: %s [interval]/[trend] PAIR1 PAIR2 ..." % os.path.basename(sys.argv[0]))
    print("       %s [interval]/[trend] pairFile.dat"    % os.path.basename(sys.argv[0]))
    print("Where: [interval] is the refresh time in units of s, m or h. E.g. 10s")
    print("       [trend]    is optionally the time to calculate hourly trends over, in units of s, m or h.")
    print("       PAIR1...n  are the exchange pairs. See Binance exchange for valid pairs.")
    print("       Alternatively, a file of pairs to monitor that will be read every cycle.")
    sys.exit(1)

theFile  = sys.argv[2]
theCoins = sys.argv[2:]
useFile  = os.path.isfile(theFile)
inTemp   = sys.argv[1]
inSplit  = inTemp.split("/")
theWait  = stringToSeconds(inSplit[0])
if len(inSplit) > 1:
    theTrend = stringToSeconds(inSplit[1])+0.49*theWait
else:
    theTrend = theWait*24

if theTrend/theWait > maxHist:
    maxHist = round(theTrend/theWait)+10

theHist = {}
theTime = {}

tSpan = 0
wLen  = 86

while True:
    
    toPrint  = "Every %.1f seconds:" % theWait
    toPrint += " "*(wLen-len(toPrint)-19)
    toPrint += datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')+"\n"
    toPrint += "\n"
    
    if useFile:
        theCoins = []
        with open(theFile,mode="r") as inFile:
            for inLine in inFile:
                inLine = inLine.strip()
                if len(inLine) < 5:  continue
                if inLine[0] == "#": continue
                theCoins.append(inLine)
    
    for theCoin in theCoins:
        
        if theCoin == "":
            continue
        
        if theCoin not in okPairs.keys():
            toPrint += (BOLD+"%-8s: "+END) % theCoin
            toPrint += RED+"Invalid trading pair"+END+"\n"
            continue
        
        if not theCoin in theHist.keys():
            theHist[theCoin] = []
            theTime[theCoin] = []
        
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
            yFit   = np.polyfit(theTime[theCoin][-nTimes:],theHist[theCoin][-nTimes:],1)
            tSpan  = timeNow-xTimes[0]
        if nHist > maxHist:
            theHist[theCoin].pop(0)
            theTime[theCoin].pop(0)
        
        if   okPairs[theCoin] == "BTC":
            fmtNum = "%10.8f"
        elif okPairs[theCoin] == "ETH":
            fmtNum = "%10.7f"
        elif okPairs[theCoin] == "BNB":
            fmtNum = "%10.6f"
        elif okPairs[theCoin] == "USDT":
            fmtNum = "%10.4f"
        else:
            fmtNum = "%10.6f"
        
        toPrint += (BOLD+"%-8s: "+END) % theSymbol
        toPrint += (CYAN+fmtNum+" "+END) % lastPrice
        toPrint += (YELLOW+"(L:"+fmtNum+" H:"+fmtNum+" O:"+fmtNum+") "+END) % (lowPrice,highPrice,openPrice)
        if change24h < 0:
            toPrint += (RED+"%+7.2f%%"+END)   % change24h
        else:
            toPrint += (GREEN+"%+7.2f%%"+END) % change24h
        
        hTrend = 360000*yFit[0]/lastPrice
        if hTrend < 0:
            toPrint += (RED+"  [T:%+6.2f %%/h]"+END)   % hTrend
        elif hTrend < 100.0:
            toPrint += (GREEN+"  [T:%+6.2f %%/h]"+END) % hTrend
        else:
            toPrint += (GREEN+"  [T:>99.99%/h]"+END)
        
        toPrint += "\n"
    
    toPrint += "\n"
    prTrend  = "Trend calculated over %.2f minutes" % (tSpan/60)
    
    # Calculate sleep time
    if nHist > 1:
        actTime  = theTime[theCoin][-1]-theTime[theCoin][0]
        wantTime = theWait*(nHist-1)
        diffTime = wantTime-actTime
        toWait   = theWait+diffTime
        if toWait < 0:
            toWait = 0.5
        prTime   = "Avg. Time: %.2f seconds" % (actTime/(nHist-1))
    else:
        prTime = ""
        toWait = theWait
    
    toPrint += prTrend+(" "*(wLen-len(prTrend)-len(prTime)))+prTime
    
    print("\033[H\033[J",end="")
    sys.stdout.flush()
    print(toPrint)
    sys.stdout.flush()
    sleep(toWait)
