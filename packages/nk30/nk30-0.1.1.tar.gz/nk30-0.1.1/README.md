# nk30

✨ One-function Hangul/Hanja encoder/decoder in base-30000.

## Install

```bash
pip install nk30
```

## Usage

```python
import nk30

nk30(123456)     # → 문자
nk30('문자')     # → 123456
```

## Concept

- Pass `int` → returns 30KN Hangul/Hanja string.
- Pass `str` → returns original integer.
- That's it. Minimal and elegant.

## License

MIT
