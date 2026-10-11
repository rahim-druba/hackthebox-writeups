from Crypto.Util.number import getPrime as getAnchor
import random
from secrets import flag


class AffineNoiseCipher:
    """
    ┌───────────────────────────────────────────────────────────────────┐
    │     A N C   :   A F F I N E   N O I S E   C I P H E R             │
    │───────────────────────────────────────────────────────────────────│
    │ "If truth must be hidden, drown it in the thunder of primes."     │
    │                                                                   │
    │ The cipher binds each bit to noise:                               │
    │      c = p*q  +  2*r  +  b                                        │
    │                                                                   │
    │ Where:                                                            │
    │   p — Anchor, whispered to be soul-bound to each user             │
    │   q — structural distortion                                       │
    │   r — deep noise harvested from entropy rituals                   │
    │   b — the message bit, the ghost in the machine                   │
    └───────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, anchor):
        self.anchor = anchor

    def inscribe_noise(self, message: str):
        """
        A ritual engraving: truth carved into chaos.
        Echo Mirage claimed bits do not travel—they haunt.
        """

        bits = "".join(f"{ord(c):08b}" for c in message)
        ciphertext = []
        for bit in bits:
            b = int(bit)

            distortion = random.randint(self.anchor, self.anchor**2)
            entropy = random.randint(2**256, 2**512)

            c = self.anchor * distortion + 2 * entropy + b
            ciphertext.append(c)

        return ciphertext


print(">> Initiating Noise Inscription Ritual...")
print(">> Echo Mirage watches from the static.")


anchor = getAnchor(1024)
noise = AffineNoiseCipher(anchor)

with open("output.txt", "w") as file:
    file.write(str(noise.inscribe_noise(flag)))
