import hashlib

enc_table_16 = "0123456789abcdef"
enc_table_64 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_"


def int_to_enc(n, enc_table):
    """Encode integer into string, using digit encoding table."""
    if n == 0:
        return enc_table[0]

    base = len(enc_table)
    digits = ""
    while n:
        digits += enc_table[int(n % base)]
        n //= base
    return digits[::-1]


def short_str_enc(s, char_length=8, enc_table=enc_table_64):
    """Generate string hash with given length, using specified encoding table."""

    if char_length > 128:
        raise ValueError("char_length {} exceeds 128".format(char_length))
    hash_object = hashlib.sha512(s.encode())
    hash_hex = hash_object.hexdigest()
    hash_enc = int_to_enc(int(hash_hex, 16), enc_table)
    return hash_enc[0:char_length]
