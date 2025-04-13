# nk256

Unicode-based Base-256,000 numeral encoding system.

This package encodes massive integers using a custom 256,000-character set starting from U+20000 in the Unicode range. The encoding is compact, reversible, and supports full numeric sorting. Some characters may not render properly on all systems, but the data is fully intact and designed for machine use.

## Example

```python
import nk256

n = 98765432101234567890
encoded = nk256.encode_nk256(n)
decoded = nk256.decode_nk256(encoded)

print("🔐 Encoded:", encoded)
print("🔓 Decoded:", decoded)
print("✅ Success:", decoded == n)
```
