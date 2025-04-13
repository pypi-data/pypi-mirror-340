# nk100

Layered Unicode Base-100000 numeral system.

- Top 30,000 characters: Hangul + Hanja (human-readable)
- Bottom 70,000 characters: CJK Extensions (machine-readable only)

```python
import nk100

encoded = nk100.encode_nk100(98765432109876543210)
decoded = nk100.decode_nk100(encoded)

print(encoded)  # may include some squares (□)
print(decoded)  # 98765432109876543210
```
