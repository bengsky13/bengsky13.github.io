# Tattletale

## Challenge Description
A forensics challenge involving a Linux keylogger. We are provided with a PyInstaller-packed executable (`serizawa`), a captured data file (`cron.aseng`), and an encrypted file (`whatisthis.enc`).

## Investigation

### 1. Malware Analysis (`serizawa`)
First, we analyze the binary type.
```bash
$ file serizawa
serizawa: ELF 64-bit LSB executable...
```
It appears to be a PyInstaller packed binary. We extract it:
```bash
$ python3 pyinstxtractor.py serizawa
```
This creates `serizawa_extracted`. We locate the main logic script (usually sharing the name of the binary) and decompile it:
```bash
$ uncompyle6 serizawa_extracted/serizawa.pyc > serizawa.py
```
**Analysis**: The script reads `/dev/input/event0` (keyboard) and writes structs of `QQHHi` format (timestamp, type, code, value) to `/opt/cron.aseng`.

### 2. Log Analysis (`cron.aseng`)
To understand what was typed, we wrote a script to parse the binary event data.

```python
# parsing cron.aseng
import struct
events = open("cron.aseng", "rb").read()
# unpack in chunks of 24 bytes...
```
**Reconstructed Keystrokes**:
The attacker/user performed the following commands:
1.  `ls -la`
2.  `env > whatisthis`
3.  `od whatisthis > whatisthis.baboi`
4.  `openssl enc -aes-256-cbc -salt -in whatisthis.baboi -out whatisthis.enc -pass pass:4_g00d_fr13nD_in_n33D -pbkdf2`
5.  `rm whatisthis whatisthis.baboi`

### 3. Decryption
We have the encrypted file `whatisthis.enc` and the password `4_g00d_fr13nD_in_n33D`. We verify the command used above used `-pbkdf2`.

```bash
$ openssl enc -d -aes-256-cbc -in whatisthis.enc -out decrypted.octal -pass pass:4_g00d_fr13nD_in_n33D -pbkdf2
```
This decrypts to an **octal dump** (produced by `od`). We need to reverse the `od` format to get the original text.

```bash
# Convert octal dump back to binary/text
# (Custom script or text processing required)
```

The resulting text contains the environment variables.

## Findings
*   **Malware Type**: Keylogger
*   **Target**: Linux Input Subsystem
*   **Recovered Password**: `4_g00d_fr13nD_in_n33D`

## Flag
`C2C{it_is_just_4_very_s1mpl3_l1nuX_k3ylogger_xixixi_haiyaaaaa_ez}`
