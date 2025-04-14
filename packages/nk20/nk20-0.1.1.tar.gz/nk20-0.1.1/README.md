# nk20

✨ One-function nk20 encoder/decoder using CJK Unified Ideographs (base-20000)  
**nk20 – Number Kilo 20 Numeric system (이만진수)**

---

## Install

```bash
pip install nk20
```

## Usage

```python
import nk20

nk20(123456)     # → '漢字' 등 한자 조합 문자열
nk20('漢字')     # → 123456
```

## Concept

- Pass `int` → returns nk20 CJK string.
- Pass `str` → returns original integer.
- Based on Unicode range U+4E00 ~ U+9FFF (20,992 chars).
- Lexicographically sortable & extremely compact.

## License

MIT
