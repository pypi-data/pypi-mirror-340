# nk10

High-compression Unicode Hangul numeral system (base-10,000).

```bash
pip install nk10
```

```python
import nk10

s = nk10.encode_nk10(123456789)
n = nk10.decode_nk10(s)
```
