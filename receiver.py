import os
import socket
from des_socket_utils import HEADER_SIZE, parse_header, recv_exact, decrypt_des_cbc

# Cấu hình từ biến môi trường hoặc mặc định[cite: 5, 9]
HOST = os.getenv('RECEIVER_HOST', '0.0.0.0')
PORT = int(os.getenv('RECEIVER_PORT', '6001'))
TIMEOUT = float(os.getenv('SOCKET_TIMEOUT', '30'))  # Chờ tối đa 30s
OUTPUT_FILE = os.getenv('RECEIVER_OUTPUT_FILE', 'logs/received_message.txt')
LOG_FILE = os.getenv('RECEIVER_LOG_FILE', 'logs/receiver.log')

def main() -> None:
    # 1. Khởi tạo TCP Socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Cho phép sử dụng lại địa chỉ nếu chương trình vừa tắt
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(1)
        s.settimeout(TIMEOUT)

        print(f"[*] Đang lắng nghe tại {HOST}:{PORT}...")

        try:
            conn, addr = s.accept()
            with conn:
                print(f"[!] Kết nối từ: {addr}")

                # 2. Nhận Header (20 byte) để lấy Key, IV và Độ dài Ciphertext
                header_data = recv_exact(conn, HEADER_SIZE)
                key, iv, cipher_len = parse_header(header_data)

                # 3. Nhận chính xác số byte bản mã dựa trên độ dài trong header[cite: 5, 8]
                cipher_bytes = recv_exact(conn, cipher_len)

                # 4. Giải mã và loại bỏ Padding[cite: 5, 8]
                try:
                    plaintext_bytes = decrypt_des_cbc(key, iv, cipher_bytes)
                    message = plaintext_bytes.decode('utf-8', errors='ignore')

                    result_line = f"[+] Bản tin gốc nhận được: {message}"
                    print(result_line)

                    # 5. Lưu kết quả và Log minh chứng[cite: 5, 6]
                    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

                    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                        f.write(message)

                    with open(LOG_FILE, 'a', encoding='utf-8') as f:
                        f.write(f"From {addr}: {result_line}\n")

                except ValueError as e:
                    print(f"[-] Lỗi giải mã (Sai Key/IV hoặc dữ liệu bị hỏng): {e}")
                except Exception as e:
                    print(f"[-] Lỗi không xác định: {e}")

        except socket.timeout:
            print("[-] Hết thời gian chờ (Timeout). Không có kết nối nào đến.")
        except KeyboardInterrupt:
            print("\n[!] Đã dừng Receiver.")

if __name__ == '__main__':
    main()