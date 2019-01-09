from __future__ import division
DMG = 100
STR = 0
INT = 125
DEX = 0
LUK = 200
crit = 100

a = DMG
b = STR
c = STR
x = crit
y = LUK
z = INT


if __name__ == '__main__':

    print (float(50000*a*x*z + 37500000*a*x + 5000*a*y*z + 3750000*a*y + 10000000000*a\
          + 10*b*c*x*z + 7500*b*c*x + 1*b*c*y*z + 750*b*c*y + 2000000*b*c\
          + 5000*b*x*z + 3750000*b*x + 500*b*y*z + 375000*b*y + 1000000000*b)/(10000000000))

    b = INT
    print (float(50000*a*x*z + 37500000*a*x + 5000*a*y*z + 3750000*a*y + 10000000000*a \
          + 10*b*c*x*z + 7500*b*c*x + 1*b*c*y*z + 750*b*c*y + 2000000*b*c \
          + 5000*b*x*z + 3750000*b*x + 500*b*y*z + 375000*b*y + 1000000000*b)/(10000000000))

    b = DEX
    print (float(50000*a*x*z + 37500000*a*x + 5000*a*y*z + 3750000*a*y + 10000000000*a \
          + 10*b*c*x*z + 7500*b*c*x + 1*b*c*y*z + 750*b*c*y + 2000000*b*c \
          + 5000*b*x*z + 3750000*b*x + 500*b*y*z + 375000*b*y + 1000000000*b)/(10000000000))

    '''
    Every variable is dependent on another one
    Depending on the current build, there will be a different factor of increase for each
    You could assign a value based on how much the total increases
    No matter what, you still need the rest of the stats to give an accurate increase
    But can you find a value/range 
    '''

