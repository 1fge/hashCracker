import hashlib, time, os

modes = ["md5", "sha1", "sha256"]

def promptPickMode():
    userMode = ""
    while userMode not in modes:
        userMode = input('\nError, please enter the hashing algorithm you want to use (md5, sha1, sha256)')
        if userMode == "md5":
            print("MD5 algorithm selected, continuing")
            return userMode
            break
        elif userMode == "sha1":
            print("SHA-1 selected, continuing")
            return userMode
            break
        elif userMode == "sha256":
            print("SHA-256 selected, continuing")
            return userMode
            break
        
def getMode():   
    userMode = input("Please enter hashing algorithm (md5, sha1, sha256) ").lower()
    if userMode not in modes:
        pass
    elif userMode == "md5":
        print("MD5 algorithm selected, continuing")
        return userMode
    elif userMode == "sha1":
        print("SHA-1 selected, continuing")
        return userMode
    elif userMode == "sha256":
        print("SHA-256 selected, continuing")
        return userMode
    

attempt1 = getMode()
attempt2 = None

if attempt1 == None:
    while attempt2 == None:
        attempt2 = promptPickMode()

# get user wordlist and lastline of the file (ptwResults[0] = wlPath & ptwResults[1] = wlLastLine
ptwResults = []
def pathToWordlist():
    wlPath = input("\nPlease copy and paste the path to your wordlist ")
    ptwResults.append(wlPath)

    with open(wlPath, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            pass
        last = line
        ptwResults.append(last)
                    

pathToWordlist()

wlPath = ptwResults[0]
wlLastLine = ptwResults[1]
wlLastLine = wlLastLine.strip()
print("Obtained wordlist {}".format(os.path.basename(wlPath)))
        
def userHash():
    userHash = input("\nPlease enter all of your hashes separated by a comma (no spaces) ")
    userHash = userHash.split(",")
    return userHash

userHash = userHash()

# various hashing algs    
def makeMd5Hash(string):
    string = string.encode("utf-8")
    m = hashlib.md5()
    m.update(string)

    currentHash = m.hexdigest()
    return currentHash

def makeSha1Hash(string):
    string = string.encode("utf-8")
    m = hashlib.sha1()
    m.update(string)

    currentHash = m.hexdigest()
    return currentHash

def makeSha256Hash(string):
    string = string.encode("utf-8")
    m = hashlib.sha256()
    m.update(string)

    currentHash = m.hexdigest()
    return currentHash

# compares hashes with user-provided algorithm
def compareHash():
    print("\nComparing {} hash(es) to selected wordlist".format(len(userHash)))

    def initHashes():
        solvedHashes = []
        unsolvedHashes = []
        totalTimes = []
        for i in userHash:
            start = time.time()
            with open(wlPath, "r", encoding="utf8", errors="ignore") as wordlist:
                for lineWord in wordlist:
                    lineWord = lineWord.strip()

                    if attempt1 == "md5" or attempt2 == "md5":
                        alg = "MD5"
                        lineHash = makeMd5Hash(lineWord)   
                    elif attempt1 == "sha1" or attempt2 == "sha1":
                        alg = "SHA-1"
                        lineHash = makeSha1Hash(lineWord)
                    elif attempt1 == "sha256" or attempt2 == "sha256":
                        alg = "SHA-256"
                        lineHash = makeSha256Hash(lineWord)

                    if i == lineHash:
                            
                            pos = userHash.index(i)
                            end = time.time()
                            allTime = end - start
                            print("Process took {} seconds".format(allTime))
                            print("***ALERT*** HASH {}  CRACKED WITH STRING\n{}\n".format(userHash[pos],lineWord))

                            solvedHashes.append((i,lineHash,lineWord,allTime))
                            totalTimes.append(float(allTime))
                            break
                       
                    elif lineWord == wlLastLine:
                        if i != lineHash:
                                end = time.time()
                                allTime = end - start
                                totalTimes.append(float(allTime))
                                pos = userHash.index(i)
                                print("Error, hash {} not found ({} seconds)".format(userHash[pos], allTime))
                                unsolvedHashes.append(i)
                                
                                break
                    else:
                              pass

        if len(solvedHashes) + len(unsolvedHashes) == len(userHash):
            print("\n\n********************************************")
            print("Algorithm: {}".format(alg))
            print("Wordlist: {}".format(os.path.basename(wlPath)))
            print("Solved Hashes: {}\n".format(len(solvedHashes)))
            for i in range(len(solvedHashes)):
                print("Your Hash: {}".format(solvedHashes[i][0]))
                print("Solved Hash: {}".format(solvedHashes[i][1]))
                print("Solved String: {}".format(solvedHashes[i][2]))
                print("Time Taken: {} seconds\n".format(solvedHashes[i][3]))
                
            print("Unsolved Hashes: {}".format(len(unsolvedHashes)))
            for i in range(len(unsolvedHashes)):
                print("Hash: {}".format(unsolvedHashes[int(i)]))
            print("********************************************\n")

            totalTime = 0        
            for i in totalTimes:
                totalTime = totalTime + i
            print("\nAll together, cracking took {} seconds".format(totalTime))
                        
    initHashes()
        
compareHash()

    
