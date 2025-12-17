import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ChatBotTester:
    """
    챗봇 테스트를 위해 공통으로 사용하는 동작 모음 클래스.
    메시지 전송, 답변 대기, 새 대화 버튼 클릭 등을 담당한다.
    """

    def __init__(self, browser):
        self.browser = browser

    # ------------------------------------------------
    # 1. 메시지 전송
    # ------------------------------------------------
    def send_message(self, message):
        for idx, line in enumerate(message.split("\n")):        # idx = 줄 번호, line = 실제 텍스트, enumerate = 인덱스와 실제 줄을 동시에 가져옴
            textarea = WebDriverWait(self.browser, 10).until(       # 매번 한줄의 텍스트마다 입력창 찾음으로써 안정화
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea[name='input']")
                )
            )

            textarea.send_keys(line)

            # 마지막 줄이 아니면 줄바꿈만
            if idx < len(message.split("\n")) - 1:          
                textarea.send_keys(Keys.SHIFT, Keys.ENTER)

        # 마지막에 전송
        textarea = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "textarea[name='input']")
            )
        )
        textarea.send_keys(Keys.ENTER)

    # ------------------------------------------------
    # 2. 모든 답변 요소 가져오기
    # ------------------------------------------------
    def get_all_answers(self):
        return self.browser.find_elements(
            By.CSS_SELECTOR, ".elice-aichat__markdown"
        )

    # ------------------------------------------------
    # 3. 답변 대기 (멈춤 방지 핵심 로직)
    # ------------------------------------------------
    def wait_for_answer(
        self,
        prev_answer_count,
        spinner_selector="svg.MuiCircularProgress-svg",
        answer_selector=".elice-aichat__markdown",
        min_wait_time=5.0,
        stable_duration=1.0,
        max_total_wait=60.0,
    ):
        start_time = time.time()

        # 1️⃣ 최소 대기 시간 (너무 빠른 종료 방지)
        time.sleep(min_wait_time)
        print("⏳ 최소 대기 시간 경과")

        # 2️⃣ 스피너가 있다면 사라질 때까지 (있을 때만)
        try:
            WebDriverWait(self.browser, 3).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            WebDriverWait(self.browser, 30).until_not(
                EC.presence_of_element_located((By.CSS_SELECTOR, spinner_selector))
            )
            print("⏳ 스피너 종료 감지")
        except Exception:
            print("ℹ️ 스피너 미감지 (즉시 답변)")

        # 3️⃣ 새 답변 DOM 증가 감지 (실패 허용)
        try:
            WebDriverWait(self.browser, 30).until(
                lambda d: len(d.find_elements(By.CSS_SELECTOR, answer_selector))    # d는 브라우저 객체, lambda 는 일회용 조건함수
                > prev_answer_count                                                 # 이전 답변보다 많으면 새 답변 DOM이 추가됨
            )
            print("⏳ 새 답변 DOM 감지")
        except Exception:
            print("⚠️ 답변 DOM 증가 감지 실패 → 기존 답변 사용")

        # 4️⃣ 마지막 답변 텍스트 안정화 (타임아웃 필수)
        answers = self.get_all_answers()
        if not answers:
            print("⚠️ 답변 요소 없음")
            return

        
        prev_text = ""                                      # 이전 확인 시점 텍스트 저장
        stable_start = None                                 # 텍스트 안 변하는 시점 시작 기록
        deadline = time.time() + max_total_wait             # 최대 대기 시간

        while time.time() < deadline:                       
            answers = self.get_all_answers()                # 루프에서 get_all_answers 를 호출, DOM 갱신 감지
            if not answers:                                 # 답변 없다면 대기 후 다시 확인
                time.sleep(0.3)
                continue

            last_answer = answers[-1]                       # 역순으로 넣어서 가장 최근 답변
            current_text = last_answer.text.strip()         # 텍스트 추출 후 앞뒤 공백 제거

            if current_text != prev_text:                   # 이전 확인 시점과 다르면
                prev_text = current_text                    # 현재 텍스트로 변경
                stable_start = time.time()                  # 안정화 시작 시간 기록
            else:                                                                   # 이전 텍스트와 같다면 (변동없다면) 
                if stable_start and time.time() - stable_start >= stable_duration:  # 이어서 상태가 stable_duration 이상이라면 답변 안정화 완료
                    print("✅ 답변 안정화 완료")                                     
                    return

            time.sleep(0.3)

        print("⚠️ 답변 안정화 타임아웃 → 강제 진행")

    # ------------------------------------------------
    # 4. 마지막 답변 가져오기
    # ------------------------------------------------
    def get_last_answer(self):
        answers = self.get_all_answers()
        return answers[-1].text if answers else ""          # 답변 없다면 빈 문자열 "" 을 반환, 테스트 코드가 지속되게 함

    # ------------------------------------------------
    # 5. 새 대화 시작 버튼 클릭
    # ------------------------------------------------
    def new_chat(self):
        try:
            btn = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//a[.//span[contains(text(), '새 대화')]]")
                )
            )
            btn.click()

            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea[name='input']")
                )
            )
            print("🆕 새 대화 시작")
        except Exception as e:
            print("❌ 새 대화 버튼 클릭 실패:", e)      # e 는 실제 발생한 에러 객체이며 안의 에러 로그를 보여줌



    