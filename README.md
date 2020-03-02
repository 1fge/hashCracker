# hashCracker
hashCracker is Python program used to crack unknown hashes. Place a list of random hashes in any order that use the MD5, SHA-1, or SHA-256 algorithms. All libraries used are a part of the standard library in Python.
# How to Install
To install hashCracker, ensure you have Python 3 on your machine. Clone the directory to wherever you desire, and edit the config file to reflect the paths to the files you want to use for your wordlist and hash list. 
# Info  
Compared to previous versions, speeds have been increased dramatically. This was achieved by sorting hashes by hash type, and opening the wordlist once per hash type. Previous versions would read the word list for each unknown hash, wasting time and computer resources.
