# nku

Unified controller for NK Unicode numeral systems (nk10, nk20, nk30, nk100, nk200, nk256).  
Handles compact number encoding and decoding across multiple radices.

## Features

- One interface to handle multiple Unicode numeral systems
- Accepts base=10 or base=10000 equivalently (internally normalized ×1000)
- Modules supported: nk10, nk20, nk30, nk100, nk200, nk256
- Simplifies encoding logic across your projects

## Example

```python
from nku import encode, decode

n = 12345678901234567890

e1 = encode(n, base=10)       # nk10
e2 = encode(n, base=20)       # nk20
e3 = encode(n, base=100)      # nk100
e4 = encode(n, base=256)      # nk256

print(decode(e1, base=10))
print(decode(e2, base=20))
print(decode(e3, base=100))
print(decode(e4, base=256))
```

## License

Custom License for nku (Unified Controller by blueradiance, 2025)  
- Free to use with attribution  
- Commercial use allowed  
- Do not rebrand or modify without notice  
