# nk20

Unicode Hanja-based base-20,000 numeral compression system.

```bash
pip install nk20
```

```python
import nk20

s = nk20.encode_nk20(123456789)
n = nk20.decode_nk20(s)
```
