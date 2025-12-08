import secrets
import sys
import os
from math import gcd
from Crypto.Hash import MD4


class ElGamalSignature:
    def __init__(self, p, g):
        self.p = p
        self.g = g
        self.p_bits = p.bit_length()
        self.private_key = None  # x
        self.public_key = None   # y

    def ntlm_hash(self, message):

        hash_obj = MD4.new(message)
        hash_hex = hash_obj.hexdigest()
        hash_int = int(hash_hex, 16)

        return hash_int, hash_hex

    def mod_inverse(self, a, m):
        try:
            return pow(a, -1, m)
        except ValueError:
            raise ValueError("Modular inverse does not exist")

    def generate_keys(self):
        print(f"\n{'='*70}")
        print("STEP 1: Generating ElGamal Key Pair")
        print(f"{'='*70}")
        print(f"Prime modulus (p) size: {self.p_bits} bits")
        print(f"Generator (g): {self.g}")
        print("Generating private key...")

        # private key x in range [2, p-2]
        self.private_key = secrets.randbelow(self.p - 3) + 2

        print("Computing public key y = g^x mod p (this may take a moment)...")
        # public key y = g^x mod p
        self.public_key = pow(self.g, self.private_key, self.p)

        print("\n✓ Keys generated successfully!")
        print("\nKey Parameters:")
        print(
            f"  • Private key (x) size: {self.private_key.bit_length()} bits")
        print(
            f"  • Private key (x) first 50 digits: {str(self.private_key)[:50]}...")
        print(f"  • Public key (y) size: {self.public_key.bit_length()} bits")
        print(
            f"  • Public key (y) first 50 digits: {str(self.public_key)[:50]}...")

        return self.private_key, self.public_key

    def save_keys_to_files(self, private_file="elgamal_private.txt", public_file="elgamal_public.txt"):
        if self.private_key is None or self.public_key is None:
            raise ValueError("Keys must be generated before saving")

        print(f"\n{'='*70}")
        print("STEP 2: Saving Keys to Files")
        print(f"{'='*70}")

        with open(private_file, 'w') as f:
            f.write("ElGamal Private Key (x)\n")
            f.write("=" * 70 + "\n")
            f.write(f"Decimal: {self.private_key}\n")
            f.write(f"Hex: {hex(self.private_key)}\n")
        print(f"✓ Private key saved to: {private_file}")

        with open(public_file, 'w') as f:
            f.write("ElGamal Public Key (y)\n")
            f.write("=" * 70 + "\n")
            f.write(f"Decimal: {self.public_key}\n")
            f.write(f"Hex: {hex(self.public_key)}\n")
            f.write("\nDomain Parameters:\n")
            f.write(f"p = {self.p}\n")
            f.write(f"g = {self.g}\n")
        print(f"✓ Public key saved to: {public_file}")

    def sign_message(self, message):
        if self.private_key is None:
            raise ValueError("Private key is required for signing")

        if isinstance(message, str):
            message = message.encode('utf-8')

        hash_int, hash_hex = self.ntlm_hash(message)

        print(f"\n  • Message size: {len(message)} bytes")
        print(f"  • NTLM hash (hex): {hash_hex}")
        print(f"  • NTLM hash (decimal): {hash_int}")

        print("  • Generating random k with gcd(k, p-1) = 1...")
        p_minus_1 = self.p - 1

        for attempt in range(1000):
            k = secrets.randbelow(p_minus_1 - 2) + 2
            if gcd(k, p_minus_1) == 1:
                break
        else:
            raise ValueError("Failed to generate valid k")

        print(f"  • Random k size: {k.bit_length()} bits")

        # r = g^k mod p
        print("  • Computing r = g^k mod p...")
        r = pow(self.g, k, self.p)

        # s = (h - x*r) * k^(-1) mod (p-1)
        print("  • Computing k^(-1) mod (p-1)...")
        k_inv = self.mod_inverse(k, p_minus_1)

        print("  • Computing s = (h - x*r) * k^(-1) mod (p-1)...")
        s = ((hash_int - self.private_key * r) * k_inv) % p_minus_1

        print("\n  ✓ Signature computed successfully!")
        print(f"  • r size: {r.bit_length()} bits")
        print(f"  • r (first 50 digits): {str(r)[:50]}...")
        print(f"  • s size: {s.bit_length()} bits")
        print(f"  • s (first 50 digits): {str(s)[:50]}...")

        return r, s

    def verify_signature(self, message, signature):
        if self.public_key is None:
            raise ValueError("Public key is required for verification")

        r, s = signature

        if isinstance(message, str):
            message = message.encode('utf-8')

        hash_int, hash_hex = self.ntlm_hash(message)

        print(f"\n  • Message size: {len(message)} bytes")
        print(f"  • NTLM hash (hex): {hash_hex}")
        print(f"  • NTLM hash (decimal): {hash_int}")

        print("  • Checking signature bounds...")
        if not (0 < r < self.p):
            print("  ✗ Invalid: r is out of bounds")
            return False
        if not (0 < s < self.p - 1):
            print("  ✗ Invalid: s is out of bounds")
            return False

        # Verify the signature equation
        # g^h ≡ y^r * r^s (mod p)
        print("  • Verifying: g^h ≡ y^r * r^s (mod p)")
        print("    Computing left side: g^h mod p...")
        left_side = pow(self.g, hash_int, self.p)

        print("    Computing right side: (y^r * r^s) mod p...")
        right_side = (pow(self.public_key, r, self.p)
                      * pow(r, s, self.p)) % self.p

        if left_side == right_side:
            print("\n  ✓ SIGNATURE IS VALID!")
            print("    The equation holds: g^h ≡ y^r * r^s (mod p)")
            print("    Signature was created with the corresponding private key.")
            return True
        else:
            print("\n  ✗ SIGNATURE IS INVALID!")
            print("    The verification equation does not hold.")
            return False

    def sign_file(self, input_file, signature_file):
        print(f"\n{'='*70}")
        print(f"STEP 3: Signing the Document")
        print(f"{'='*70}")
        print(f"Document: {input_file}")

        try:
            with open(input_file, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"✗ Error: File '{input_file}' not found!")
            sys.exit(1)

        r, s = self.sign_message(content)

        with open(signature_file, 'w') as f:
            f.write("ElGamal Signature\n")
            f.write("=" * 70 + "\n")
            f.write(f"r (decimal):\n{r}\n\n")
            f.write(f"r (hex):\n{hex(r)}\n\n")
            f.write(f"s (decimal):\n{s}\n\n")
            f.write(f"s (hex):\n{hex(s)}\n")

        print(f"\n✓ Signature saved to: {signature_file}")
        return r, s

    def verify_file_signature(self, input_file, signature_file):
        print(f"\n{'='*70}")
        print("STEP 4: Verifying the Signature")
        print(f"{'='*70}")
        print(f"Document: {input_file}")
        print(f"Signature file: {signature_file}")

        try:
            with open(input_file, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"✗ Error: File '{input_file}' not found!")
            return False

        try:
            with open(signature_file, 'r') as f:
                lines = f.readlines()
                r = None
                s = None
                i = 0
                while i < len(lines):
                    if lines[i].startswith("r (decimal):"):
                        r = int(lines[i+1].strip())
                    elif lines[i].startswith("s (decimal):"):
                        s = int(lines[i+1].strip())
                    i += 1
        except FileNotFoundError:
            print(f"✗ Error: Signature file '{signature_file}' not found!")
            return False

        if r is None or s is None:
            print("✗ Error: Could not parse signature file")
            return False

        return self.verify_signature(content, (r, s))


def main():
    print("\n" + "="*70)
    print("ELGAMAL DIGITAL SIGNATURE - LABORATORY WORK 6 - PART 2")
    print("Cryptography and Security")
    print("="*70)
    print("\nRequirements:")
    print("  • Signature scheme: ElGamal")
    print("  • Prime modulus (p): 2048 bits (provided)")
    print("  • Generator (g): 2")
    print("  • Hash algorithm: NTLM (MD4-based)")
    print("  • Document: message_multiline.txt")
    print("="*70)

    P = int("323170060713110073001535134778251633624880571334890751745884"
            "34139269806834136210002792056362640164685458556357935330816928"
            "82902308057347262527355474246124574102620252791657297286270630"
            "03252634282131457669314142236542209411113486299916574782680342"
            "30553086349050635557712219187890332729569696129743856241741236"
            "23722519734640269185579776797682301462539793305801522685873076"
            "11975324364674758554607150438968449403661304976978128542959586"
            "59597567051283852132784468522925504568272879113720098931873959"
            "14337417583782600027803497319855206060753323412260325468408812"
            "0031105907484281003994966956119696956248629032338072839127039")
    G = 2

    MESSAGE_FILE = "message_multiline.txt"
    SIGNATURE_FILE = "message_multiline_elgamal.sig"
    PRIVATE_KEY_FILE = "elgamal_private.txt"
    PUBLIC_KEY_FILE = "elgamal_public.txt"

    # Verify message file exists
    if not os.path.exists(MESSAGE_FILE):
        print(f"\n✗ Error: Message file '{MESSAGE_FILE}' not found!")
        sys.exit(1)

    elgamal = ElGamalSignature(p=P, g=G)

    elgamal.generate_keys()

    elgamal.save_keys_to_files(PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)

    r, s = elgamal.sign_file(MESSAGE_FILE, SIGNATURE_FILE)

    is_valid = elgamal.verify_file_signature(MESSAGE_FILE, SIGNATURE_FILE)

    print(f"\n{'='*70}")
    print("SUMMARY - LABORATORY WORK PART 2 RESULTS")
    print(f"{'='*70}")
    print("Configuration:")
    print("  • Signature scheme: ElGamal")
    print(f"  • Prime modulus (p): {P.bit_length()} bits")
    print(f"  • Generator (g): {G}")
    print("  • Hash algorithm: NTLM (MD4-based)")
    print("\nFiles Generated:")
    print(f"  • Document: {MESSAGE_FILE}")
    print(f"  • Private key: {PRIVATE_KEY_FILE} (keep secret!)")
    print(f"  • Public key: {PUBLIC_KEY_FILE} (can be shared)")
    print(f"  • Signature: {SIGNATURE_FILE}")
    print("\nVerification Result:")
    print(f"  • Signature status: {'VALID ✓' if is_valid else 'INVALID ✗'}")


if __name__ == "__main__":
    main()
