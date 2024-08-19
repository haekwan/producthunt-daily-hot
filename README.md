
# Product Hunt 매일 한국어 인기 목록

[English](README.en.md) | [한국어](README.md)

![License](https://img.shields.io/github/license/ViggoZ/producthunt-daily-hot) ![Python](https://img.shields.io/badge/python-3.x-blue)

Product Hunt 매일 인기 목록은 GitHub Action을 기반으로 한 자동화 도구로, 매일 정해진 시간에 Product Hunt의 인기 제품 목록 Markdown 파일을 생성하고 자동으로 GitHub 리포지토리에 제출합니다. 이 프로젝트는 사용자가 매일 Product Hunt의 인기 목록을 빠르게 확인하고, 더 자세한 제품 정보를 제공하는 데 목적이 있습니다.

목록은 매일 오후 4시에 자동으로 업데이트되며, [🌐 여기에서 확인할 수 있습니다](https://decohack.com/category/producthunt/)。

## 미리보기

![Preview](./preview.gif)

## 기능 개요

- **자동 데이터 수집**: 매일 전날의 Product Hunt Top 30 제품 데이터를 자동으로 수집합니다.
- **키워드 생성**: 간결하고 이해하기 쉬운 한국어 키워드를 생성하여 사용자가 제품 내용을 더 잘 이해할 수 있도록 돕습니다.
- **고품질 번역**: OpenAI의 GPT-4 모델을 사용하여 제품 설명을 고품질로 번역합니다.
- **Markdown 파일 생성**: 제품 데이터, 키워드 및 번역된 설명을 포함한 Markdown 파일을 생성하여 웹사이트나 다른 플랫폼에 쉽게 게시할 수 있습니다.
- **매일 자동화**: GitHub Actions를 통해 매일 Markdown 파일을 자동으로 생성하고 제출합니다.
- **구성 가능한 워크플로우**: 수동으로 트리거하거나 GitHub Actions를 통해 정기적으로 콘텐츠를 생성할 수 있습니다.
- **유연한 커스터마이징**: 스크립트를 쉽게 확장하거나 수정할 수 있으며, 추가 제품 세부 정보 포함이나 파일 형식 조정도 가능합니다.

## 빠른 시작

### 사전 준비

- Python 3.x
- GitHub 계정 및 리포지토리
- OpenAI API 키
- Product Hunt API 인증 정보

### 설치

1. **리포지토리 클론:**

```bash
git clone https://github.com/ViggoZ/producthunt-daily-hot.git
cd producthunt-daily-hot
```

2. **Python 의존성 설치:**

시스템에 Python 3.x가 설치되어 있는지 확인한 후, 필요한 의존성을 설치합니다:

```bash
pip install -r requirements.txt
```

### 설정

1. **GitHub Secrets:**

   GitHub 리포지토리에 다음 Secrets를 추가하세요:

   - `OPENAI_API_KEY`: OpenAI API 키.
   - `PRODUCTHUNT_CLIENT_ID`: Product Hunt API 클라이언트 ID.
   - `PRODUCTHUNT_CLIENT_SECRET`: Product Hunt API 클라이언트 비밀 키.
   - `PAT`: 리포지토리에 변경 사항을 푸시하기 위한 개인 액세스 토큰.

2. **GitHub Actions 워크플로우:**

   워크플로우는 `.github/workflows/generate_markdown.yml`에 정의되어 있습니다. 이 워크플로우는 매일 UTC 시간 08:01(한국 시간 16:01)에 자동으로 실행되며, 수동으로도 트리거할 수 있습니다.

### 사용 방법

설정이 완료되면 GitHub Action이 Product Hunt 매일 인기 제품이 포함된 Markdown 파일을 자동으로 생성하고 제출합니다. 파일은 `data/` 디렉토리에 저장됩니다.

### 커스터마이징

- `scripts/product_hunt_list_to_md.py` 파일을 수정하여 생성되는 파일의 형식을 커스터마이징하거나 추가 내용을 포함시킬 수 있습니다.
- 필요에 따라 `.github/workflows/generate_markdown.yml`에서 예약 작업의 실행 시간을 조정할 수 있습니다.

### 예시 출력

생성된 파일은 `data/` 디렉토리에 저장됩니다. 각 파일은 `PH-daily-YYYY-MM-DD.md` 형식으로 이름이 지정됩니다.

### 기여

모든 형태의 기여를 환영합니다! 개선이나 새로운 기능에 대한 제안이 있다면 issue나 pull request를 제출해 주세요.

### 라이선스

이 프로젝트는 MIT 라이선스를 기반으로 오픈 소스로 제공됩니다 - 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
