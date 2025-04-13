# nk256_full

Fully Unicode-based Base-256,000 numeral encoding system.

This module encodes extremely large integers using a 256,000-character set from extended Unicode ranges (starting from U+20000). While many characters may not render correctly (appearing as □), the system ensures perfect reversibility, order preservation, and ultra-efficient number compression. Ideal for tagging, indexing, and high-density numeric encoding in internal systems.

## Example

```python
import nk256_full as nk256

n = 98765432101234567890
encoded = nk256.encode_nk256(n)
decoded = nk256.decode_nk256(encoded)

print("🔐 Encoded:", encoded)
print("🔓 Decoded:", decoded)
print("✅ Success:", decoded == n)
```
