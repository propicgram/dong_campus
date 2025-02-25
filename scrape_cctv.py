import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def get_cctv_video_url():
    # ✅ Chrome 옵션 설정
    options = Options()
    options.add_argument("--headless")  # 화면 없이 실행
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # ✅ User-Agent 추가 (사이트 차단 우회)
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    # ✅ WebDriver 실행
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # ✅ CCTV 페이지 로드
    url = "https://www.utic.go.kr/jsp/map/cctvStream.jsp?cctvid=L900033&cctvname=%25EB%258F%2599%25EC%2584%259C%25EC%259A%25B8%25EB%258C%2580%25EC%2582%25AC%25EA%25B1%25B0%25EB%25A6%25AC&kind=EE&cctvip=60204&cctvch=undefined&id=undefined&cctvpasswd=undefined&cctvport=undefined&minX=127.11061562586477&minY=37.44630582546269&maxX=127.14100884393808&maxY=37.47160131581751"
    driver.get(url)

    try:
        # ✅ WebDriverWait을 사용하여 요소가 나타날 때까지 대기
        video_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "vid_html5_api"))
        )

        # ✅ JavaScript 실행하여 src 가져오기 (동적 로딩 대응)
        video_src = driver.execute_script("return document.getElementById('vid_html5_api')?.getAttribute('src');")

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
    # ✅ HTML 파일 경로
    html_file = "index.html"

    # ✅ 파일이 존재하는지 확인
    if not os.path.exists(html_file):
        print(f"🚨 HTML 파일을 찾을 수 없음: {html_file}")
        return

    # ✅ 기존 HTML 파일 읽기
    with open(html_file, "r", encoding="utf-8") as file:
        html_content = file.read()

    # ✅ iframe의 src 값을 새로운 CCTV 링크로 변경
    new_html_content = re.sub(r'<iframe src="[^"]+"', f'<iframe src="{new_cctv_url}"', html_content)

    # ✅ 변경된 HTML 저장
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(new_html_content)

    print("✅ HTML 파일이 성공적으로 업데이트되었습니다.")

if __name__ == "__main__":
    new_cctv_url = get_cctv_video_url()
    if new_cctv_url:
        update_html_with_new_cctv_link(new_cctv_url)
