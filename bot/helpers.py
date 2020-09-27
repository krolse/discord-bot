import ctypes.util
import os

import discord

from definitions import ROOT_PATH


def import_sounds():
    return [os.path.splitext(x)[0] for x in os.listdir(f'{ROOT_PATH}/sounds')]


def load_opus():
    if not discord.opus.is_loaded():
        lib = ctypes.util.find_library('opus')
        discord.opus.load_opus(lib or 'libopus-0')
