import os
import socket
import subprocess
import sys
import time
from pathlib import Path

# Xac dinh thu muc goc cua repo[cite: 13]
REPO_ROOT = Path(__file__).resolve().parents[1]

def find_free_port() -> int:
    """Tim mot cong trong tren he thong de chay test[cite: 13]"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]

def test_local_sender_receiver_roundtrip():
    port = find_free_port()

    # Thiet lap moi truong cho Receiver[cite: 13]
    receiver_env = os.environ.copy()
    receiver_env.update({
        "PYTHONUNBUFFERED": "1",
        "RECEIVER_HOST": "127.0.0.1",
        "RECEIVER_PORT": str(port),
        "SOCKET_TIMEOUT": "5",
    })

    # Thiet lap moi truong cho Sender[cite: 13]
    sender_env = os.environ.copy()
    sender_env.update({
        "PYTHONUNBUFFERED": "1",
        "SERVER_IP": "127.0.0.1",
        "SERVER_PORT": str(port),
        "MESSAGE": "Xin chao FIT4012 - local integration test",
    })

    # Khoi chay receiver.py nhu mot tien trinh con[cite: 13]
    receiver = subprocess.Popen(
        [sys.executable, "-u", "receiver.py"],
        cwd=REPO_ROOT,
        env=receiver_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    try:
        started = False
        start_time = time.time()
        collected = []

        # Doc tung dong tu stdout cua Receiver[cite: 13]
        while time.time() - start_time < 5:
            line = receiver.stdout.readline()
            if line:
                collected.append(line)
                # QUAN TRONG: Phai trung khop voi dong print trong receiver.py[cite: 5, 13]
                if "Dang lang nghe" in line:
                    started = True
                    break

        assert started, "Receiver khong khoi dong dung. Output: " + "".join(collected)

        # Khoi chay sender.py[cite: 13]
        sender = subprocess.run(
            [sys.executable, "sender.py"],
            cwd=REPO_ROOT,
            env=sender_env,
            capture_output=True,
            text=True,
            timeout=10,
            check=True,
        )

        receiver_out, _ = receiver.communicate(timeout=10)
        full_receiver_output = "".join(collected) + receiver_out

        # Kiem tra ket qua dau ra cua ca hai phia[cite: 13]
        assert "[+] Da gui ban ma." in sender.stdout
        assert "Key:" in sender.stdout
        assert "IV:" in sender.stdout
        assert "Ciphertext:" in sender.stdout
        assert "[+] Ban tin goc nhan duoc: Xin chao FIT4012 - local integration test" in full_receiver_output

    finally:
        # Dam bao luon dong tien trinh receiver sau khi test xong[cite: 13]
        if receiver.poll() is None:
            receiver.kill()