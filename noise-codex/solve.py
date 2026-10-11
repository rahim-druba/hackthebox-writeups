import ast
from flint import fmpz_mat

c = ast.literal_eval(open('extracted/output.txt').read())
print("ciphertexts:", len(c))

# c_i = p*q_i + (2*r_i + b_i), noise < 2^513 while p has 1024 bits.
# Approximate GCD: LLL on a few ciphertexts gives q_0.
RHO = 513
t = 12
rows = [[2**RHO] + c[1:t + 1]]
for i in range(1, t + 1):
    row = [0] * (t + 1)
    row[i] = -c[0]
    rows.append(row)

reduced = fmpz_mat(rows).lll()

p = None
for r in range(reduced.nrows()):
    q0 = abs(int(reduced[r, 0])) // 2**RHO
    if q0 == 0:
        continue
    cand = c[0] // q0
    if cand.bit_length() == 1024 and all(x % cand < 2**(RHO + 1) for x in c):
        p = cand
        break

assert p is not None, "p not found"
print("p found, bits:", p.bit_length())

# c mod p = 2*r + b, so the last bit of the remainder is the message bit.
bits = "".join(str((x % p) & 1) for x in c)
msg = bytes(int(bits[i:i + 8], 2) for i in range(0, len(bits), 8))
print("flag:", msg.decode())
