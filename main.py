import sys
import json
import requests

blockTime = ""
blockIndex = 0
secondsPassedFromGenesis = 0
tenMinutesInSeconds = 600
firstBlockInterval = 771

def getBlockTime(blockIndex):
    address = 'https://blockchain.info/block-height/{}?format=json'.format(blockIndex)
    response  = requests.get(address)
    try:
        return(response .json()['blocks'][0]['time'])
    except:
        return 0

def getLastBlock():
    address = 'https://blockchain.info/latestblock'
    response  = requests.get(address)
    lastBlock = {
        "height":response .json()['height'],
        "time": response .json()['time']
    }

    return(lastBlock)

# start index, end index, time to find
# last params are to save a request for each iteration
def binary_search(low, high, x, lowTime, highTime):
    print("    low: {} time: {}, high:{} time: {}, x: {}".format(low, lowTime ,high,highTime, x))

    if highTime > lowTime:
        mid = (high + low) // 2
        midTime = getBlockTime(mid)
        if midTime == x:
            return mid - 1 # if the time is accurate return one block before
        elif midTime > x:
            return binary_search(low, mid - 1, x, lowTime, getBlockTime(mid - 1))
        else:
            return binary_search(mid + 1, high, x, getBlockTime(mid + 1), highTime)
    else:
        if highTime < x:
            return high
        else:
            return high - 1




# MAIN
genesisTime = getBlockTime(0)
lastBlock = getLastBlock()

print()
print()

print("  Please enter block timestamp:", end = " ")

while not isinstance(blockTime, int):
    try:
        blockTime = int(input())
        print()
    except:
        print("  Invalid timestamp, try again:", end = " ")

if blockTime <= genesisTime:
    print("0")
    exit()
if blockTime >= lastBlock['time']:
    print(lastBlock['height'])
    exit()

secondsPassedFromGenesis = (blockTime - genesisTime)
approxIndex = int((secondsPassedFromGenesis / tenMinutesInSeconds) - firstBlockInterval)
approxTime = getBlockTime(approxIndex)

res = ""

if approxTime == blockTime:
    res = approxIndex
elif approxTime > blockTime:
    res = binary_search(0, approxIndex, blockTime, genesisTime, getBlockTime(approxIndex))
elif approxTime < blockTime:
    res = binary_search(approxIndex, lastBlock['height'], blockTime, getBlockTime(approxIndex), lastBlock['time'])

print()
print("  Closest block is {}".format(res))
