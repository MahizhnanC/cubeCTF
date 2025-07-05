
## Step 1: Acquiring the Evidence — FTK Imager

The challenge provided us with a **disk image or archive** that seemed to contain Discord-related artifacts. 
I began analysis using **FTK Imager**, a forensic tool used to inspect and extract files from disk images.

 From FTK Imager:
- I navigated to `C:\Users\Admin\AppData\Roaming\discord\Cache\Cache_data`.
- I observed a large set of files with `.enc` extensions — clearly encrypted.
- I exported this entire folder to begin reverse engineering.
- Also the encrypter was found in the downloads

---

##  Step 2: Ghidra analysis
- In the entry poit of the functions , i saw the function FUN_14000c1fc(); which was suspicious
- In the FUN_14000c1fc() , i saw uVar3 = FUN_140001000(*puVar10,uVar4,uVar5,in_R9); which was suspicious
- From there to FUN_140002b80((uint *)PTR_DAT_140040000,param_2,param_3,param_4);
- This function revealed it checks environment variables like PYINSTALLER_RESET_ENVIRONMENT, which confirms it was built using Pyinstaller 


```
python3 pyinstxtractor.py encrypt.exe
This generated:

encrypt.exe_extracted/
├── encrypt.pyc
├── struct (binary files)

```

## Step 3: Decompiling the .pyc File
The extracted encrypt.pyc was Python 3.11 bytecode. Many popular tools failed:

- uncompyle6: Unsupported Python version.
- pycdc: Could not handle new opcodes.
- PyLingual: Successfully decompiled!

 Key findings from code:

```
sentry_path = get_appdata_path() + 'Discord' + 'sentry' + 'scope_v3.json'
user_id = sentry_data['scope']['user']['id']
key = PBKDF2(user_id.encode(), salt=b'BBBBBBBBBBBBBBBB', dkLen=32, count=1000000)
iv = b'BBBBBBBBBBBBBBBB'
```

The script fetched the Discord user ID from scope_v3.json.
It used PBKDF2 with 1 million iterations to derive the AES key.
The encryption was done using AES-CBC with fixed IV and salt.

 ## Step 4: Finding the Decryption Key
 
We located the file:

\AppData\Roaming\Discord\sentry\scope_v3.json

Contents included:
```

"user": {
  "id": "1334198101459861555",
  "username": "anorak644"
}
```
 So the key derivation looked like:
```
PBKDF2(b"1334198101459861555", b"BBBBBBBBBBBBBBBB", 32, 1000000)
```

## Step 5: Writing the Decryption Script
I wrote a decryption script to brute decrypt all .enc files in the extracted cache directory:

You can view or download the full script [here](script.py).

# decryptor.py
```

```
This successfully generated files like:

f_00001a

f_00002f

f_00003a

f_00005b

## Step 6: Identifying File Types
 
We used the Unix file command and visual inspection to identify formats:

file f_00003a

# PNG image data, 192x108, 8-bit/color RGB, non-interlaced

We renamed files accordingly:

f_00003a → f_00003a.png
f_00003b → f_00003b.woff2
f_00003c → f_00003c.gz
f_00003d → f_00003d.webp
f_00005b → f_00005b.jpg

## Step 7: Finding the Flag
Among the decrypted and renamed images, we found:

f_00003a.png

Opening it revealed a meme:

![Flag found in image](f_00003e.webp)

With the flag clearly visible at the bottom:

USCG{LOOK_MA_I_DEOBFUSCATED_IT}

## Final Flag

USCG{LOOK_MA_I_DEOBFUSCATED_IT}
