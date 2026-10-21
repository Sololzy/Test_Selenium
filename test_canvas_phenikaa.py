import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =====================================================================
# Cấu hình tùy chọn qua biến môi trường; không đưa thông tin xác thực vào Git.
# =====================================================================
STUDENT_EMAIL = os.getenv("CANVAS_STUDENT_EMAIL", "")
STUDENT_PASSWORD = os.getenv("CANVAS_STUDENT_PASSWORD", "")

BASE_URL = "https://canvas.phenikaa-uni.edu.vn/"
CANVAS_DIRECT_LOGIN_URL = "https://canvas.phenikaa-uni.edu.vn/login/canvas"


class CanvasPhenikaaTests(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def login_canvas(self):
        """Hàm hỗ trợ đăng nhập (Tự động nhận diện Microsoft SSO hoặc Canvas Login)"""
        if not STUDENT_EMAIL or not STUDENT_PASSWORD:
            self.skipTest("Cần đặt CANVAS_STUDENT_EMAIL và CANVAS_STUDENT_PASSWORD.")

        self.driver.get(BASE_URL)
        time.sleep(2)

        # Trường hợp 1: Chuyển hướng sang trang đăng nhập Microsoft SSO
        if "login.microsoftonline.com" in self.driver.current_url:
            email_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "loginfmt")))
            email_input.send_keys(STUDENT_EMAIL)
            self.driver.find_element(By.ID, "idSIButton9").click()

            pass_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "passwd")))
            pass_input.send_keys(STUDENT_PASSWORD)
            time.sleep(1)
            self.driver.find_element(By.ID, "idSIButton9").click()

            # Xác nhận "Stay signed in?" (Chọn Yes)
            try:
                yes_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
                yes_btn.click()
            except Exception:
                pass

        # Trường hợp 2: Đăng nhập qua form gốc của Canvas
        else:
            user_input = self.wait.until(
                EC.visibility_of_element_located((By.ID, "pseudonym_session_unique_id"))
            )
            pass_input = self.driver.find_element(By.ID, "pseudonym_session_password")
            user_input.send_keys(STUDENT_EMAIL)
            pass_input.send_keys(STUDENT_PASSWORD)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    # -----------------------------------------------------------------
    # Test Case 01: Kiểm tra truy cập trang chủ Canvas Phenikaa
    # -----------------------------------------------------------------
    def test_01_access_homepage(self):
        self.driver.get(BASE_URL)
        self.wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        current_url = self.driver.current_url
        # Xác nhận trang tải thành công (ở trang đăng nhập Canvas hoặc Microsoft SSO)
        self.assertTrue(
            "phenikaa-uni.edu.vn" in current_url or "microsoftonline.com" in current_url,
            "Không thể truy cập trang đăng nhập Canvas Phenikaa!"
        )

    # -----------------------------------------------------------------
    # Test Case 02: Kiểm thử đăng nhập thất bại với tài khoản sai
    # -----------------------------------------------------------------
    def test_02_login_invalid_credentials(self):
        self.driver.get(CANVAS_DIRECT_LOGIN_URL)
        user_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "pseudonym_session_unique_id"))
        )
        pass_input = self.driver.find_element(By.ID, "pseudonym_session_password")

        user_input.send_keys("sinhvien_test_sai@st.phenikaa-uni.edu.vn")
        pass_input.send_keys("MatKhauSai123!")
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        # Kiểm tra thông báo lỗi xuất hiện
        error_box = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "ic-flash-error"))
        )
        self.assertTrue(error_box.is_displayed(), "Không hiển thị thông báo lỗi khi nhập sai!")

    # -----------------------------------------------------------------
    # Test Case 03: Kiểm thử chức năng Quên mật khẩu (Forgot Password)
    # -----------------------------------------------------------------
    def test_03_forgot_password_navigation(self):
        self.driver.get(CANVAS_DIRECT_LOGIN_URL)
        forgot_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "login_forgot_password"))
        )
        forgot_link.click()

        # Kiểm tra ô nhập email khôi phục mật khẩu hiển thị
        reset_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, "pseudonym_session_unique_id_forgot"))
        )
        self.assertTrue(reset_input.is_displayed(), "Form khôi phục mật khẩu không hiển thị!")

    # -----------------------------------------------------------------
    # Test Case 04: Kiểm thử đăng nhập thành công vào Dashboard
    # -----------------------------------------------------------------
    def test_04_login_success_dashboard(self):
        self.login_canvas()
        # Chờ thanh điều hướng chính của Canvas xuất hiện sau khi đăng nhập
        global_nav = self.wait.until(
            EC.visibility_of_element_located((By.ID, "menu"))
        )
        self.assertTrue(global_nav.is_displayed(), "Đăng nhập vào Dashboard thất bại!")
        self.assertIn("canvas.phenikaa-uni.edu.vn", self.driver.current_url)

    # -----------------------------------------------------------------
    # Test Case 05: Kiểm thử điều hướng sang trang Lịch học (Calendar)
    # -----------------------------------------------------------------
    def test_05_navigate_to_calendar(self):
        self.login_canvas()
        calendar_link = self.wait.until(
            EC.element_to_be_clickable((By.ID, "global_nav_calendar_link"))
        )
        calendar_link.click()

        self.wait.until(EC.url_contains("/calendar"))
        self.assertIn("/calendar", self.driver.current_url, "Không chuyển sang được trang Lịch học!")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()