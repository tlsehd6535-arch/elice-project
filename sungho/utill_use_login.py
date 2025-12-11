from utills import *

driver = get_driver()

# 1) 정상 로그인 → 로그아웃
navigate_to_login(driver)
login(driver)
logout(driver)   # 이 안에서 driver.quit() 하지 말아야 여러 테스트 가능
print("1. 가입된 계정 로그인 테스트 완료")



# # 2) 잘못된 비밀번호 테스트
# test_wrong_password(driver, "qa3team03@elicer.com")
# driver.quit()
# print("2.잘못된 비밀번호 테스트 완료")

# driver = get_driver()

# # 3) 짧은 비밀번호 테스트
# test_short_password(driver, "qa3team03@elicer.com")
# driver.quit()
# print("3. 짧은 비밀번호 테스트 완료")



# # # 4) 존재하지 않는 계정 테스트
# # test_fake_account(driver)
# # driver.quit()
