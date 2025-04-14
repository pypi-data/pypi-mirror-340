# nk30

✨ One-function nk30 encoder/decoder using Hangul + Hanja (base-30000)  
**nk30 – Hybrid Number Kilo 30 Numeric system (삼만진수)**

## Install

```bash
pip install nk30
```

## Usage

```python
import nk30

nk30(123456)     # → '각漢' 형태의 문자
nk30('각漢')     # → 123456
```

## Concept

- Pass `int` → returns Hangul + Hanja encoded string
- Pass `str` → returns original integer
- Unicode based, lexicographically sortable
- Extremely compact numeric representation
- Ideal for short identifiers, symbolic compression, encoding systems

## License

MIT
