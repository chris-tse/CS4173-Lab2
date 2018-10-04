#! /usr/bin/python3

import os
import sys
import binascii

iv = '09080706050403020100A2B2C2D2E2F2'
targetciphertext = 'd06bf9d0dab8e8ef880660d2af65aa82'

keys = [line.rstrip('\n') for line in open('keys.txt')]
trial = 1
for key in keys:
    print('Trial #' + str(trial))
    os.system('openssl enc -aes-128-cbc -e -in p.bin -out cipher.bin -K ' + key + ' -iv ' + iv)
    with open('cipher.bin', 'rb') as f:
        content = f.read()
    result = binascii.hexlify(content).decode('utf-8')
    print('Results in ' + result[0:len(targetciphertext)])
    if result[0:len(targetciphertext)] == targetciphertext:
        print('')
        print('Success!')
        print('Key:       ' + key)
        print('Results in ' + result[0:len(targetciphertext)])
        print('Target:    ' + targetciphertext)
        sys.exit(0)
    else:
        os.system('rm cipher.bin')
    i = i + 1

print('No match found')