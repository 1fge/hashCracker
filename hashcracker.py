import json
import hashlib
import os
import sys
import time
import threading
import multiprocessing

md, sh1, sh256 = [], [], []
unknown_hashtypes = []

with open("config.json") as c:
    config = json.load(c)
    wlpath = config["wordlistpath"]
    hashpath = config["hashlistpath"]

    if not os.path.exists(wlpath) or not os.path.exists(hashpath):
        sys.exit("\nError, please check wordlist or hashlist path in config.json\n")

    with open(hashpath) as h:
        hashes = h.read().splitlines()

def makehash(word, mode):
    word = word.encode("utf-8")

    if mode == 32:
        m = hashlib.md5()
        m.update(word)

    elif mode == 40:
        m = hashlib.sha1()
        m.update(word)

    elif mode == 64:
        m = hashlib.sha256()
        m.update(word)

    return m.hexdigest()

def crackhash(hshlist, wlpath, proclist):

    start = time.time()
    mode = len(hshlist[0])

    with open(wlpath, encoding="utf-8", errors="ignore") as f:
        for word in f:
            word = word.rstrip()

            curhash = makehash(word, mode)

            if curhash in hshlist:
                print(f"{curhash[0:15]}... : {word} ({round(time.time()-start, 2)}s)")
                hshlist.remove(curhash)
    
    if len(hshlist) != 0:
        for hsh in hshlist:
            proclist.append(hsh)
            

for hsh in hashes:

    mode = len(hsh)
    hashtypes = {
                    32: md,
                    40: sh1,
                    64: sh256
                }

    if mode != 32 and mode != 40 and mode != 64:
        unknown_hashtypes.append(hsh)
    else:
        hashtypes[mode].append(hsh)

if __name__ == "__main__":
    with multiprocessing.Manager() as manager:
        px = []
        unsolved_hashes = manager.list()

        if len(md) != 0:
            p = multiprocessing.Process(target=crackhash, args=(md, wlpath, unsolved_hashes,))
            px.append(p)
        if len(sh1) != 0:
            p = multiprocessing.Process(target=crackhash, args=(sh1, wlpath, unsolved_hashes,))
            px.append(p)
        if len(sh256) != 0:
            p = multiprocessing.Process(target=crackhash, args=(sh256, wlpath, unsolved_hashes,))
            px.append(p)
        
        for p in px:
            p.start()
        for p in px:
            p.join()

        if len(unsolved_hashes) != 0:
            print("\n--UNSOLVED HASHES--")
            for us in unsolved_hashes:
                print(us)
        
        if len(unknown_hashtypes) != 0:
            print("\n--UNKNOWN HASH TYPES--")
            for uk in unknown_hashtypes:
                print(uk)


