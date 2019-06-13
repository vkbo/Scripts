#!/usr/bin/env python3
#
#  Pull Exchange Rates from APIs for Given Date
# ==============================================
#  Author:  Veronica Berglyd Olsen
#  Date:    14.06.2017
#  URL:     https://github.com/vkbo/Scripts
#  License: GPLv3
#  Website: http://vkbo.net
#
#  Usage: ./exhangeRate.py YYYY-MM-DD
#         Date must be >= 2000-01-01
#         If no date, uses today's date
#
#  Supports the cryptocurrencues that cryptocompare tracks and the fiat currencies
#  published by the European Central Bank.
#
#  Available fiat currencies
#  AUD, BGN, BRL, CAD, CHF, CNY, CZK, DKK,
#  GBP, HKD, HRK, HUF, IDR, ILS, INR, JPY,
#  KRW, MXN, MYR, NOK, NZD, PHP, PLN, RON,
#  RUB, SEK, SGD, THB, TRY, USD, ZAR
#

import json, sys

from urllib.request import Request, urlopen
from time import mktime
from datetime import datetime

#  Settings
# ==========

# Which crypto currencies to look up
getCrypto   = ["BTC","XMR","USDT"]

# What currencies (rows) to list against (columns) in the final table
listFinal   = ["CHF","DKK","EUR","GBP","NOK","SEK","USD","USDT","XMR"]
listAgainst = ["CHF","EUR","NOK","GBP","USD","USDT","BTC","XMR"]
listHLCol   = ""
listHLRow   = "NOK"

# Make JSON API Call
def getJSON(apiCall):
    urlReq  = Request(apiCall)
    urlReq.add_header("User-Agent","Mozilla/5.0 (compatible; Python script)")
    urlReq.add_header("Content-Type","application/json")
    urlData = urlopen(urlReq)
    return json.loads(urlData.read().decode())

# Linux Terminal Colours
# No idea if these work on windows
# If not, replace them with empty strings
PURPLE    = "\033[0;35m"
CYAN      = "\033[0;36m"
DARKCYAN  = "\033[0;36m"
BLUE      = "\033[0;34m"
GREEN     = "\033[0;32m"
YELLOW    = "\033[0;33m"
RED       = "\033[0;31m"
BOLD      = "\033[0;1m"
UNDERLINE = "\033[0;4m"
END       = "\033[0;0m"


if len(sys.argv) < 2:
    sDate = datetime.today().strftime("%Y-%m-%d")
else:
    sDate = sys.argv[1]

iDate      = mktime(datetime.strptime(sDate, "%Y-%m-%d").timetuple())
sCryptos   = ",".join(getCrypto)

apiCrypto  = "https://min-api.cryptocompare.com/data/pricehistorical?fsym=EUR&tsyms=%s&ts=%d" % (sCryptos, iDate)
apiFiat    = "http://api.fixer.io/latest?base=EUR&date=%s" % sDate

jsonFiat   = getJSON(apiFiat)
if len(getCrypto) > 0:
    jsonCrypto = getJSON(apiCrypto)

fiatDate   = jsonFiat["date"]
allRates   = jsonFiat["rates"]
for sCrypto in getCrypto:
    allRates[sCrypto] = jsonCrypto["EUR"][sCrypto]

allRates["EUR"] = 1.0

print(BOLD)
print(" Exchange Rates for %s" % sDate)
print(END)

finalTable = " "+BOLD+"Curr"+END+" "
for sAgainst in listAgainst:
    finalTable += ("    "+BOLD+"%-5s"+END+" ") % sAgainst

finalTable += "\n"
finalTable += "="*(len(listAgainst)*10+6)+"\n"

for sFinal in listFinal:
    finalTable += (" "+BOLD+"%-4s"+END+" ") % sFinal
    for sAgainst in listAgainst:
        if sAgainst in allRates.keys() and sFinal in allRates.keys():
            if allRates[sAgainst] > 0:
                thisRate = allRates[sFinal]/allRates[sAgainst]
                if listHLCol == sAgainst or listHLRow == sFinal:
                    finalTable += YELLOW
                if sAgainst in getCrypto:
                    finalTable += " %8.2f " % thisRate
                else:
                    finalTable += " %8.4f " % thisRate
                if listHLCol == sAgainst or listHLRow == sFinal:
                    finalTable += END
            else:
                finalTable += "    "+RED+"N/A"+END+"   "
        else:
            finalTable += "    "+RED+"N/A"+END+"   "
    finalTable += "\n"

finalTable += "="*(len(listAgainst)*10+6)+"\n"
finalTable += " "+BOLD+"Date"+END+" "
for sAgainst in listAgainst:
    if sAgainst in getCrypto:
        exDate = sDate[8:10]+"/"+sDate[5:7]+"/"+sDate[2:4]
    else:
        exDate = fiatDate[8:10]+"/"+fiatDate[5:7]+"/"+fiatDate[2:4]
    finalTable += (" "+GREEN+"%s"+END+" ") % exDate
finalTable += "\n"

print(finalTable)
