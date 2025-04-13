# nku

Unified controller for NK Unicode numeral systems (nk10, nk20, nk30, nk100, nk200, nk256).  
Handles compact number encoding and decoding across multiple radices.  
Internally normalizes base=X to X×1000 if X < 1000.

## Example

```python
from nku import encode, decode

n = 12345678901234567890

# All valid and interchangeable
print(encode(n, base=10))       # = nk10
print(encode(n, base=100))      # = nk100
print(encode(n, base=256))      # = nk256
```
