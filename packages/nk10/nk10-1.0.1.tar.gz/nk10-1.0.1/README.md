# nk10

nk10: Hangul-only base-10000 numeral encoder/decoder  
**nk10 – 만진수 기반 정보 압축**

## Install

```bash
pip install nk10
```

## Usage

```python
from nk10 import encode_nk10, decode_nk10

s = encode_nk10(987654)
n = decode_nk10(s)
print(s, n)
```
