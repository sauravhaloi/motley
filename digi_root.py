#!/usr/bin/env python

__author__ = 'saurav'

""" 
 Program to find the digital root of a number
 http://en.wikipedia.org/wiki/Digital_root
 Digital Root can be used as a poor man's crude hashing techniques
"""

import sys

input_num = 0


def got_two_more(digi_root):
    global input_num
    quotient = digi_root
    digi_root = (quotient / 10) + (quotient % 10)
    # print digi_root, quotient

    if len(str(digi_root)) == 2:
        got_two_more(digi_root)
    else:
        print 'The digital root of ' + str(input_num) + ' is: ' + str(digi_root)


def main():
    global input_num
    input_num = sys.argv[1]
    length = len(str(input_num))

    digi_root = 0
    quotient = int(input_num)

    for i in xrange(length):
        digi_root += quotient % 10
        tmp_quotient = quotient / 10
        quotient = tmp_quotient
        #print digi_root, quotient

    if len(str(digi_root)) == 2:
        got_two_more(digi_root)
    else:
        print 'The digital root of ' + str(input_num) + ' is: ' + str(digi_root)

if __name__ == "__main__":
    main()
	
	
