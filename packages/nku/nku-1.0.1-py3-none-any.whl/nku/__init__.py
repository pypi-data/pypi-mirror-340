
# nku: Unified Unicode Numeric Encoding Controller (Flexible Base)

def normalize_base(base: int) -> int:
    # If base is under 1000, assume it's a simplified base and scale by 1000
    return base if base >= 1000 else base * 1000

def encode(value: int, base: int) -> str:
    base = normalize_base(base)
    if base == 10000:
        from nk10 import encode_nk10 as encode_fn
    elif base == 20000:
        from nk20 import encode_nk20 as encode_fn
    elif base == 30000:
        from nk30 import encode_nk30 as encode_fn
    elif base == 100000:
        from nk100 import encode_nk100 as encode_fn
    elif base == 200000:
        from nk200 import encode_nk200 as encode_fn
    elif base == 256000:
        from nk256 import encode_nk256 as encode_fn
    else:
        raise ValueError(f"Unsupported base: {base}")
    return encode_fn(value)

def decode(text: str, base: int) -> int:
    base = normalize_base(base)
    if base == 10000:
        from nk10 import decode_nk10 as decode_fn
    elif base == 20000:
        from nk20 import decode_nk20 as decode_fn
    elif base == 30000:
        from nk30 import decode_nk30 as decode_fn
    elif base == 100000:
        from nk100 import decode_nk100 as decode_fn
    elif base == 200000:
        from nk200 import decode_nk200 as decode_fn
    elif base == 256000:
        from nk256 import decode_nk256 as decode_fn
    else:
        raise ValueError(f"Unsupported base: {base}")
    return decode_fn(text)
