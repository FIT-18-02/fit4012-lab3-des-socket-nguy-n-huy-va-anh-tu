import os
import socket
import sys
from des_socket_utils import encrypt_des_cbc, build_packet

# Lấy cấu hình từ biến môi trường hoặc dùng mặc định[cite: 2, 9]
SERVER_IP = os.getenv('SERVER_IP', '127.0.0.1')
SERVER_PORT = int(os.getenv('SERVER_PORT', '6001'))
MESSAGE_ENV = os.getenv('MESSAGE')
LOG_FILE = os.getenv('SENDER_LOG_FILE', 'logs/sender.log')

def get_message() -> bytes:
    """Lấy thông điệp từ biến môi trường hoặc bàn phím[cite: 2, 6]"""
    if MESSAGE_ENV:
        return MESSAGE_ENV.encode('utf-8')
    plain = input("Nhập bản tin muốn gửi: ")
    return plain.encode('utf-8')

def main() -> None:
    # 1. Chuẩn bị dữ liệu[cite: 2]
    plain = get_message()

    # 2. Mã hóa[cite: 2, 8]
    key, iv, cipher_bytes = encrypt_des_cbc(plain)

    # 3. Đóng gói[cite: 8, 14]
    overall_packet = build_packet(key, iv, cipher_bytes)

    # 4. Gửi qua Socket[cite: 2, 5]
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(overall_packet)

        # 5. Thông báo và lưu log minh chứng[cite: 2, 6]
        output = [
            "[+] Đã gửi bản mã thành công.",
            f"Key (hex): {key.hex()}",
            f"IV (hex): {iv.hex()}",
            f"Ciphertext (hex): {cipher_bytes.hex()}",
            f"Tổng độ dài gói: {len(overall_packet)} byte"
        ]

        for line in output:
            print(line)

        # Tạo thư mục logs nếu chưa có
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(output) + '\n')

    except ConnectionRefusedError:
        print(f"[-] Lỗi: Không thể kết nối tới Receiver tại {SERVER_IP}:{SERVER_PORT}. Hãy chạy receiver.py trước!")
        sys.exit(1)

if __name__ == '__main__':
    main()