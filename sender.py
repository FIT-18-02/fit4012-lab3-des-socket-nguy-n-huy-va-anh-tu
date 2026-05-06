import os
import socket
import sys
from des_socket_utils import encrypt_des_cbc, build_packet

# Cau hinh tu bien moi truong hoac mac dinh[cite: 2, 9]
SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '6001'))
MESSAGE_ENV = os.getenv('MESSAGE')
LOG_FILE = os.getenv('SENDER_LOG_FILE', 'logs/sender.log')

def get_message() -> bytes:
    if MESSAGE_ENV:
        return MESSAGE_ENV.encode('utf-8')
    plain = input("Nhap ban tin muon gui: ") # Sua thanh khong dau
    return plain.encode('utf-8')

def main() -> None:
    plain = get_message()
    key, iv, cipher_bytes = encrypt_des_cbc(plain)
    overall_packet = build_packet(key, iv, cipher_bytes)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(overall_packet)

        # Cac dong thong bao duoi day phai KHONG DAU[cite: 2]
        output = [
            "[+] Da gui ban ma.",
            f"Key: {key.hex()}",
            f"IV: {iv.hex()}",
            f"Ciphertext: {cipher_bytes.hex()}",
        ]

        for line in output:
            print(line)

        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output) + '\n')

    except ConnectionRefusedError:
        # Sua thong bao loi thanh khong dau[cite: 2]
        print(f"[-] Loi: Khong the ket noi toi Receiver tai {SERVER_IP}:{SERVER_PORT}.")
        sys.exit(1)

if __name__ == '__main__':
    main()