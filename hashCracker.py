import json
import hashlib
import os
import sys
import time
import multiprocessing as mp

with open("config.json") as c:
    config = json.load(c)
    wlpath = config["wordlistpath"]
    hashpath = config["hashlistpath"]

    if not os.path.exists(wlpath) or not os.path.exists(hashpath):
        sys.exit("\nError, please check wordlist or hashlist path in config.json\n")

    with open(hashpath) as h:
        hashes = h.read().splitlines()


def crackhash(hsh, wlpath):
    mode = len(hsh)
    start = time.time()

    if mode != 32 and mode != 40 and mode != 64:
        print(f"\nUnknown hash type: '{hsh}'\n")

    with open(wlpath, encoding="utf8", errors="ignore") as f:

        for word in f:
            word = word.rstrip()

            if makehash(word, mode) == hsh:
                print(f"{hsh[0:5]}... cracked with {word} in {round(time.time()-start, 2)} seconds")
                return

    print(f"Count not crack hash '{hsh}'")


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

begin = time.time()

if __name__ == "__main__":
    if mp.cpu_count() // 4 == 1:
        num_workers = mp.cpu_count() - 2
    elif mp.cpu_count() // 4 == 2:
        num_workers = mp.cpu_count() - 3
    elif mp.cpu_count() // 4 >= 3:
        num_workers = mp.cpu_count() - 4
    else:
        num_workers = 1

    pool = mp.Pool(num_workers)

    for hsh in hashes:
        pool.apply_async(crackhash, args=(hsh, wlpath, ))

    pool.close()
    pool.join()

    alltime = time.time() - begin
    minutes = int(alltime // 60)
    seconds = round(alltime % 60, 2)
    
    print(f"\nTotal Runtime: {minutes} minute(s) {seconds} seconds")
