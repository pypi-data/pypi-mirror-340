# nk10

✨ One-function nk10 encoder/decoder using Hangul syllables (base-10000)  
**nk10 – Number Kilo 10 Numeric system (만진수)**

---

## Install

```bash
pip install nk10
```

## Usage

```python
import nk10

nk10(123456)     # → '각갛' 등 한글 조합 문자열
nk10('각갛')     # → 123456
```

## Concept

- Pass `int` → returns nk10 Hangul string.
- Pass `str` → returns original integer.
- Based on Unicode range U+AC00 ~ U+AC00+9999 ('가' ~ ).
- Lexicographically sortable & compact.

## License

MIT
