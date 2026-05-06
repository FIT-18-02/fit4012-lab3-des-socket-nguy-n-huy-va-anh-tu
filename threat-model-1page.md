# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: Phạm Anh Tú
- Thành viên 2: TODO_STUDENT

## Assets
Nội dung bản tin gốc (Plaintext).

Khóa mã hóa DES (8 byte) và IV (8 byte).
## Attacker model
Kẻ tấn công có khả năng nghe lén gói tin trên đường truyền mạng (Network Sniffer).

## Threats
Eavesdropping: Vì Key và IV được gửi trực tiếp trong Header của gói tin mà không được mã hóa, kẻ tấn công có thể dễ dàng trích xuất chúng để giải mã toàn bộ bản tin.
Brute-force: Thuật toán DES có độ dài khóa ngắn, dễ bị tấn công vét cạn bằng sức mạnh tính toán hiện đại.
## Mitigations
Bọc luồng Socket bằng lớp bảo mật TLS/SSL.
Sử dụng các thuật toán mạnh hơn như AES-256.
Sử dụng giao thức trao đổi khóa Diffie-Hellman để không phải gửi khóa trực tiếp qua mạng.
## Residual risks
TODO_STUDENT: Nêu ít nhất 1 rủi ro còn lại.
