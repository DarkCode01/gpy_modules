#! /usr/bin/env python3

import Log

class Clasify(object):
    
    __init__(self, file):
        self.file = file
        self.log = Log()
        
    def find(self):
        commits = []
        for commit in self.log.split("\t"):
            if file in commit:
                logs.append(commit)
        return commits