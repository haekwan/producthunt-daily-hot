import os
import requests
from datetime import datetime, timedelta, timezone
from openai import OpenAI
from bs4 import BeautifulSoup
import pytz

# OpenAI 클라이언트 인스턴스 생성
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

producthunt_client_id = os.getenv('PRODUCTHUNT_CLIENT_ID')
producthunt_client_secret = os.getenv('PRODUCTHUNT_CLIENT_SECRET')

class Product:
    def __init__(self, id: str, name: str, tagline: str, description: str, votesCount: int, createdAt: str, featuredAt: str, website: str, url: str, **kwargs):
        self.name = name
        self.tagline = tagline
        self.description = description
        self.votes_count = votesCount
        self.created_at = self.convert_to_seoul_time(createdAt)
        self.featured = "예" if featuredAt else "아니오"
        self.website = website
        self.url = url
        self.og_image_url = self.fetch_og_image_url()
        self.keyword = self.generate_keywords()
        self.translated_tagline = self.translate_text(self.tagline)
        self.translated_description = self.translate_text(self.description)

    def fetch_og_image_url(self) -> str:
        """제품의 Open Graph 이미지 URL 가져오기"""
        response = requests.get(self.url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            og_image = soup.find("meta", property="og:image")
            if og_image:
                return og_image["content"]
        return ""

    def generate_keywords(self) -> str:
        """제품의 키워드를 생성하여 한 줄로 표시 (영어 쉼표로 구분)"""
        prompt = f"다음 내용을 바탕으로 적절한 한국어 키워드를 생성해 주세요. 키워드는 영어 쉼표로 구분되어야 합니다:\n\n제품 이름: {self.name}\n\n슬로건: {self.tagline}\n\n설명: {self.description}"
        
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "제품 정보를 기반으로 적절한 한국어 키워드를 생성하세요. 키워드는 영어 쉼표로 구분되어 한 줄에 표시해야 합니다."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=50,
                temperature=0.7,
            )
            keywords = response.choices[0].message.content.strip()
            if ',' not in keywords:
                keywords = ', '.join(keywords.split())
            return keywords
        except Exception as e:
            print(f"키워드 생성 중 오류 발생: {e}")
            return "키워드 없음"

    def translate_text(self, text: str) -> str:
        """OpenAI를 사용하여 텍스트 내용을 번역합니다."""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "당신은 세계 최고의 번역 도구입니다. 영어와 한국어를 능숙하게 번역하는 전문가입니다. IT 전문 용어나 표현을 쉽고 자연스러운 한국어로 번역해 주세요. 아래 내용을 한국어로 번역하세요."},
                    {"role": "user", "content": text},
                ],
                max_tokens=500,
                temperature=0.7,
            )
            translated_text = response.choices[0].message.content.strip()
            return translated_text
        except Exception as e:
            print(f"번역 중 오류 발생: {e}")
            return text

    def convert_to_seoul_time(self, utc_time_str: str) -> str:
        """UTC 시간을 서울 시간으로 변환합니다."""
        utc_time = datetime.strptime(utc_time_str, '%Y-%m-%dT%H:%M:%SZ')
        seoul_tz = pytz.timezone('Asia/Seoul')
        seoul_time = utc_time.replace(tzinfo=pytz.utc).astimezone(seoul_tz)
        return seoul_time.strftime('%Y년%m월%d일 %p%I:%M (서울 시간)')

    def to_markdown(self, rank: int) -> str:
        """제품 데이터를 Markdown 형식으로 반환합니다."""
        og_image_markdown = f"![{self.name}]({self.og_image_url})"
        return (
            f"## [{rank}. {self.name}]({self.url})\n\n"
            f"**슬로건:**\n{self.translated_tagline}\n\n"
            f"**소개:**\n{self.translated_description}\n\n"
            f"**제품 웹사이트:**\n[바로 방문]({self.website})\n\n"
            f"**프로덕트 헌트:**\n[View on Product Hunt]({self.url})\n\n"
            f"{og_image_markdown}\n\n"
            f"**키워드:** {self.keyword}\n\n"
            f"**투표수:** 🔺{self.votes_count}\n\n"
            f"**피처 여부:** {self.featured}\n\n"
            f"**발표 시간:** {self.created_at}\n\n"
            f"---\n\n"
        )

def get_producthunt_token():
    """client_id와 client_secret을 사용하여 Product Hunt의 access_token을 가져옵니다."""
    url = "https://api.producthunt.com/v2/oauth/token"
    payload = {
        "client_id": producthunt_client_id,
        "client_secret": producthunt_client_secret,
        "grant_type": "client_credentials",
    }

    headers = {
        "Content-Type": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"access token을 가져오는데 실패했습니다: {response.status_code}, {response.text}")

    token = response.json().get("access_token")
    return token

def fetch_product_hunt_data():
    """Product Hunt에서 전날의 Top 30 데이터를 가져옵니다."""
    token = get_producthunt_token()
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')
    url = "https://api.producthunt.com/v2/api/graphql"
    headers = {"Authorization": f"Bearer {token}"}

    base_query = """
    {
      posts(order: VOTES, postedAfter: "%sT00:00:00Z", postedBefore: "%sT23:59:59Z", after: "%s") {
        nodes {
          id
          name
          tagline
          description
          votesCount
          createdAt
          featuredAt
          website
          url
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
    """

    all_posts = []
    has_next_page = True
    cursor = ""

    while has_next_page and len(all_posts) < 30:
        query = base_query % (date_str, date_str, cursor)
        response = requests.post(url, headers=headers, json={"query": query})

        if response.status_code != 200:
            raise Exception(f"Product Hunt 데이터 가져오기에 실패했습니다: {response.status_code}, {response.text}")

        data = response.json()['data']['posts']
        posts = data['nodes']
        all_posts.extend(posts)

        has_next_page = data['pageInfo']['hasNextPage']
        cursor = data['pageInfo']['endCursor']

    # 상위 30개의 제품만 반환합니다.
    return [Product(**post) for post in sorted(all_posts, key=lambda x: x['votesCount'], reverse=True)[:30]]

def generate_markdown(products, date_str):
    """Markdown 내용을 생성하여 data 디렉토리에 저장합니다."""
    markdown_content = f"# PH 오늘의 인기 제품 | {date_str}\n\n"
    for rank, product in enumerate(products, 1):
        markdown_content += product.to_markdown(rank)

    # data 디렉토리가 없으면 생성합니다.
    os.makedirs('data', exist_ok=True)

    # data 디렉토리에 파일 저장
    file_name = f"data/PH-daily-{date_str}.md"
    
    # 파일이 이미 존재하면 덮어씁니다.
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(markdown_content)
    print(f"파일 {file_name} 생성 및 덮어쓰기 완료.")

def main():
    # 어제 날짜 가져오기 및 포맷팅
    yesterday = datetime.now(timezone.utc) - timedelta(days=1)
    date_str = yesterday.strftime('%Y-%m-%d')

    # Product Hunt 데이터 가져오기
    products = fetch_product_hunt_data()

    # Markdown 파일 생성
    generate_markdown(products, date_str)

if __name__ == "__main__":
    main()
