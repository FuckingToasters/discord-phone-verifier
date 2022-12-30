import random

class randomagentclass:
    def randomagent(self):
        with open("files/useragents.txt") as ua_file:
            self.LINES = ua_file.readlines()
            self.USERAGENT = random.choice(self.LINES).strip()
        return self.USERAGENT