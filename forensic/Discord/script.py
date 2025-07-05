from pathlib import Path
from Cryptodome.Cipher import AES
from Cryptodome.Protocol.KDF import PBKDF2
from Cryptodome.Util.Padding import unpad

ENCODED_CACHE_PATH = Path(r"C:\Users\mahiy\Encoded_discord\Cache_Data")
user_id = "1334198101459861555"
salt = b"BBBBBBBBBBBBBBBB"
iv = b"BBBBBBBBBBBBBBBB"
key = PBKDF2(user_id.encode(), salt, 32, 1000000)

print(f"Decrypting files in {ENCODED_CACHE_PATH}...")
for file in ENCODED_CACHE_PATH.glob("*.enc"):
    try:
        ciphertext = file.read_bytes()
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), 16)
        decrypted_path = file.with_suffix("")  # remove .enc
        decrypted_path.write_bytes(plaintext)
        print(f"Decrypted {file.name} → {decrypted_path.name}")
    except Exception as e:
        print(f"Failed to decrypt {file.name}: {e}")
