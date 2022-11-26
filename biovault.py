#!/usr/bin/python3

import os
import argparse
from threading import Thread
from itertools import cycle
from shutil import get_terminal_size
from time import sleep
from subprocess import PIPE, Popen

# Author: Shain Lakin

pm3_path = "/Users/shain/Documents/tools/proxmark3/"
uid = "0478A5D2CD5280"
pre = '0' * 32

banner = """

"""


class Loader:
    def __init__(self, desc="Loading...", end="[+] Communicating with proxmark ... ", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!...".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()


# Parse arguments
parser = argparse.ArgumentParser(description="", \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-m", "--mode", type=str, default="r", help="Read/Write to vault")
parser.add_argument("-z", "--zero", action='store_true',  help="Zero sector with null bytes" )
args = parser.parse_args()

# Static strings
zero = f"{pm3_path}pm3 -c \'script run hf_i2c_plus_2k_utils -s 1 -m f -f zero.null\'"
aes_enc = f"openssl aes-256-cbc -salt -pbkdf2 -in vault.txt -out vault.txt.enc"
write_vault = f"{pm3_path}pm3 -c \'script run hf_i2c_plus_2k_utils -s 1 -m f -f vault.txt.enc\'"

dump_vault = f"{pm3_path}pm3 -c \'script run hf_i2c_plus_2k_utils -s 1 -m d\' >/dev/null 2>&1"
extract = f"/bin/cat {uid}.hex | awk -F \'{pre}\' \'{{print $2}}\' > dump.bin"
reverse_hex = "xxd -r -ps dump.bin > vault.txt.enc"
aes_dec = "openssl aes-256-cbc -d -pbkdf2 -in vault.txt.enc -out vault.txt.dec"
display = "csvtojson vault.txt.dec | jq"


# Process function
def proc(cmd):
    try:
        proc = Popen(f"{cmd}".split(), \
            stdin=PIPE, stdout=PIPE, stderr=PIPE)
        proc.communicate()
    except KeyboardInterrupt:
        exit(0)


# Create null byte file
def zero_file():
    with open(f"zero.null", "w+b") as z:
        z.write(b"\0" * 3000)


# Delete files
def clean():
    if args.mode == 'w':
        os.remove("vault.txt")
        os.remove("vault.txt.enc")
        if args.zero:
            os.remove("zero.null")
    elif args.mode == 'r':
        os.remove(f"{uid}.hex")
        os.remove("dump.bin")
        os.remove("vault.txt.enc")
        os.remove("vault.txt.dec")

# Loading function
def wait():
    loader = Loader("[+] Place proxmark on implant .. sleeping for 10").start()
    sleep(10)
    loader.stop()
    print("[+] Reading data ...")


def main():
    try:
        if args.mode == 'r':
            wait()
            os.system(dump_vault)
            os.system(extract)
            os.system(reverse_hex)
            proc(aes_dec)
            os.system(display)
            clean()
        elif args.mode == 'w':
            if args.zero:
                wait()
                zero_file()
                os.system(zero)
            proc(aes_enc)
            wait()
            os.system(write_vault)
            clean()
    except Exception as e:
        print(e)
        exit(0)

main()
