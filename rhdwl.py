import requests
from bs4 import BeautifulSoup

url = "https://www.du.ac.kr/submenu.do?menuUrl=VYlDwaWjKSwAGszRXT2bcg%3d%3d"

# 웹 페이지에 요청을 보내고 HTML을 가져오기
response = requests.get(url)
html_content = response.text

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, "html.parser")

# 테이블에서 각각의 title left 클래스를 가진 td 요소들을 찾기
td_elements = soup.find_all("td", class_="title left")

# 텍스트를 담을 변수 초기화
text_content = ""

# 각 td 요소의 텍스트를 변수에 추가
for td in td_elements:
    text_content += td.get_text(strip=True) + "\n"

# 기존의 ./js 파일 내용을 제거하고 새로운 내용을 저장
with open("web_content.js", "w", encoding="utf-8") as js_file:
    js_file.write("var webContent = `\n")
    js_file.write(text_content)
    js_file.write("`;\n")
