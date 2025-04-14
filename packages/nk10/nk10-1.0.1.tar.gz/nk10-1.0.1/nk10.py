"""
nk10 - 10KN: Man-Jinsu (만진수) numeral system using Hangul only

- 한글 기반 10,000진법 숫자 체계
- 범위: '가'(U+AC00)부터 시작하는 Hangul Syllables
- 정렬 가능: 유니코드 순서 = 숫자 크기
- 정보 압축력 우수, 한글 전용
- 설계: blueradiance (2025)
"""

BASE_10KN = 10000
HANGUL_OFFSET = 0xAC00  # '가' = 0

def encode_nk10(n: int) -> str:
    if n == 0:
        return chr(HANGUL_OFFSET)
    result = []
    while n > 0:
        digit = n % BASE_10KN
        ch = chr(HANGUL_OFFSET + digit)
        result.insert(0, ch)
        n //= BASE_10KN
    return ''.join(result)

def decode_nk10(s: str) -> int:
    n = 0
    for ch in s:
        val = ord(ch) - HANGUL_OFFSET
        if not (0 <= val < BASE_10KN):
            raise ValueError(f"Invalid nk10 character: '{ch}'")
        n = n * BASE_10KN + val
    return n
