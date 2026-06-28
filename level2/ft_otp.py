import sys
import time
import hmac
import hashlib
import struct
from pathlib import Path

def validate_and_save_key(filename):
    try:
        with open(filename, 'r') as f:
            cle_hex = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    if len(cle_hex) != 64:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return 
    
    for char in cle_hex:
        if (char < '0' or char > '9') and (char < 'a' or char > 'f') and (char < 'A' or char > 'F'):
            print("./ft_otp: error: key must be 64 hexadecimal characters.")
            return
    
    try:
        key_bytes = bytes.fromhex(cle_hex)
    except ValueError:
        print("./ft_otp: error: key must be 64 hexadecimal characters.")
        return

    new_file = str(Path(filename).with_suffix(".key"))
    with open(new_file, "wb") as f:
        f.write(key_bytes)
    
    print("Key was successfully saved in " + filename)


def ft_otp(filename):
    try:
        with open(filename, 'rb') as f:
            key_bytes = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return

    current_time = int(time.time())
    counter = current_time // 30

    counter_bytes = struct.pack(">Q", counter)

    mac = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()

    offset = mac[-1] & 0x0f
    binary = struct.unpack('>I', mac[offset:offset+4])[0] & 0x7fffffff
    
    otp = binary % 1000000
    
    print(f"{otp:06d}")

def main():
    if len(sys.argv) != 3:
        print("Usage:\n  ./ft_otp -g <key_file.hex>\n  ./ft_otp -k <ft_otp.key>")
        sys.exit(1)
    
    flag = sys.argv[1]
    filename = sys.argv[2]

    if flag == "-g":
        validate_and_save_key(filename)
    elif flag == "-k":
        ft_otp(filename)
    else:
        print("Error: unknown flag. Use -g or -k.")

if __name__ == "__main__":
    main()



# uint32_t binary = ((mac[offset] & 0x7f) << 24) |
#                   (mac[offset + 1] << 16) |
#                   (mac[offset + 2] << 8)  |
#                   (mac[offset + 3]);