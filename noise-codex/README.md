# Noise Codex

Crypto, Easy. https://app.hackthebox.com/challenges/NoiseCodex

## Files

- `extracted/source.py` — the challenge source
- `extracted/output.txt` — 328 ciphertext numbers (one per bit of the flag)
- `solve.py` — the solver (needs `python-flint` for LLL: `pip install python-flint`)

## Approach

Each bit `b` of the flag is encrypted as `c = p*q + 2*r + b`, where `p` is one
1024-bit prime reused for every bit, `q` is random between `p` and `p^2`, and
`r` is random between `2^256` and `2^512`. The noise `2*r + b` is always
smaller than `2^513`, far smaller than `p`, so `c mod p` recovers the noise,
and its last bit is the message bit.

This is the approximate GCD problem: every ciphertext is close to a multiple
of the same unknown `p`. It is solved with lattice reduction (LLL). A lattice
is built from 13 ciphertexts, and LLL finds a short vector that reveals the
multiplier for the first ciphertext, from which `p` follows directly.

Once `p` is known, `(c mod p) & 1` gives each bit, and grouping them by 8
recovers the flag.

## Run

```
pip install python-flint
python3 solve.py
```
