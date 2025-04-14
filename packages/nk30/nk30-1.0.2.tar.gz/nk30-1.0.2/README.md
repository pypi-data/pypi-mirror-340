# nk30

✨ nk30: Hybrid base-30000 encoder/decoder using Hangul + Hanja  
**nk30 – 삼만진수 기반 정보 압축**

## Install

```bash
pip install nk30
```

## Usage

```python
from nk30 import encode_nk30, decode_nk30

s = encode_nk30(123456)
n = decode_nk30(s)
```

## Aliases

```python
import nk30
nk30.nk30(123456)     # == encode_nk30(123456)
```

## License

MIT
