from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
import random

def random_string(length):
    chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"
    return ''.join(random.choice(chars) for _ in range(length))

def encrypt_password(password, key):
    if not key:
        return password
    
    try:
        # Generate a 64-character random prefix (matching JS implementation)
        random_prefix = random_string(64)
        
        # Combine prefix and password
        plaintext = (random_prefix + password).encode('utf-8')
        
        # Pad key to 32 bytes
        key_bytes = key.encode('utf-8')
        key_bytes = key_bytes + b'\0' * (32 - len(key_bytes))
        
        # Generate random 16-byte IV (matching JS implementation)
        iv = random_string(16).encode('utf-8')
        
        # Create cipher object and encrypt the data
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
        
        # Pad and encrypt
        encrypted = cipher.encrypt(pad(plaintext, AES.block_size))
        
        # Encode as base64
        encrypted_message = base64.b64encode(encrypted)
        
        return encrypted_message.decode('utf-8')
        
    except Exception as e:
        print(f"Encryption error: {e}")
        return password

# Example usage:
if __name__ == "__main__":
    password = "frNwzTNNeGnAkkq6ADpAqv*ZGvPHYU"
    key = "F9be0zpobE1zsNmv"
    encrypted = encrypt_password(password, key)
    print(encrypted)