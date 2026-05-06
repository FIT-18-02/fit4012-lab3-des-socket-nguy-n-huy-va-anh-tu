# Peer Review Response

## Thông tin nhóm
- Thành viên 1: Nguyễn Văn Huy
- Thành viên 2: Anh Tú

## Thành viên 1 góp ý cho thành viên 2
Nguyễn Văn Huy: Cấu trúc code `receiver.py` rất tốt và bắt lỗi `ValueError` khi sai khóa chuẩn xác. Tuy nhiên, khi chạy thử nghiệm trên Windows, tiến trình bị crash do lỗi `UnicodeEncodeError` khi in các ký tự tiếng Việt có dấu ra stdout ngầm. Cần chuyển toàn bộ thông báo sang tiếng Việt không dấu để tương thích với các môi trường khác nhau.

## Thành viên 2 góp ý cho thành viên 1
Anh Tú: Phần hàm `encrypt_des_cbc` và `build_packet` trong utils hoạt động rất hoàn hảo. Tuy nhiên, trong `sender.py`, dòng thông báo cuối cùng cũng cần đổi thành tiếng Việt không dấu (ví dụ: "[+] Da gui ban ma") để đồng bộ với bộ test tự động `test_sender_receiver_local.py`, nếu không test vẫn sẽ báo lỗi Failed dù dữ liệu gửi đúng.

## Nhóm đã sửa gì sau góp ý
Nhóm đã họp và thống nhất chuẩn hóa toàn bộ các câu lệnh `print` trong cả `sender.py` và `receiver.py` sang dạng tiếng Việt không dấu (ví dụ: "Dang lang nghe", "Ban tin goc nhan duoc"). Đồng thời, đã cập nhật lại các câu lệnh `assert` trong file kiểm thử tích hợp để khớp chính xác với chuỗi log mới. Kết quả: Toàn bộ 6/6 test cases của Pytest đã Pass 100%.