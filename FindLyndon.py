__author__ = 't-amirub'
from LyndonTools import *
'''
Algo:
Look at the first word $x\neq(k-1)$.
(1)If (the suffix after x is not a prefix of x):
              Take the smallest rotation - this is $L_i^{r_i}$
(2)Else: (Not clear that this is true)
              Take the suffix.
              Put it in the begging ->Y
              If this is Lyndon, and not expended Lyndon - return Y. ( Claim - if so - this is $L_i$, and $m=0$, $r=1$).
              If not -  use Duval (on Y) to get to the next Lyndon word : $L_{i+1}^{r_{i+1}}$.
'''
def extractL1(w,k):
    #cover the dummy case of (k-1)^n
    if w==str(int(k)-1)*len(w):
        return str(int(k)-1)
    # First case, first letter is not (k-1) m=0. Simply rotate to find L_i^{R_i}
    if w[0] != str(int(k)-1):
        lyndonRotation = findLyndonRotation(w)
        ans = SplitLyndon(lyndonRotation)[0]
        return ans
    # Look at the first word x != (k-1)
    parts = SplitLyndon(w)
    x=''
    for i in range(len(parts)):
        x = parts[i]
        if x != str(int(k)-1):
            # Extract the suffix after it
            suffix = ''.join(parts[i+1:])
            #(1)If (the suffix after x is not a prefix of x)- take the smallest rotation - this is $L_i^{r_i}$
            if (len(x)<len(suffix)) or (x[:len(suffix)] != suffix):
                lyndonRotation = findLyndonRotation(w)
                return SplitLyndon(lyndonRotation)[0]
            #(2)Else, take the suffix. Put it in the begging.
            # If this is Lyndon - return it. ( Claim - if so - this is $L_i$, and $m=0$, $r=1$).
            indexOfSuffix = len(w)-len(suffix)
            rotatedW = w[indexOfSuffix:] + w[:indexOfSuffix]
            if isLyndon(rotatedW) and len(SplitLyndon(rotatedW))==1:
                return rotatedW
            # If not - use Duval (maybe on X?) to get to the next Lyndon word : $L_{i+1}^{r_{i+1}}$
            else:
                nextLyndon = NextLyndon(x,k,len(w))
                return SplitLyndon(nextLyndon)[0]



#Example m != 0
MisNot0 = "123333123333"
#L1 = 123333, r=2
#L2 =     "123333131313"
#rotateMisNot0 = 2 #or 3,4,5

#Example m = 0
Mis0 = "1111311113"
#L1 = 11113, r=2
#L2 = "1111311122"
#rotateMis0= 1,2,3



L1 = "113123223"
r=2
w = L1*r
k="4"
L2=NextLyndon(w,k)


if True:

    if (not isLyndon(L1)) or (not isLyndon(L2)):
        print( "Bad input: L1 and L2 should be Lyndon")
    else:
        if k in L1 or k in L2:
            print( "Bad input- k cannot be in L1 or L2")
        else:
            length = len(L1)
            print("L1: " + L1)
            print ("w: " + w)
            print("L2: " + L2)
            for i in range(length-1):
                w = w[1:]+L2[len(L2)-length+i]
                extracted = extractL1(w,k)
                if extracted != L1 and extracted !=L2:
                    print("WRONG: i:" + str(i+1) +  " word: "+ str(SplitLyndon(w))+" extracted: " +  str(extracted))
            print("ALL DONE")

