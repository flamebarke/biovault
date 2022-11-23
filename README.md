![Biovault](/biovault.png)

### About:

With the two helper scripts in this repo it is possible to read and write an AES-256 encrypted file on an NFC implant (specifically the [xSIID](https://dangerousthings.com/product/xsiid/)). The `hf_i2c_plus_2k_utils` script can also be used standalone to write arbitrary data to user memory on a sector of your choosing (sector 0 or 1). 

The `vault.py` script is a python wrapper around `hf_i2c_plus_2k_utils` which reads and writes an encrypted CSV file. The CSV file is carved from the hexdump, reversed with xxd and then displayed in the terminal in JSON format.

`vault.py` writes data to sector 1 not sector 0 for two reasons:

1.  Sector 0 can still be used to read and write NDEF records. Sector 1 remains untouched when modifying sector 0.
2.  Sector 1 is not accessible from Android or IOS without a custom application or a tool to send raw commands.

Even with encrypted data written to sector 1, when the implant is read from a device such as a phone it will still only return the NDEF record in sector 0 (URL, vcard etc). When the encrypted data needs to be accessed just use the proxmark3 to access sector 1 using `vault.py`.



### To Do:

- [ ] : The lua script is good. The python script is functional but shit. When I have some time I will refactor it to use pure python not os.system calls so no files need to be written/deleted from disk.
- [ ] : Add support for other data formats and maybe some compression to save space.


### Requirements:


Software: python3, openssl, jq ,csvtojson

Hardware: proxmark3

Usage:

1.  move `hf_i2c_plus_2k_utils.lua` to `~/.proxmark3/luascripts/`
    - this script is now in the [Proxmark3 Iceman fork](https://github.com/RfidResearchGroup/proxmark3/blob/master/client/luascripts/hf_i2c_plus_2k_utils.lua) so you can just do a `git pull` to grab the latest version
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


*Note:* 

*You will need to modify variables `pm3_path` and `uid` in vault.py (lines 13,14) to reflect the path to the pm3 binary and your implants UID.* 
*If you already have data on sector 1, use the -z flag to zero out the user memory of sector 1 with NULL bytes.*

### Demo:

![xSIID Vault](https://x90x90.net/assets/files/biovault/biovault.gif)
