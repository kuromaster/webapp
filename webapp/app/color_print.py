#! /usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime as dt
# import os
import traceback
from app import app

# import imp
# try:
#     imp.find_module('libs')
#     found = True
#     from libs import IS_DEBUG
# except ImportError:
#     found = False
#     IS_DEBUG = 1


if app.config['DEBUG']:
    # is_debug_on = int(os.environ["IS_DEBUG"])
    is_debug_on = 1
else:
    is_debug_on = 0


class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'
    CYAN = '\033[96m'


def cprint(status, text):

    if is_debug_on == 1:
        data = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        if status == 'GREEN':
            print(bcolors.GREEN + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'YELLOW':
            print(bcolors.YELLOW + '[W] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'PURPLE':
            print(bcolors.PURPLE + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'RED':
            print(bcolors.RED + '[E] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'BLUE':
            print(bcolors.BLUE + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'BOLD':
            print(bcolors.BOLD + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'UNDERLINE':
            print(bcolors.UNDERLINE + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'WHITE':
            print(bcolors.ENDC + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'GRAY':
            print(bcolors.GRAY + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)
        if status == 'CYAN':
            print(bcolors.CYAN + '[I] [{}] {}'.format(data, text) + bcolors.ENDC)


def PrintException(pth):
    # print("OOOOOOOOOOOOOOOOOOO: " + os.path.abspath(os.getcwd()))
    cprint("RED", "[ERROR] " + traceback.format_exc())
    if pth is not None:
        log(pth, "[ERROR] " + traceback.format_exc())


def log(pth, msg):
    # rotate_log(filePth)
    log_file = open(pth, "a")
    with open(pth) as f:
        if not str(msg) in f.read():
            log_file.write("\n" + "[" + str(dt.now().strftime("%Y-%m-%d %H:%M:%S")) + "] {} \n".format(msg))
    log_file.close()
