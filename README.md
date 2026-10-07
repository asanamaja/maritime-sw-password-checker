# 비밀번호 보안성 검사기

해사소프트웨어 4번째 과제. VS Code에서 만든 첫 파이썬 프로젝트입니다.

비밀번호 길이가 8자리 이상인지, 대문자와 소문자가 함께 있는지, 숫자와 특수문자(`!@#$%^&*`)가 있는지를 검사합니다. 충족한 조건 수에 따라 **취약(0~1)**, **보통(2~3)**, **강력(4)** 으로 보여주고, 강력 등급 비밀번호 예시를 하나 추천합니다.

## 실행

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python src/checker.py
```

예시 3건(취약, 보통, 강력)을 한 번에 보려면:

```powershell
python src/checker.py --demo
```

## 테스트

```powershell
python -m unittest discover -s tests
```
