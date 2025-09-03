# AI 다중 에이전트 협력 시뮬레이터 (MVP)

본 저장소는 경제/생태/사회 시뮬레이션을 위한 다중 에이전트(MAS) MVP입니다. Python으로 시뮬레이션을 실행하고, 결과를 `docs/` 정적 사이트에서 시각화합니다. GitHub Pages로 자동 배포됩니다.

## 빠른 시작 (로컬)

1) Python 3.9+ 준비 후, 의존성 설치 (현재 MVP는 표준 라이브러리만 사용):

```bash
pip install -r requirements.txt
```

2) 시뮬레이션 실행 및 결과 생성:

```bash
python main.py
```

성공 시 `docs/data/sim.json` 이 생성됩니다.

3) 정적 사이트 미리보기:

- 간단히 파일 오픈 또는 로컬 서버 구동:

```bash
python -m http.server 8080 --directory docs
```

브라우저에서 `http://localhost:8080` 접속.

## GitHub Pages 배포

- 기본 브랜치(`main` 또는 `master`)에 푸시하면 GitHub Actions가 `docs/` 폴더를 Pages에 배포합니다.
- 리포지토리 Settings → Pages에서 "Build and deployment: GitHub Actions" 선택되어 있는지 확인하세요.

## 구조

```
.
├── agents.py
├── environment.py
├── simulation.py
├── main.py
├── requirements.txt
├── docs/
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── data/
│       └── sim.json (main.py 실행 후 생성)
└── .github/workflows/gh-pages.yml
```

## 다음 단계 제안
- 강화학습 연동(PettingZoo/RLlib/Ray)과 정책 학습 모듈 추가
- 사회/법률(투표/규칙)과 배신/신뢰도 메커니즘 심화
- Web UI에 그래프(협력률, 생존율 등)와 시나리오 프리셋 추가