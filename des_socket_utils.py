import os
import struct
from typing import Tuple
from Crypto.Cipher import DES

BLOCK_SIZE = 8
# Header chuẩn của bài lab: 8 byte Key + 8 byte IV + 4 byte Length[cite: 8, 14]
HEADER_SIZE = 8 + 8 + 4

def pad(data: bytes) -> bytes:
    """Thêm padding PKCS#7 để dữ liệu là bội số của 8 byte[cite: 8, 15]"""
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad(data: bytes) -> bytes:
    """Loại bỏ padding PKCS#7[cite: 8, 15]"""
    if not data:
        raise ValueError("Dữ liệu rỗng, không thể bỏ padding.[cite: 8]")
    pad_len = data[-1]
    if pad_len < 1 or pad_len > BLOCK_SIZE:
        raise ValueError("Padding không hợp lệ.[cite: 8]")
    if data[-pad_len:] != bytes([pad_len]) * pad_len:
        raise ValueError("Padding PKCS#7 không khớp.[cite: 8]")
    return data[:-pad_len]

def encrypt_des_cbc(plain: bytes, key: bytes | None = None, iv: bytes | None = None) -> Tuple[bytes, bytes, bytes]:
    """Mã hóa DES ở chế độ CBC"""
    key = key or os.urandom(8)
    iv = iv or os.urandom(8)
    if len(key) != 8 or len(iv) != 8:
        raise ValueError("DES key và IV phải dài đúng 8 byte.[cite: 8]")
    des = DES.new(key, DES.MODE_CBC, iv)
    cipher_bytes = des.encrypt(pad(plain))
    return key, iv, cipher_bytes

def decrypt_des_cbc(key: bytes, iv: bytes, cipher_bytes: bytes) -> bytes:
    """Giải mã DES ở chế độ CBC và bỏ padding (Hàm bạn đang thiếu)"""
    if len(key) != 8 or len(iv) != 8:
        raise ValueError("DES key và IV phải dài đúng 8 byte.[cite: 8]")
    des = DES.new(key, DES.MODE_CBC, iv)
    decrypted = des.decrypt(cipher_bytes)
    return unpad(decrypted)

def build_packet(key: bytes, iv: bytes, cipher_bytes: bytes) -> bytes:
    """Đóng gói gói tin theo đúng thứ tự giao thức[cite: 8, 14]"""
    return key + iv + struct.pack('!I', len(cipher_bytes)) + cipher_bytes

def parse_header(header: bytes) -> tuple[bytes, bytes, int]:
    """Phân tách header 20 byte[cite: 5, 8]"""
    if len(header) != HEADER_SIZE:
        raise ValueError(f"Header phải dài đúng {HEADER_SIZE} byte.[cite: 8]")
    key = header[:8]
    iv = header[8:16]
    length = struct.unpack('!I', header[16:20])[0]
    return key, iv, length

def recv_exact(conn, n: int) -> bytes:
    """Nhận chính xác n byte từ socket[cite: 5, 8]"""
    chunks = []
    received = 0
    while received < n:
        chunk = conn.recv(n - received)
        if not chunk:
            raise ConnectionError("Kết nối bị đóng bất ngờ.[cite: 8]")
        chunks.append(chunk)
        received += len(chunk)
    return b''.join(chunks)