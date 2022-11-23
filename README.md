# xSIID vault

### Requirements:


Software: python3, openssl, jq ,csvtojson

Hardware: proxmark3

Usage:

1.  move `hf_i2c_plus_2k_utils.lua` to `~/.proxmark3/luascripts/`
2.  install jq and csvtojson : `brew install jq ; npm -g install csvtojson`
3.  create a csv file in the following format and save it as vault.txt in the same folder as vault.py:

Example vault.txt:
```
d,u,p
google.com,testuser,Password1
reddit.com,reddituser,Password2
```
to write the encrypted file to the xSIID:
4.  `python3 vault.py -m w` : write file

to read the encrypted file:
5.  `python3 vault.py -m r` : read passwords


#### Note: you will need to modify variables `pm3_path` and `uid` in vault.py (lines 13,14) to reflect the path to the pm3 binary and your implants UID.
