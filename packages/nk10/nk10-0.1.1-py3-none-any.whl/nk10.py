"""
✨ One-function nk10 encoder/decoder using Hangul syllables (base-10000)

nk10 - Number Kilo 10 Numeric system (만진수)

- 한글 음절 기반 10,000진법 숫자 체계
- 범위: U+AC00 ~ U+AC00+9999 ('가' ~ )
- 정렬 가능: 유니코드 순서 = 숫자 크기
- 설계: blueradiance (2025)
"""

BASE = 10000
OFFSET = 0xAC00  # Unicode starting point for Hangul syllables

def _encode(n: int) -> str:
    if n == 0:
        return chr(OFFSET)
    result = []
    while n > 0:
        result.insert(0, chr(OFFSET + (n % BASE)))
        n //= BASE
    return ''.join(result)

def _decode(s: str) -> int:
    total = 0
    for ch in s:
        val = ord(ch) - OFFSET
        if not (0 <= val < BASE):
            raise ValueError(f"Invalid nk10 character: '{ch}'")
        total = total * BASE + val
    return total

def nk10(x):
    """Pass int → encode / str → decode"""
    if isinstance(x, int):
        return _encode(x)
    elif isinstance(x, str):
        return _decode(x)
    else:
        raise TypeError("nk10() only accepts int or str")
