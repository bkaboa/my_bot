import requests
import sys
import json
from time import time, sleep

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Scrapper:
    def get_reddit(self, subreddit, header):
        # data = open("test.json", "r")
        # data = json.load(data)
        data = requests.get(
            url=subreddit["url"],
            headers=header,
        )
        if (data.status_code != 200):
            eprint(bcolors.FAIL +  "Error: ", data.status_code, " ", subreddit["url"] + bcolors.ENDC)
            return None
        return data

    async def get_messages(self, configs, file):
        messages = []
        message_data = ()
        for subreddit in configs["reddit"]:
            data = self.get_reddit(subreddit, configs["header"])
            sleep(1)
            if data is None:
                continue
            childs = data.json()["data"]["children"]
            # childs = data["data"]["children"]
            for child in childs:
                title = child["data"]["link_flair_text"]
                for topic in subreddit["topics"]:
                    print(topic)
                    if title == None or topic["topic"] in title or topic == "":
                        if (configs["timestamp"] > child["data"]["created_utc"]):
                            break
                        url = child["data"]["url"]
                        message_data = (topic["channel"], url)
                        print(bcolors.OKBLUE + url + bcolors.ENDC)
                        messages.append(message_data)
                        break
        configs["timestamp"] = time()
        file.seek(0)
        json.dump(configs, file, indent=4)
        file.truncate()
        print("Messages: " + str(messages))
        return messages
