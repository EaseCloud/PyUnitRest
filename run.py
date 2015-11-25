#!/usr/bin/python3.5
import os

import config


def begin():
    os.system('mysqldump -h%s -u%s -p%s > ')
