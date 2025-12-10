import os
import sys
import time
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리 (프로젝트 루트, 예: .../qa03)를 PATH에 추가
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from utils.driver_setup import login_driver
from utils.login_module import perform_login

VALID_NAME = "동빈"
LONG_NAME = "0"*101
VALIDATION_MESSAGE_TEXT = "이름은 최대 100자입니다"

LONG_TEXT = "0"*301
VALID_TEXT = "길 찾기 에이전트 입니다"

USER_EMAIL = "qa3team03@elicer.com"  
USER_PASSWORD = "@qa12345" 
LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

# 2. 로그인 실행
perform_login(driver, USER_EMAIL, USER_PASSWORD)
print(f"로그인 후 현재 URL: {driver.current_url}") 
time.sleep(5)

wait = WebDriverWait(driver, 10)
print("--- 에이전트 생성 프로세스 시작 ---")

try:
    agent_make_btn = wait.until(
      EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='만들기']")))
   
    agent_make_btn.click()
    print("[SUCCESS]'만들기'버튼 클릭 성공.")
       
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.NAME, "name"))
    )
    
    agent_make_name.send_keys(LONG_NAME)
    print(f"[SUCCESS] 1차 이름 입력 성공! ({len(LONG_NAME)}자 입력 완료)")
    
    print(f"[VALIDATION SUCCESS] 길이 제한 메시지 확인: '{VALIDATION_MESSAGE_TEXT}'")
    
    validation_message = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{VALIDATION_MESSAGE_TEXT}')]"))
    )
    
    time.sleep(1)
    
    validation_message = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{VALIDATION_MESSAGE_TEXT}')]"))
    )
    
    time.sleep(2)
    
    agent_make_name.send_keys(Keys.CONTROL, "a")
    agent_make_name.send_keys(Keys.DELETE)
    
    agent_make_name.send_keys(VALID_NAME)
    print("[SUCCESS] 2차 이름 입력 성공.")
    
    time.sleep(2) # 최종 결과 확인을 위한 대기
    
    agent_make_name = wait.until(
        EC.visibility_of_element_located((By.NAME, "description"))
    )
   
    agent_make_name.send_keys(LONG_TEXT)
    print(f"[SUCCESS] 1차 한줄 소개 입력 성공! ({len(LONG_TEXT)}자 입력 완료)")
    
    print(f"[VALIDATION SUCCESS] 길이 제한 메시지 확인: '{VALIDATION_MESSAGE_TEXT}'")
    
    validation_message = wait.until(
        EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{VALIDATION_MESSAGE_TEXT}')]"))
    )
    
    time.sleep(1)   
    
    agent_make_name.send_keys(Keys.CONTROL, "a")
    agent_make_name.send_keys(Keys.DELETE)
    
    agent_make_name.send_keys(VALID_TEXT)
    print("[SUCCESS] 2차 한줄 소개 입력 성공.")
    
    time.sleep(2) # 최종 결과 확인을 위한 대기
    
except Exception as e:
    print(f"[ERROR] '만들기' 버튼 찾기/클릭 실패: {e}")
    
    
    

