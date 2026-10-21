# Selenium Tests — Canvas Phenikaa

Bộ kiểm thử giao diện tự động cho trang Canvas của Đại học Phenikaa, sử dụng Python, Selenium WebDriver và `unittest`. Các bài kiểm thử bao phủ khả năng truy cập trang, xử lý đăng nhập sai, điều hướng quên mật khẩu, đăng nhập hợp lệ và mở lịch học.

> **Lưu ý bảo mật:** Không lưu mật khẩu, cookie, token hoặc dữ liệu đăng nhập thật trong mã nguồn. Hai bài kiểm thử cần tài khoản hợp lệ chỉ chạy khi cung cấp biến môi trường tương ứng; nếu không, chúng được đánh dấu `skipped`.

## Yêu cầu

- Windows 10/11, macOS hoặc Linux
- Python 3.9 trở lên
- Google Chrome
- Selenium 4.x
- Kết nối Internet tới Canvas Phenikaa và Microsoft đăng nhập (nếu trường dùng SSO)

Selenium Manager của Selenium 4 thường tự tìm/tải ChromeDriver tương thích. Nếu môi trường không cho phép tải tự động, cài ChromeDriver phù hợp với phiên bản Chrome và thêm vào `PATH`.

## Cài đặt

Tạo môi trường ảo rồi cài Selenium:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Trên macOS/Linux, kích hoạt môi trường bằng `source .venv/bin/activate`.

## Cấu hình tài khoản (tùy chọn)

Đặt thông tin tài khoản trong môi trường của tiến trình chạy test, không ghi vào file Python hay commit lên Git.

PowerShell:

```powershell
$env:CANVAS_STUDENT_EMAIL = "email-sinh-vien"
$env:CANVAS_STUDENT_PASSWORD = "mat-khau"
```

macOS/Linux:

```bash
export CANVAS_STUDENT_EMAIL="email-sinh-vien"
export CANVAS_STUDENT_PASSWORD="mat-khau"
```

Nếu trường bật MFA, yêu cầu phê duyệt đăng nhập, CAPTCHA hoặc các xác minh tương tác khác, bài test đăng nhập có thể cần xác nhận thủ công hoặc không phù hợp chạy hoàn toàn unattended. Chỉ chạy kiểm thử trên tài khoản và hệ thống bạn được phép sử dụng.

## Chạy kiểm thử

Chạy toàn bộ suite:

```powershell
python -m unittest -v test_canvas_phenikaa.py
```

Hoặc chạy trực tiếp:

```powershell
python test_canvas_phenikaa.py
```

Mỗi test mở một phiên Chrome riêng và tự đóng trình duyệt khi hoàn tất. Không chạy song song các test trong cùng một profile trình duyệt.

## Danh sách test case

| Test | Mục tiêu | Điều kiện |
|---|---|---|
| `test_01_access_homepage` | Xác nhận truy cập Canvas hoặc trang đăng nhập Microsoft SSO | Không cần tài khoản |
| `test_02_login_invalid_credentials` | Gửi thông tin đăng nhập cố ý sai và xác nhận thông báo lỗi | Không cần tài khoản hợp lệ |
| `test_03_forgot_password_navigation` | Mở trang quên mật khẩu và xác nhận ô email khôi phục | Không cần tài khoản |
| `test_04_login_success_dashboard` | Đăng nhập và xác nhận thanh điều hướng Canvas | Cần tài khoản hợp lệ qua biến môi trường |
| `test_05_navigate_to_calendar` | Đăng nhập và mở trang lịch học | Cần tài khoản hợp lệ qua biến môi trường |

## Kết quả kiểm thử

Kết quả chạy thực tế trong môi trường phát triển Windows, Python 3.11.9, Chrome/Selenium:

```text
Ran 5 tests in 42.437s
OK (skipped=2)
```

- **3 test đạt:** truy cập trang chủ, đăng nhập sai và điều hướng quên mật khẩu.
- **2 test bỏ qua:** đăng nhập Dashboard và mở lịch học do chưa cung cấp thông tin tài khoản qua biến môi trường.

Đây là kết quả tại thời điểm chạy trong môi trường phát triển; có thể thay đổi theo kết nối mạng, trạng thái Canvas, phiên bản trình duyệt và chính sách xác thực của trường. `unittest` sẽ tổng kết số `ok`, `FAIL`, `ERROR` và `skipped` ở cuối mỗi lần chạy.

- `ok`: test hoàn tất và các assertion đạt.
- `FAIL`/`ERROR`: assertion không đạt hoặc phát sinh lỗi môi trường/định vị phần tử; xem traceback để chẩn đoán.
- `skipped`: chưa cấu hình tài khoản hợp lệ cho test yêu cầu đăng nhập.

Test đăng nhập thất bại dựa trên giao diện thực tế của Canvas và có thể cần cập nhật selector nếu website thay đổi. Các test giao diện cần Chrome có thể khởi chạy được trong môi trường hiện tại.

## Cấu trúc dự án

```text
Test_Selenium/
├── README.md
├── requirements.txt
├── .gitignore
└── test_canvas_phenikaa.py
```

## Bảo mật và giới hạn

- Không dùng mật khẩu thật trong test đăng nhập thất bại; test chỉ gửi dữ liệu giả có chủ đích.
- Không commit file `.env`, thông tin xác thực, cookies hoặc profile trình duyệt.
- Không dùng tài khoản của người khác; tuân thủ chính sách truy cập và điều khoản dịch vụ của Canvas Phenikaa.
- Đây là kiểm thử giao diện theo selector hiện tại, không thay thế kiểm thử bảo mật hay kiểm thử tải.

## Công nghệ

- [Python](https://www.python.org/)
- [Selenium](https://www.selenium.dev/)
- `unittest` (thư viện chuẩn Python)
