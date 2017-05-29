__author__ = 't-amirub'
from LyndonTools import *
import copy

k = 4
n = 10

def verifyJandR(l1,l2,window):
    # end cases - this is a lyndon, or it doesnt start with (k-1)
    if isLyndon(window) or window[0] != k-1:
        return [True]
    parts = SplitLyndon(window)
    # Find x_j - the first x which is not s-1
    j=0
    while j < (len(parts)):
        if parts[j][0] != k-1:
            break
        j=j+1
    x = ''.join(str(x) for x in (parts[j]))
    # If the x_{j+1}..{x_k} is NOT a prefix of x_j - nothing to do
    suffix = ''.join((''.join(str(z) for z in x) for x in (parts[j+1:])))
    if (len(x) < len(suffix)) or (x[:len(suffix)] != suffix):
        return [True]
    # Else
    #   if the rotation is NOT Lyndon we have L_i^{r_i-1}v1..vm - nothing to do
    #   else this is a Lyndon, we need to verify that j==r:
    #      -make sure that
    #       a. the suffix is the prefix of l2
    #      AND
    #       b. the prefix is the suffix of l1
    else:
        prefix = ''.join((''.join(str(z) for z in x) for x in (parts[:j])))
        rotated = suffix + prefix + x
        #   if the rotation is NOT Lyndon we have L_i^{r_i-1}v1..vm - nothing to do
        if (not isLyndon(rotated)) or (isExpendedLyndon(rotated)):
            return [True]
        #   else this is a Lyndon, we need to verify that j==r:
        else:
            l2str = ''.join(str(x) for x in l2)
            l1str = ''.join(str(x) for x in l1)
            return [(len(l2str)>=len(suffix)) and (l2str[:len(suffix)] == suffix) and (len(l1str)>=len(prefix)-len(x)) and (l1str[len(l1str) - len(prefix)-len(x):] == prefix + x),prefix,x,suffix,l1str,l2str]

def goOverAllWindows(l1,l2):
    both = l1+l2
    l = len(both)
    for i in range(0,l-n+1):
        yield both[i:(i+n)]

def verifyJandRForAll():
        l1 = []
        l2 = []
        for w in LyndonWordsWithLengthDividingN(k,n):
            l2=copy.deepcopy(w)
            if l1 !=[]:
                for window in goOverAllWindows(l1,l2):
                    JisR = verifyJandR(l1,l2,window)
                    if not JisR[0] :
                        print ("J!=R")
                        print ("l1     " + str(l1))
                        print ("l2     " + str(l2))
                        print ("window " + str(window))
                        print ("prefix " + JisR[1])
                        print ("x      " + JisR[2])
                        print ("suffix " + JisR[3])
                        print ("l1 " + JisR[4])
                        print ("l2 " + JisR[5])
            l1=copy.deepcopy(l2)


verifyJandRForAll()
print (n)
print (k)