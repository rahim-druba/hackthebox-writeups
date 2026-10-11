ct = bytes.fromhex(open('extracted/msg.enc').read().strip())
inv = pow(123, -1, 256)
print("inverse of 123 mod 256 =", inv)
print("ciphertext bytes       =", len(ct))
pt = bytes(((b - 18) * inv) % 256 for b in ct)
print("plaintext              =", pt.decode())
# sanity check: re-encrypt with the original algorithm
assert bytes((123 * c + 18) % 256 for c in pt) == ct
print("re-encryption matches msg.enc: OK")
