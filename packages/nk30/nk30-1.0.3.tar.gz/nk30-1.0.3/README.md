# nk30

nk30: Hangul + Hanja base-30000 numeral encoder/decoder  
**Compatible with kn30 but renamed for namespace clarity.**

## Install

```bash
pip install nk30
```

## Usage

```python
from nk30 import encode_nk30, decode_nk30

s = encode_nk30(123456)
n = decode_nk30(s)
print(s, n)
```
