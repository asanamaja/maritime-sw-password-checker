"""비밀번호 보안성 검사기.

조건 4가지(길이, 대소문자 혼합, 숫자, 특수문자)를 세어
취약(0~1), 보통(2~3), 강력(4)으로 판정한다.
"""

from __future__ import annotations

import argparse
import secrets
import string
import sys

SPECIALS = "!@#$%^&*"


def evaluate(password: str) -> dict[str, object]:
    has_upper = any(ch.isupper() for ch in password)
    has_lower = any(ch.islower() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    has_special = any(ch in SPECIALS for ch in password)
    length_ok = len(password) >= 8
    mixed_case = has_upper and has_lower
    score = sum((length_ok, mixed_case, has_digit, has_special))

    if score >= 4:
        grade = "강력"
    elif score >= 2:
        grade = "보통"
    else:
        grade = "취약"

    return {
        "length": len(password),
        "length_ok": length_ok,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "mixed_case": mixed_case,
        "score": score,
        "grade": grade,
    }


def advice(result: dict[str, object]) -> str:
    if result["grade"] == "강력":
        return "안전한 비밀번호입니다."

    missing: list[str] = []
    if not result["length_ok"]:
        missing.append("8자리 이상")
    if not result["mixed_case"]:
        missing.append("대문자와 소문자 혼합")
    if not result["has_digit"]:
        missing.append("숫자")
    if not result["has_special"]:
        missing.append("특수문자(!@#$%^&*)")
    return "보안 강화를 위해 " + ", ".join(missing) + " 조건을 추가하세요."


def suggest_password(length: int = 12) -> str:
    if length < 8:
        raise ValueError("추천 비밀번호는 8자리 이상이어야 합니다.")

    required = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(SPECIALS),
    ]
    pool = string.ascii_letters + string.digits + SPECIALS
    chars = required + [secrets.choice(pool) for _ in range(length - len(required))]
    secrets.SystemRandom().shuffle(chars)
    password = "".join(chars)
    if evaluate(password)["grade"] != "강력":
        raise RuntimeError("추천 비밀번호가 강력 등급이 아닙니다.")
    return password


def _mark(ok: bool) -> str:
    return "✅" if ok else "❌"


def render(password: str) -> str:
    result = evaluate(password)
    lines = [
        "========================================",
        "비밀번호 보안성 검사기",
        "========================================",
        f"검사할 비밀번호를 입력하세요: {password}",
        "",
        "[검사 결과]",
        f"{_mark(bool(result['length_ok']))} 8자리 이상 (현재 {result['length']}자리)",
        f"{_mark(bool(result['has_upper']))} 대문자 포함",
        f"{_mark(bool(result['has_lower']))} 소문자 포함",
        f"{_mark(bool(result['has_digit']))} 숫자 포함",
        f"{_mark(bool(result['has_special']))} 특수문자 포함",
        "",
        f"결과: [{result['grade']}] - {advice(result)}",
        "",
        "[추천 비밀번호]",
        f"강력 등급 예시: {suggest_password()}",
        "========================================",
    ]
    return "\n".join(lines)


def check_once(password: str) -> None:
    print(render(password))


def run_demo() -> None:
    samples = ["abc", "Pass12!", "Abcd1234!"]
    for index, password in enumerate(samples):
        if index:
            print()
        check_once(password)


def _prepare_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            continue
        try:
            reconfigure(encoding="utf-8", errors="replace")
        except (OSError, ValueError):
            pass


def main(argv: list[str] | None = None) -> None:
    _prepare_output()
    parser = argparse.ArgumentParser(description="비밀번호 보안성 검사기")
    parser.add_argument("password", nargs="?", help="검사할 비밀번호")
    parser.add_argument("--demo", action="store_true", help="취약/보통/강력 예시 3건을 출력")
    args = parser.parse_args(argv)

    if args.demo:
        run_demo()
        return
    if args.password is not None:
        check_once(args.password)
        return

    print("========================================")
    print("비밀번호 보안성 검사기")
    print("========================================")
    password = input("검사할 비밀번호를 입력하세요: ")
    result = evaluate(password)
    print()
    print("[검사 결과]")
    print(f"{_mark(bool(result['length_ok']))} 8자리 이상 (현재 {result['length']}자리)")
    print(f"{_mark(bool(result['has_upper']))} 대문자 포함")
    print(f"{_mark(bool(result['has_lower']))} 소문자 포함")
    print(f"{_mark(bool(result['has_digit']))} 숫자 포함")
    print(f"{_mark(bool(result['has_special']))} 특수문자 포함")
    print()
    print(f"결과: [{result['grade']}] - {advice(result)}")
    print()
    print("[추천 비밀번호]")
    print(f"강력 등급 예시: {suggest_password()}")
    print("========================================")


if __name__ == "__main__":
    main(sys.argv[1:])
