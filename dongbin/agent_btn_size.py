import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

from utils.credentials import USER_EMAIL, USER_PASSWORD
from utils.driver_setup import login_driver
from utils.login_module import perform_login

LOGIN_URL = "https://accounts.elice.io/accounts/signin/me?continue_to=https%3A%2F%2Fqaproject.elice.io%2Fai-helpy-chat%2Fagents&lang=en-US&org=qaproject"
MY_AGENTS_BUTTON = (By.XPATH, "//a[@href='/ai-helpy-chat/agents/mine']")

# 에이전트 카드 관련 로케이터
AGENT_CARDS = (By.XPATH, "//a[contains(@class, 'MuiCard-root')]")
DRAFT_STATUS = (By.XPATH, ".//span[normalize-space()='초안']")
DELETE_BUTTON_IN_CARD = (By.XPATH, ".//button[./*[name()='svg' and @data-icon='trash']]")
CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[normalize-space()='삭제']")

driver = login_driver(LOGIN_URL) 
driver.maximize_window()

try:
    perform_login(driver, USER_EMAIL, USER_PASSWORD)
    print(f"로그인 후 현재 URL: {driver.current_url}") 

    # 1. '내 에이전트' 페이지로 이동
    wait = WebDriverWait(driver, 10)
    agent_btn = wait.until(EC.element_to_be_clickable(MY_AGENTS_BUTTON))
    agent_btn.click()
    wait.until(EC.url_to_be("https://qaproject.elice.io/ai-helpy-chat/agents/mine"))
    print("\n--- 초안 에이전트 삭제 프로세스 시작 ---")
    print("[INFO] '/mine' 페이지로 이동 완료.")

    time.sleep(2) # 페이지 로딩 및 DOM 안정화 대기

    deleted_count = 0
    
    # 2. 모든 카드를 찾고, 초안인 경우 삭제를 시도합니다.
    # 주의: 요소를 삭제하면 DOM 구조가 바뀌므로, 무한 루프를 돌지 않도록 재검색 루프를 사용합니다.
    
    while True:
        try:
            # 현재 페이지의 모든 에이전트 카드를 다시 찾습니다. (Stale 방지)
            cards = driver.find_elements(*AGENT_CARDS)
        except StaleElementReferenceException:
            # 드물게 발생하는 StaleElement 예외 처리 (다시 시도)
            continue
            
        draft_cards_count = 0
        target_draft_card = None

        # 초안 카드가 남아 있는지 확인
        for card in cards:
            try:
                # 카드 내부에 '초안' 상태 태그가 있는지 확인
                if card.find_elements(*DRAFT_STATUS):
                    target_draft_card = card
                    draft_cards_count += 1
                    break # 첫 번째 초안만 찾으면 루프 종료
            except StaleElementReferenceException:
                continue # 다음 카드로

        if not target_draft_card:
            print(f"\n[INFO] 초안 상태인 에이전트 카드를 더 이상 찾지 못했습니다.")
            break # 초안 카드가 없으면 무한 루프 종료
            
        # 3. 삭제 버튼 클릭
        try:
            delete_btn = target_draft_card.find_element(*DELETE_BUTTON_IN_CARD)
            delete_btn.click()
            print(f"[SUCCESS] 초안 카드 내 삭제 버튼 클릭.")

            # 4. 팝업에서 최종 삭제 확인 버튼 클릭 (대기 시간 5초)
            wait_short = WebDriverWait(driver, 5)
            confirm_btn = wait_short.until(EC.element_to_be_clickable(CONFIRM_DELETE_BUTTON))
            confirm_btn.click()
            print("[SUCCESS] 최종 삭제 확인 버튼 클릭 완료.")
            
            deleted_count += 1
            # 삭제 후 목록 업데이트를 위해 잠시 대기
            time.sleep(1.5) 

        except TimeoutException:
            print("[FAILURE] 삭제 확인 팝업이 나타나지 않거나 버튼을 찾을 수 없습니다. (스킵)")
            break
        except Exception as e:
            print(f"[CRITICAL ERROR] 삭제 중 예상치 못한 오류 발생: {e.__class__.__name__}")
            break
            
    print(f"\n[PASS] 총 {deleted_count}개의 초안 에이전트를 성공적으로 삭제했습니다.")

except Exception as e:
    print(f"\n[CRITICAL ERROR] 자동화 프로세스 중 예상치 못한 오류 발생.")
    print(f"오류 클래스: {e.__class__.__name__}")
    print(f"오류 메시지: {e}")
    
finally:
    if 'driver' in locals() and driver:
        time.sleep(3) 
        driver.quit()
        print("\n[INFO] 드라이버 종료.")

