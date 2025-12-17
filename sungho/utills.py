import os
import time
import random
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException




# 기본 설정
BASE_LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
BASE_SIGNUP_URL ="https://accounts.elice.io/accounts/signup/method?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%3FisFirstLogin%3Dtrue&lang=en-US&org=qaproject"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
# -----------------------------
# 드라이버 생성
# -----------------------------

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    return driver
@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()

#스크린샷 설정
def save_screenshot(driver, test_type: str, name: str):
    """
    test_type: signup_email / signup_pw / signup_name
    name: TC명
    """

    test_dir = os.path.join(SCREENSHOT_DIR, test_type)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{name}_{timestamp}.png"
    filepath = os.path.join(test_dir, filename)

    driver.save_screenshot(filepath)
    print(f"📸 Screenshot saved: {filepath}")

    return filepath



# -----------------------------
# 로그인 페이지 이동
# -----------------------------
def navigate_to_login(driver):
    driver.get(BASE_LOGIN_URL)
    time.sleep(2)
# 회원가입 창 이동    
def navigate_to_signup(driver):
    driver.get(BASE_SIGNUP_URL)
    time.sleep(2)


# -----------------------------
# 요소 기다리기
# -----------------------------
def wait_for_element(driver, selector,by=By.CSS_SELECTOR,timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, f"[placeholder='{selector}']"))
        )

def wait_clickable(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by,selector))
    )

def click_element(driver, selector: str):
    """Click element with data-testid."""
    element = wait_clickable(driver, selector)
    element.click()
    return element


def type_text(driver, selector: str, text: str):
    """Type text into element with data-testid."""
    element = wait_for_element(driver, selector)
    element.clear()
    element.send_keys(text)
    return element

def generate_unique_username():
    num = random.randint(1000, 9999)
    return f"testuser{num}"

# 공통 로그인 함수
# -----------------------------
def login(driver, email, password):
    navigate_to_login(driver)
    type_text(driver, "Email", email)
    type_text(driver, "Password", password)
    click_element(driver, "[type='submit']")



#재로그인 기능
def relogin(driver,password):
    print("\n▶ 로그인 진행 중...")
    wait_clickable(driver, "[placeholder='Password']").send_keys(password)
    wait_clickable(driver, "[type='submit']").click()

    time.sleep(2)
    print("✔ 재로그인 완료")




# -----------------------------
# 로그아웃 기능
# -----------------------------
def logout(driver):
    print("\n▶ 로그아웃 진행 중...")

    wait_clickable(driver, '[data-testid="PersonIcon"]').click()
    wait_clickable(driver, "//p[contains(text(), '로그아웃')]", by=By.XPATH).click()
    welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
    assert welcome_text.is_displayed()
    print("TC17:정상적으로 로그아웃 완료")

    time.sleep(1)
#회원가입 기능 
def open_signup_page(driver):
    navigate_to_signup(driver)
    click_element(driver, "[type='button']")

def fill_signup_form(driver, email=None, password=None, name=None):
    if email is not None:
        type_text(driver, "Email", email)
    if password is not None:
        type_text(driver, "Password", password)
    if name is not None:
        type_text(driver, "Name", name)

    driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()

def submit_signup(driver):
    click_element(driver, "button[type='submit']")

def signup(driver, email, password, name):
    open_signup_page(driver)
    fill_signup_form(driver, email, password, name)
    submit_signup(driver)
    


# -----------------------------
# URL 출력
# -----------------------------
def print_current_url(driver):
    print(f"현재 URL: {driver.current_url}")



    

