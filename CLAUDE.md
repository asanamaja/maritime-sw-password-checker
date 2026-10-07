# 비밀번호 보안성 검사기

파이썬 표준 라이브러리만 사용하는 CLI 프로그램이다.

## Commands

- Run app: `python src/checker.py`
- Run demo: `python src/checker.py --demo`
- Run tests: `python -m unittest discover -s tests`

## Code Style

- Use type hints for function signatures.
- Follow PEP 8 guidelines.
- Do NOT hardcode API keys or credentials; use a `.env` file if one is ever needed.

## Architecture

- `src/checker.py`: 비밀번호 검사와 강력 등급 추천 비밀번호 생성
- `tests/`: 등급 판정 단위 테스트

## Security

- 입력한 비밀번호를 파일로 저장하지 않는다.
- API 키, 토큰, 비밀번호를 소스코드에 하드코딩하지 않는다.
