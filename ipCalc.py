#!/usr/bin/env python

import sys

# Process Input

if len(sys.argv) == 1:
    print "Error: Please provide an IP address."
    sys.exit(0)

aIn = sys.argv[1].split("/")
aIP = aIn[0].split(".")

if len(aIP) != 4:
    print "Error: Not a valid IP address."
    sys.exit(0)

for i in range(4):
    if not aIP[i].isdigit():
        print "Error: Not a valid IP address."
        sys.exit(0)
    else:
        aIP[i] = int(aIP[i])

if len(aIn) > 1:
    iMask = int(aIn[1])
else:
    iMask = 24

# Functions

def fBin2IP(iIn):
    sT = "{0:032b}".format(iIn)
    return "{0:d}.{1:d}.{2:d}.{3:d}".format(int(sT[0:8],2),int(sT[8:16],2),int(sT[16:24],2),int(sT[24:32],2))
    
def fFormatBin(iIn):
    sT = "{0:032b}".format(iIn)
    return " ".join((sT[0:8],sT[8:16],sT[16:24],sT[24:32]))
    
# Calculate Values

iIP = aIP[0]*256**3 + aIP[1]*256**2 + aIP[2]*256 + aIP[3]
iNM = int("1"*iMask + "0"*(32-iMask), 2)
iWC = int("0"*iMask + "1"*(32-iMask), 2)
iNW = iIP & iNM
iBC = iIP | iWC

# Print

print ""
print "Address:    {0:15} => {1:35}".format(fBin2IP(iIP), fFormatBin(iIP))
print "Netmask:    {0:15} => {1:35}".format(fBin2IP(iNM), fFormatBin(iNM))
print "Wildcard:   {0:15} => {1:35}".format(fBin2IP(iWC), fFormatBin(iWC))
print "Network:    {0:15} => {1:35}".format(fBin2IP(iNW), fFormatBin(iNW))
print "Broadcast:  {0:15} => {1:35}".format(fBin2IP(iBC), fFormatBin(iBC))
print ""
