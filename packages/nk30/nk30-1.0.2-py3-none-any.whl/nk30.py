"""
✨ One-function nk30 encoder/decoder using Hangul + Hanja (base-30000)

nk30 - Hybrid Number Kilo 30 Numeric system (삼만진수)

- 한글 + 한자 기반 30,000진법 숫자 체계
- 범위: 한글(가~) + 한자(一~)
- 정렬 가능: 유니코드 순서 = 숫자 크기
- 정보 압축 및 표현력 극대화
- 설계: blueradiance (2025)
"""

BASE_30KN = 30000
HANGUL_OFFSET = 0xAC00  # '가'
HANJA_OFFSET = 0x4E00   # '一'
HANGUL_MAX = 9999
HANJA_MAX = 29999

def encode_nk30(n: int) -> str:
    if n == 0:
        return chr(HANGUL_OFFSET)
    result = []
    while n > 0:
        digit = n % BASE_30KN
        if digit <= HANGUL_MAX:
            ch = chr(HANGUL_OFFSET + digit)
        else:
            ch = chr(HANJA_OFFSET + (digit - (HANGUL_MAX + 1)))
        result.insert(0, ch)
        n //= BASE_30KN
    return ''.join(result)

def decode_nk30(s: str) -> int:
    n = 0
    for ch in s:
        code = ord(ch)
        if HANGUL_OFFSET <= code <= HANGUL_OFFSET + HANGUL_MAX:
            val = code - HANGUL_OFFSET
        elif HANJA_OFFSET <= code <= HANJA_OFFSET + (HANJA_MAX - HANGUL_MAX - 1):
            val = HANGUL_MAX + 1 + (code - HANJA_OFFSET)
        else:
            raise ValueError(f"Invalid character in nk30 string: '{ch}'")
        n = n * BASE_30KN + val
    return n

# alias
nk30 = encode_nk30
