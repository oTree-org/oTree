#!/usr/bin/env python
# standalone script to commit and push to git remote (e.g. Heroku).

import os
import sys

def run(environment):
    os.system('git commit -am "."')
    os.system('git push {} master'.format(environment))

def main():
    environment = sys.argv[1]
    run(environment)

if __name__ == '__main__':
    main()