#!/usr/bin/python3

import requests
import configparser
import os
import sys
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class RunFailed(Exception):
    def __init__(self, m):
        self.message = m

    def __str__(self):
        return self.message


class Config:
    def __init__(self):
        if os.path.dirname(__file__) != "":
            os.chdir(os.path.dirname(__file__))

        # Read config from ini file: .env.yml
        self.config = configparser.ConfigParser()
        self.config.read('.env')

    def get(self, key):
        # get config object
        return self.config.get('default', key)


class OutlineOperation:
    def __init__(self, name):
        self.cfg = Config()
        self.name = name
        self.id = -1

    def createAccessKey(self):
        url = self.cfg.get("API_URL") + "/access-keys"
        r = requests.post(url, verify=False)
        if r.status_code == 201:
            self.id = r.json()["id"]
            return r.json()
        else:
            raise RunFailed("Error: can't create access key for " + self.name)

    def renameUser(self):
        url = self.cfg.get("API_URL") + "/access-keys/" + \
            str(self.id) + "/name"
        r = requests.put(url, data={"name": self.name}, verify=False)
        if r.status_code == 204:
            print(r.text)
        else:
            raise RunFailed("Error: can't rename for " + self.name)

    def addUser(self):
        try:
            info = self.createAccessKey()
            self.renameUser()
            return info
        except Exception as e:
            print(e)

    def deleteAccessKey(self, id):
        url = self.cfg.get("API_URL") + "/access-keys/" + str(id)
        requests.delete(url, verify=False)


def replaceDomain(str, newStr):
    m = re.match(r'.*@(.*?):.*', str)
    oldPattern = m.groups()[0]
    return str.replace(oldPattern, newStr)


def main():
    cfg = Config()
    output = open("result.txt", "a")
    with open('user.txt') as f:
        for line in f.readlines():
            line = line.rstrip()

            if line != "":
                o = OutlineOperation(line)
                info = o.addUser()
                accessUrl = replaceDomain(
                    info["accessUrl"], cfg.get("DOMAIN_NAME"))
                output.write(line + "\t" + accessUrl + "\n")
    output.close()


if __name__ == '__main__':
    main()
