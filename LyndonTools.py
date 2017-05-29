__author__ = 't-amirub'

"""
From https://www.ics.uci.edu/~eppstein/PADS/Lyndon.py
Algorithms on strings and sequences based on Lyndon words.
David Eppstein, October 2011."""

import unittest

def LengthLimitedLyndonWords(s,n):
    """Generate nonempty Lyndon words of length <= n over an s-symbol alphabet.
    The words are generated in lexicographic order, using an algorithm from
    J.-P. Duval, Theor. Comput. Sci. 1988, doi:10.1016/0304-3975(88)90113-2.
    As shown by Berstel and Pocchiola, it takes constant average time
    per generated word."""
    w = [-1]                            # set up for first increment
    while w:
        w[-1] += 1                      # increment the last non-z symbol
        yield w
        m = len(w)
        while len(w) < n:               # repeat word to fill exactly n syms
            w.append(w[-m])
        while w and w[-1] == s - 1:     # delete trailing z's
            w.pop()

def LyndonWordsWithLength(s,n):
    """Generate Lyndon words of length exactly n over an s-symbol alphabet.
    Since nearly half of the outputs of LengthLimitedLyndonWords(s,n)
    have the desired length, it again takes constant average time per word."""
    if n == 0:
        yield []    # the empty word is a special case not handled by main alg
    for w in LengthLimitedLyndonWords(s,n):
        if len(w) == n:
            yield w

def LyndonWordsWithLengthDividingN(s,n):
    """Generate Lyndon words of length exactly n over an s-symbol alphabet.
    Since nearly half of the outputs of LengthLimitedLyndonWords(s,n)
    have the desired length, it again takes constant average time per word."""
    if n == 0:
        yield []    # the empty word is a special case not handled by main alg
    for w in LengthLimitedLyndonWords(s,n):
        if n % len(w) == 0:
            yield w


def LyndonWords(s):
    """Generate all Lyndon words over an s-symbol alphabet.
    The generation order is by length, then lexicographic within each length."""
    n = 0
    while True:
        for w in LyndonWordsWithLength(s,n):
            yield w
        n += 1

def DeBruijnSequence(s,n):
    """Generate a De Bruijn sequence for words of length n over s symbols
    by concatenating together in lexicographic order the Lyndon words
    whose lengths divide n. The output length will be s^n.
    Because nearly half of the generated sequences will have length
    exactly n, the algorithm will take O(s^n/n) steps, and the bulk
    of the time will be spent in sequence concatenation."""

    output = []
    for w in LengthLimitedLyndonWords(s,n):
        if n % len(w) == 0:
            output += w
    return output


def rotate(s,n):
    return s[n:] + s[:n]

def isLyndon(s):
    for i in range(len(s)):
        if s>rotate(s,i):
            return False
    return True

def isExpendedLyndon(s):
    return isLyndon(s) and len(SplitLyndon(s))==1

def ChenFoxLyndonBreakpoints(s):
    """Find starting positions of Chen-Fox-Lyndon decomposition of s.
    The decomposition is a set of Lyndon words that start at 0 and
    continue until the next position. 0 itself is not output, but
    the final breakpoint at the end of s is. The argument s must be
    of a type that can be indexed (e.g. a list, tuple, or string).
    The algorithm follows Duval, J. Algorithms 1983, but uses 0-based
    indexing rather than Duval's choice of 1-based indexing."""
    k = 0
    while k < len(s):
        i,j = k,k+1
        while j < len(s) and s[i] <= s[j]:
            i = (s[i] == s[j]) and i+1 or k     # Python cond?yes:no syntax
            j += 1
        while k < i+1:
            k += j-i
            yield k

def SplitLyndon(s):
    """Decompose s into Lyndon words according to the Chen-Fox-Lyndon theorem.
    The arguments are the same as for ChenFoxLyndonBreakpoints but the
    return values are subsequences of s rather than indices of breakpoints."""
    old = 0
    ans=[]
    for k in ChenFoxLyndonBreakpoints(s):
        ans.append(s[old:k])
        old = k
    return ans

def findLyndonRotation(w):
    ans = w
    for i in range(len(w)):
        if ans>rotate(w,i):
            ans =  rotate(w,i)
    return ans

def findNextChunk(w,k,bitsToMove):
    k_1 = str(int(k)-1)
    chunk = w[:bitsToMove]
    while True:
        if len(chunk)==0:
            break
        if chunk[len(chunk)-1] == k_1:
            chunk = chunk[:len(chunk)-1] # Should be -1?
        else:
            break
    chunk = chunk[:len(chunk)-1] + str(int(chunk[len(chunk)-1])+1)
    return chunk

'''
Takes a N-long Lyndon word and return the next Lyndon word with length N
'''
def NextLyndon(w,k,bitsToMove=-1):
    if (not isLyndon(w)):
        print ("Not a lyndon word: "+w)
        return
    if bitsToMove==-1:
        bitsToMove=len(w)
    ans = ''
    while bitsToMove>0:
        chunk = findNextChunk(w,k,bitsToMove)
        bitsToMove = bitsToMove-len(chunk)
        ans = ans + chunk
    return ans

