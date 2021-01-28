with open("words.txt", "r") as f:
    wordlist = f.read().splitlines()

# t = [i for i in wordlist if i.isupper()]
# print (t)

import os
os.mkdir("a")