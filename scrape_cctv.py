import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_cctv_video_url():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # 화면 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    url = "https://www.utic.go.kr/jsp/map/cctvStream.jsp?cctvid=L900033&cctvname=%25EB%258F%2599%25EC%2584%259C%25EC%259A%25B8%25EB%258C%2580%25EC%2582%25AC%25EA%25B1%25B0%25EB%25A6%25AC&kind=EE&cctvip=60204&cctvch=undefined&id=undefined&cctvpasswd=undefined&cctvport=undefined&minX=127.1158589926679&minY=37.44945412462696&maxX=127.13769799468838&maxY=37.46908224990571"
    driver.get(url)

    time.sleep(5)  # 페이지 로딩 대기

    try:
        video_element = driver.find_element(By.ID, "vid_html5_api")
        video_src = video_element.get_attribute("src")

        if video_src:
            print("✅ 최신 CCTV 영상 링크:", video_src)
            return video_src
        else:
            print("🚨 CCTV 영상 링크를 찾을 수 없음")
            return None

    except Exception as e:
        print("❌ 오류 발생:", str(e))
        return None

    finally:
        driver.quit()

def update_html_with_new_cctv_link(new_cctv_url):

    html_file = "dong_campus/index.html"

    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()


    new_html_content = re.sub(r'<iframe src="[^"]+"', f'<iframe src="{new_cctv_url}"', html_content)

    with open(html_file, "w", encoding="utf-8") as file:
        file.write(new_html_content)

    print("✅ HTML 파일이 성공적으로 업데이트되었습니다.")

if __name__ == "__main__":
    new_cctv_url = get_cctv_video_url()
    if new_cctv_url:
        update_html_with_new_cctv_link(new_cctv_url)
