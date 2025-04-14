# nk20

nk20: Hanja-based base-20000 numeral encoder/decoder  
**nk20 – 이만진수 기반 정보 압축**

## Install

```bash
pip install nk20
```

## Usage

```python
from nk20 import encode_nk20, decode_nk20

s = encode_nk20(123456)
n = decode_nk20(s)
print(s, n)
```
