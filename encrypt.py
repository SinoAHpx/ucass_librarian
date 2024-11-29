from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import random

def get_aes_string(text, key, iv):
    # Remove leading/trailing whitespace from key
    key = key.strip()
    
    # Convert strings to bytes
    text = text.encode('utf-8')
    key = key.encode('utf-8')
    iv = iv.encode('utf-8')
    
    # Create cipher and encrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(text, AES.block_size))
    
    # Convert to base64 string
    return base64.b64encode(encrypted).decode('utf-8')

def random_string(length):
    chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_aes(text, key):
    if key:
        return get_aes_string(random_string(64) + text, key, random_string(16))
    return text

def encrypt_password(password, key):
    try:
        return encrypt_aes(password, key)
    except Exception:
        return password

def decrypt_password(encrypted_text, key):
    try:
        # Convert from base64
        encrypted_data = base64.b64decode(encrypted_text)
        
        # Convert key to bytes
        key = key.strip().encode('utf-8')
        iv = random_string(16).encode('utf-8')
        
        # Create cipher and decrypt
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        
        # Return the decrypted text without the first 64 characters
        return decrypted[64:].decode('utf-8')
    except Exception as e:
        print(f"Decryption error: {e}")
        return encrypted_text