import requests
from bs4 import BeautifulSoup

# 웹 페이지에서 텍스트를 가져오는 함수 정의
def get_page_text(url):
    response = requests.get(url, proxies={})
    if response.status_code == 200:
        return response.text
    else:
        print("Error: Unable to fetch the page")
        return None

# 주어진 URL
url = "https://www.du.ac.kr/submenu.do?menuUrl=I9D4yBgHJGlG1TUOf%2FpDHQ%3D%3D&"

# 웹 페이지에서 텍스트 가져오기
page_text = get_page_text(url)

if page_text:
    # BeautifulSoup을 사용하여 HTML 파싱
    soup = BeautifulSoup(page_text, "html.parser")

    # <tbody> 태그 안의 텍스트 추출
    tbody_text = soup.find('tbody').get_text().strip()  # strip() 메서드로 좌우 공백 제거

    # 개행 문자를 제거한 후 JavaScript 파일에 추가할 코드
    tbody_lines = tbody_text.split('\n')
    tbody_cleaned_lines = []

    for line in tbody_lines:
        line = line.strip()  # 좌우 공백 제거
        if line:  # 빈 줄이 아니라면 추가
            tbody_cleaned_lines.append(line)

    # 리스트를 다시 문자열로 변환
    tbody_text_cleaned = '\n'.join(tbody_cleaned_lines)

    # JavaScript 파일에 추가할 코드
    js_code = f"""
    // JavaScript 파일에 변수를 선언하고 텍스트 할당
    var tbodyData = `{tbody_text_cleaned}`;
    """

    # 기존 내용을 모두 지우고 새로운 내용 추가
    with open("scripts.js", "w", encoding="utf-8") as js_file:
        js_file.write(js_code)

    print("텍스트가 성공적으로 JavaScript 파일에 추가되었습니다.")
else:
    print("텍스트를 가져올 수 없습니다.")
