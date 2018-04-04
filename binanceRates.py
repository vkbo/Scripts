#!/usr/bin/env python3
#
#  Pull Latest Binance Crypto Rate for a Given Pair
# ==================================================
#  Author:  Veronica Berglyd Olsen
#  Date:    04.04.2018
#  URL:     https://github.com/Jadzia626/Scripts
#

import json, sys

from urllib.request import Request, urlopen
from time import mktime
from datetime import datetime

#  Settings
# ==========

# Which crypto currencies to look up
getCrypto   = ["BTC","XMR"]

# What currencies (rows) to list against (columns) in the final table
listFinal   = ["CHF","DKK","EUR","GBP","NOK","SEK","USD","XMR"]
listAgainst = ["CHF","EUR","NOK","GBP","USD","BTC","XMR"]
listHLCol   = ""
listHLRow   = "NOK"

# Make JSON API Call
def getJSON(apiCall):
    urlReq = Request(apiCall)
    urlReq.add_header("User-Agent","Mozilla/5.0 (compatible; Python script)")
    urlReq.add_header("Content-Type","application/json")
    urlData = urlopen(urlReq)
    return json.loads(urlData.read().decode())

# Linux Terminal Colours
# No idea if these work on windows
# If not, replace them with empty strings
RED       = "\033[0;31m"
GREEN     = "\033[0;32m"
YELLOW    = "\033[0;33m"
BLUE      = "\033[0;34m"
PURPLE    = "\033[0;35m"
CYAN      = "\033[0;36m"
BOLD      = "\033[0;1m"
UNDERLINE = "\033[0;4m"
END       = "\033[0;0m"


if len(sys.argv) < 2:
    print("Error: No currency pair specified")
    exit(1)
else:
    theCoins = sys.argv[1:]

for theCoin in theCoins:
    if theCoin == "":
        continue
    apiCall = "http://api.binance.com/api/v1/ticker/24hr?symbol=%s" % theCoin
    apiJSON = getJSON(apiCall)
    
    lastPrice = float(apiJSON["lastPrice"])
    lowPrice  = float(apiJSON["lowPrice"])
    highPrice = float(apiJSON["highPrice"])
    change24h = 100*(lastPrice-lowPrice)/lowPrice
    
    toPrint  = (BOLD+"%-8s: "+END) % apiJSON["symbol"]
    toPrint += (CYAN+"%14.8f "+END) % lastPrice
    toPrint += (YELLOW+"(%14.8f - %14.8f) "+END) % (lowPrice,highPrice)
    if change24h > 0:
        toPrint += (GREEN+"%7.2f%%"+END) % change24h
    else:
        toPrint += (RED+"%7.2f%%"+END) % change24h
    print(toPrint)
