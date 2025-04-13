# nk200

Unicode-based Base-200,000 numeral encoding system.

Each character encodes up to 200,000 values using extended Unicode blocks.  
Designed for ultra-high-compression of large numbers in machine-readable form.

## Example

```python
import nk200

value = 12345678901234567890
encoded = nk200.encode_nk200(value)
decoded = nk200.decode_nk200(encoded)

print("🔐 Encoded:", encoded)
print("🔓 Decoded:", decoded)
print("✅ Success:", value == decoded)
```
