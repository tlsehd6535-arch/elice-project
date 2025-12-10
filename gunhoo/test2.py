import time
import pytest
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

USERNAME = "qa3team03@elicer.com"
PASSWORD = "@qa12345"

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat&lang=en-US&org=qaproject"
CHAT_URL = "https://qaproject.elice.io/ai-helpy-chat"

@pytest.fixture(scope="session")
def browser():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@pytest.fixture(scope="session", autouse=True)
def test_login(browser):
    # 로그인 페이지 접속
    browser.get(LOGIN_URL)
    time.sleep(1)

    # 아이디/비번 입력
    browser.find_element(By.NAME, "loginId").send_keys(USERNAME)
    browser.find_element(By.NAME, "password").send_keys(PASSWORD)

    # 로그인 버튼 클릭
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(2)

    

def test_chat_input(browser):
    # 챗봇 입력란 찾기
    textarea = browser.find_element(By.CSS_SELECTOR, "textarea[name='input']")
    
    # 입력값 전송
    textarea.send_keys("오늘 날씨 어때?")
    textarea.send_keys(Keys.ENTER)  # 엔터를 눌러 전송
    response_element = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".elice-aichat__markdown"))
    )
    
    # AI 답변 텍스트 추출
    answer = response_element.text

    # JSON으로 저장
    chat_log = {
        "question": "오늘 날씨 어때?",
        "answer": answer
    }

    with open("TC-CHAT-001.json", "w", encoding="utf-8") as f:
        json.dump(chat_log, f, ensure_ascii=False, indent=4)

    print("AI 답변 저장 완료:", answer)
    