import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))

project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from utils.driver_setup import login_driver
from utils.login_module import perform_login

agent_rule = "길 찾기용 에이전트 입니다.  서울 위주 대중교통을 안내합니다"
file_name = "elice_logo.png"
file_path = os.path.join(current_dir, file_name)

USER_EMAIL = "qa3team03@elicer.com"  
USER_PASSWORD = "@qa12345" 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
STARTER_FIELD = '//input[@placeholder="이 에이전트의 시작 대화를 입력하세요"]'

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 
time.sleep(5)

wait = WebDriverWait(driver, 10)
print("--- 에이전트 생성 프로세스 시작 ---")
    
    #만들기 버튼 클릭
try:
    agent_make_btn = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
   
    agent_make_btn.click()
    print("[SUCCESS]'만들기'버튼 클릭 성공.")
       
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )        
    time.sleep(1)
    
    #시작 대화 입력
    agent_starter_field_1 = driver.find_element(By.XPATH, STARTER_FIELD)
    agent_starter_field_1.send_keys("대중교통")
    print(f"[SUCCESS] 시작 대화 입력 성공!")
    
    time.sleep(1)
    
    def two_elements_visible(driver):
        elements = driver.find_elements(By.XPATH, STARTER_FIELD)
        if len(elements) >= 2 and elements[1].is_displayed():
            return elements[1]
        return False
    second_field = WebDriverWait(driver, 5).until(two_elements_visible)
    
    if second_field:
        print("\n[SUCCESS!]")
        print("숨겨져 있던 두 번째 시작 대화 입력 필드가 성공적으로 화면에 나타났습니다.")
        
except TimeoutException:
    print("\n[FAILURE]")
    print(f"5초 내에 두 번째 시작 대화 필드({STARTER_FIELD})가 화면에 나타나지 않았습니다.")
    
except NoSuchElementException:
    print("\n[CRITICAL ERROR] 첫 번째 시작 대화 필드 자체를 찾지 못했습니다.")
    
    
except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        driver.quit()
        print("\n[INFO] 드라이버 종료.")