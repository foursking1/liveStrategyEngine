from exchangeConnection.jubi.utils import *

def getAccountInfo():
    params = {}
    method = "balance"
    res = send2api(params, method)
    return res

def getTicker():
    params = {"coin": "eth"}
    method = "depth"
    #res = get2api(params, method)
    res = send2api(params, method)
    return res

if __name__ == '__main__':
    print(getAccountInfo())
    print(getTicker())