import os
import socket
from des_socket_utils import HEADER_SIZE, parse_header, recv_exact, decrypt_des_cbc

# Cau hinh tu bien moi truong hoac mac dinh[cite: 5, 9]
HOST = os.getenv('RECEIVER_HOST', '0.0.0.0')
PORT = int(os.getenv('RECEIVER_PORT', '6001'))
TIMEOUT = float(os.getenv('SOCKET_TIMEOUT', '30'))  # Cho toi da 30s
OUTPUT_FILE = os.getenv('RECEIVER_OUTPUT_FILE', 'logs/received_message.txt')
LOG_FILE = os.getenv('RECEIVER_LOG_FILE', 'logs/receiver.log')

def main() -> None:
    # 1. Khoi tao TCP Socket[cite: 5]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Cho phep su dung lai dia chi neu chuong trinh vua tat[cite: 5]
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        s.settimeout(TIMEOUT)

        # Dong nay da sua thanh khong dau de fix loi UnicodeEncodeError
        print(f"[*] Dang lang nghe tai {HOST}:{PORT}...")

        try:
            conn, addr = s.accept()
            with conn:
                print(f"[!] Ket noi tu: {addr}")

                # 2. Nhan Header (20 byte) de lay Key, IV va Do dai Ciphertext[cite: 5, 8]
                header_data = recv_exact(conn, HEADER_SIZE)
                key, iv, cipher_len = parse_header(header_data)

                # 3. Nhan chinh xac so byte ban ma dua tren do dai trong header[cite: 5, 8]
                cipher_bytes = recv_exact(conn, cipher_len)

                # 4. Giai ma va loai bo Padding[cite: 5, 8]
                try:
                    plaintext_bytes = decrypt_des_cbc(key, iv, cipher_bytes)
                    message = plaintext_bytes.decode('utf-8', errors='ignore')

                    result_line = f"[+] Ban tin goc nhan duoc: {message}"
                    print(result_line)

                    # 5. Luu ket qua va Log minh chung[cite: 5, 6]
                    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

                    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                        f.write(message)

                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"From {addr}: {result_line}\n")

                except ValueError as e:
                    print(f"[-] Loi giai ma (Sai Key/IV hoac du lieu bi hong): {e}")
                except Exception as e:
                    print(f"[-] Loi khong xac dinh: {e}")

        except socket.timeout:
            print("[-] Het thoi gian cho (Timeout). Khong co ket noi nao den.")
        except KeyboardInterrupt:
            print("\n[!] Da dung Receiver.")

if __name__ == '__main__':
    main()