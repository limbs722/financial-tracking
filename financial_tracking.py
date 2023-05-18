"""
  - title: Financial Tracking
  - Desc: 실행 시 ticker를 입력받아 야후 파이낸셜 웹페이지 뉴스 크롤링 하기
"""
from argparse import ArgumentParser as Parser
from bs4 import BeautifulSoup
import requests
import json

def handler(ticker):
  headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
  }

  url = f"https://finance.yahoo.com/quote/{ticker}/press-release"
  response = requests.get(url, headers=headers)
  data_list = []

  if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    all_elements = soup.select("div#Main li.js-stream-content.Pos\\(r\\)")

    for a_el in all_elements:
      source_element = a_el.select_one(".C\\(\\#959595\\)")
      source = source_element.text if source_element else None

      h3_element = a_el.select_one("h3.Mb\\(5px\\)")
      if h3_element:
        title_element = h3_element.select_one("a")
        if title_element:
          title = title_element.text
          link = title_element.get("href")
          data_list.append({"title": title, "source": source, "link": link})

  save_file(data_list, ticker)

def save_file(data, ticker):
  with open(f'./{ticker}.json', 'w', newline = '') as f:
    json.dump(data, f, indent = 4, ensure_ascii=False)

def main():
    parser = Parser()
    parser.add_argument('ticker')
    args = parser.parse_args()
    print(f'input ticker : {args.ticker}')
    handler(args.ticker)

if __name__ == '__main__':
  main()