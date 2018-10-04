# CS 4173 Lab 2
#### Pseudo Random Number Generation Lab

## Prerequisites
Versions of software used listed here:
- Environment: Ubuntu 16.04.4 LTS
- Python: 3.5.2
- `gcc`: 5.4.0
- `make`: 4.1
- `diff`: 3.3

## Task 1: Generate Encryption Key in a Wrong Way

In this task, we observe the functionality of pseudo-random number generators. By running the code to generate a 128-bit key as given, we see two outputs: the first is the current Unix timestamp and the second is the resulting randomly generated key. Running this several times allows one to observe the time incrementing every second. However, after commenting out the indicated line, we see the same two outputs, but this time the generated key stays the same no matter how many times the program is run.

The reason lies in the purpose of `srand()` and `time()`. By running `time(NULL)` we can obtain the current Unix timestamp, which will be different every time the program is run (in one second intervals). By using `srand()` we can seed the random number generator such that it will generate a different sequence of numbers. Random number generators are not truly random, only pseudo-random, and are affected by the seed value. For a particular seed value, the random number sequence generated will be exactly the same. In this case, we use the current Unix timestamp as the seed, meaning the key generated will be unique since time can only be incremented.

## Task 2: Guessing the Key 

In this task, we will guess the key used to encrypt the given plaintext into the given ciphertext. We are given many tools in order to guess the key. The first is the `date` utility. We can use this to determine the seed used to generate the key. Since each seed determines the random number sequence, it effectively determines the key. Since we know the time of the file creation `2018-04-17 23:08:49` and the beginning of the two-hour window `2018-04-17 21:08:49`, we can use this to find the range of seed values used with the date utility: 

```bash
$ date -d "2018-04-17 21:08:49" +%s
1524017329
$ date -d "2018-04-17 23:08:49" +%s
1524024529
```

The difference is 7200, which is the number of seconds in two hours. Now we can use these values to generate all the possible keys that could have resulted in this 7200-second range. See source code in `keygen.c`. Source code can be run and executed as such:

```bash
$ make keygen
$ ./keygen
```

This will generate a file called `keys.txt` which contains one key per line. Now we can use the code in `trialencrypt.py` to loop through each key that was generated in the previous step and compare whether the first 128 bits of the resulting key is the same as the specified target ciphertext. We first write the plaintext as binary to a `p.bin` file:

```py
$ python3
>>> plain = '255044462d312e350a25d0d4c5d80a34'
>>> # Split into chunks of 2 digits
>>> bytearr = [plain[i:i+2] for i in range(0, len(plain), 2)]
>>> # Parse into decimal ints
>>> bytelist = [int(x, 16) for x in bytearr]
>>> f = open('p.bin', 'wb')
>>> f.write(bytes(bytelist))
```

Then we can run our script:

```
$ ./trialencrypt.py
Trial #1
Results in 43c300208414f46ba95f10bcaedfc939
Trial #2
Results in 2962fc5a7082604de13217195d738698
...
Trial #367
Results in d06bf9d0dab8e8ef880660d2af65aa82

Success!
Key:       95fa2030e73ed3f8da761b4eb805dfd7
Results in d06bf9d0dab8e8ef880660d2af65aa82
Target:    d06bf9d0dab8e8ef880660d2af65aa82
```

Therefore, we can presume that the key used by Alice is `95fa2030e73ed3f8da761b4eb805dfd7` and should be able to be used to decrypt the rest of the file. We can verify by running the reverse:

```
$ openssl enc -aes-128-cbc -d -in cipher.bin -out p2.bin \ 
    -K 95fa2030e73ed3f8da761b4eb805dfd7 \
    -iv 09080706050403020100A2B2C2D2E2F2
$ diff p.bin p2.bin
$
```

A lack of output from `diff` confirms that the original `p.bin` and the decrypted `p2.bin` are the same. 