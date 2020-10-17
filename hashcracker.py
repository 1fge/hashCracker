import json
import hashlib
import os
import sys
import time
import multiprocessing

class HashCracker:
    def __init__(self, wordlist_path=None, hashlist_path=None):
        self.start_time = time.time()
        self.wordlist_path = wordlist_path
        self.hashlist_path = hashlist_path
        self.unsolved_hashes = multiprocessing.Manager().list()
        self.unknown_hash_types = []
        self.sorted_hashes = {
            "md5": {
                "hashes": [],
            },
            "sha1": {
                "hashes": [],
            },
            "sha256": {
                "hashes": [],
            }
        }
        if wordlist_path is None or hashlist_path is None:
            with open("config.json") as config_file:
                config = json.load(config_file)
            self.wordlist_path = self._get_wordlist_path(wordlist_path, config)
            self.hashlist_path = self._get_hashlist_path(hashlist_path, config)

    def _get_wordlist_path(self, wordlist_path, config):
        """If no value is given for wordlist_path in `HashCracker` constructor,
        attempt to use the wordlist path found in config.json.

        Args:
            wordlist_path (str/None): String of wordlist path or was initialized to None.
            config (dict): Dictionary containing secondary wordlist path.

        Returns:
            str:  Path to wordlist file.
        """
        if wordlist_path is None:
            return config["wordlistpath"]
        return wordlist_path

    def _get_hashlist_path(self, hashlist_path, config):
        """If no value is given for hashlist_path in `HashCracker` constructor,
        attempt to use the hashlist path found in config.json.

        Args:
            hashlist_path (str/None): String of hashlist path or was initialized to None.
            config (dict): Dictionary containing secondary hashlist path.

        Returns:
            str: Path to hashlist file.
        """
        if hashlist_path is None:
            return config["hashlistpath"]
        return hashlist_path

    def _return_hash_type(self, hsh):
        """Attempt to identify the hash's algorithm based upon its length.

        Args:
            hsh (str): Hash to identify type of.

        Returns:
            str/None: Result of using .get on dictionary containing hash lengths.
        """
        hash_types = {
            32: "md5",
            40: "sha1",
            64: "sha256"
        }
        potential_hash_type = len(hsh)
        return hash_types.get(potential_hash_type)

    def _verify_file_locations(self):
        """Check if wordlist path and hashlist path exist.
        Exit the program if they do not.
        """
        both_files_exist = True
        if not os.path.exists(self.wordlist_path):
            print(f"ERROR: wordlist not found at path '{self.wordlist_path}'")
            both_files_exist = False
        if not os.path.exists(self.hashlist_path):
            print(f"ERROR: hashlist not found at path '{self.hashlist_path}'")
            both_files_exist = False
        if not both_files_exist:
            sys.exit()

    def _sort_hashes(self):
        """Strip each hash and attempt to categorize it based upon length"""
        for hsh in self.hashlist:
            hsh = hsh.strip()
            hash_type = self._return_hash_type(hsh)
            if hash_type is not None:
                self.sorted_hashes[hash_type]["hashes"].append(hsh)
            else:
                self.unknown_hash_types.append(hsh)
        print("Sorted hashes")

    def load_hashes(self):
        """Ensure specificied wordlist and hashlist paths exist.
        Set hashlist attribute to hashlist file contents split by newline.
        Finally, place each hash in a list depending on the algorithm
        """
        self._verify_file_locations()
        with open(self.hashlist_path) as f:
            self.hashlist = f.readlines()
        self._sort_hashes()
        print("Loaded hashes")

    def _make_hash(self, word, algorithm):
        """Create a hash of a word using a specific hashing algorithm.

        Args:
            word (str): String to be hashed.
            algorithm (str): Specific hashing algorithm (md5, sha1, sha256).

        Returns:
            str: Hashed `word` parameter.
        """
        hash_modes = {
            "md5": hashlib.md5(),
            "sha1": hashlib.sha1(),
            "sha256": hashlib.sha256()
        }
        m = hash_modes[algorithm]
        m.update(word.encode("utf-8"))
        return m.hexdigest()
    
    def _crack_hashes(self, algorithm):
        """For each hash of a specific algorithm, 
        iterate through the word list and attempt to find the original string.

        Args:
            algorithm (str): Specific hashing algorithm (md5, sha1, sha256).
        """
        hashlist = self.sorted_hashes[algorithm]["hashes"]
        start_time = self.start_time
        with open(self.wordlist_path, encoding="utf-8", errors="ignore") as wordlist:
            for word in wordlist:
                word = word.rstrip()
                current_hash = self._make_hash(word, algorithm)
                if current_hash in hashlist:
                    hashlist.remove(current_hash)
                    elapsed_time = round(time.time() - start_time, 2)
                    print(f"{current_hash[0:15]}... : {word} ({elapsed_time}s)")
                    if not hashlist: # if the list of hashes is empty, no need to keep reading wordlist
                        break
        self.unsolved_hashes.extend(hashlist)

    def _display_unknown_unsolved_hashes(self):
        """Display each unsolved hash along with each hash of an unknown format"""
        if self.unsolved_hashes:
            print("\n--UNSOLVED HASHES--")
            for unsolved_hash in self.unsolved_hashes:
                print(unsolved_hash)
        if self.unknown_hash_types:
            print("\n--UNKNOWN HASH TYPES--")
            for unknown_hash in self.unknown_hash_types:
                print(unknown_hash) 

    def crack(self):
        """For each type of hash, create a process to hash each item in wordlist and check for matches"""
        hash_processes = []
        if self.sorted_hashes["md5"]["hashes"]:
            md5_cracker = multiprocessing.Process(
                target=self._crack_hashes, 
                args=("md5",)
            )
            hash_processes.append(md5_cracker)
        if self.sorted_hashes["sha1"]["hashes"]:
            sha1_cracker = multiprocessing.Process(
                target=self._crack_hashes, 
                args=("sha1",)
            )
            hash_processes.append(sha1_cracker)
        if self.sorted_hashes["sha256"]["hashes"]:
            sha256_cracker = multiprocessing.Process(
                target=self._crack_hashes, 
                args=("sha256",)
            )
            hash_processes.append(sha256_cracker)

        for hash_process in hash_processes:
            hash_process.start()
        for hash_process in hash_processes:
            hash_process.join()
        self._display_unknown_unsolved_hashes()

if __name__ == "__main__":
    #cracker = HashCracker(wordlist_path="rockyou.txt", hashlist_path="example_hashes.txt")
    cracker = HashCracker()
    cracker.load_hashes()
    cracker.crack()


