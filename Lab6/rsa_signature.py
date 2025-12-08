from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import MD4
import os
import sys


class RSADigitalSignature:
    def __init__(self, key_size=3072):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        print(f"\n{'='*70}")
        print("STEP 1: Generating RSA Key Pair")
        print(f"{'='*70}")
        print(f"Key size: {self.key_size} bits")
        print("This may take a moment for large key sizes...")

        self.private_key = RSA.generate(self.key_size)

        self.public_key = self.private_key.publickey()

        print("\nKeys generated successfully!")
        print("\nKey Parameters:")
        print(f"  • Modulus (n) size: {self.private_key.n.bit_length()} bits")
        print(f"  • Public exponent (e): {self.private_key.e}")
        print(
            f"  • Modulus (n) first 50 digits: {str(self.private_key.n)[:50]}...")

        return self.private_key, self.public_key

    def save_keys_to_files(self, private_file="private_key.pem", public_file="public_key.pem"):
        if not self.private_key or not self.public_key:
            raise ValueError("Keys must be generated before saving")

        print(f"\n{'='*70}")
        print("STEP 2: Saving Keys to Files")
        print(f"{'='*70}")

        with open(private_file, 'wb') as f:
            f.write(self.private_key.export_key('PEM'))
        print(f"✓ Private key saved to: {private_file}")

        with open(public_file, 'wb') as f:
            f.write(self.public_key.export_key('PEM'))
        print(f"✓ Public key saved to: {public_file}")

    def sign_message(self, message):
        if not self.private_key:
            raise ValueError("Private key is required for signing")

        if isinstance(message, str):
            message = message.encode('utf-8')

        hash_obj = MD4.new(message)
        hash_hex = hash_obj.hexdigest()
        hash_decimal = int(hash_hex, 16)  # Convert hex to decimal

        print(f"\n  • Message size: {len(message)} bytes")
        print(f"  • MD4 hash (hex): {hash_hex}")
        print(f"  • MD4 hash (decimal): {hash_decimal}")

        signature = pkcs1_15.new(self.private_key).sign(hash_obj)

        print(
            f"  • Signature size: {len(signature)} bytes ({len(signature) * 8} bits)")
        print(
            f"  • Signature (hex, first 64 chars): {signature.hex()[:64]}...")

        return signature

    def verify_signature(self, message, signature):
        if not self.public_key:
            raise ValueError("Public key is required for verification")

        if isinstance(message, str):
            message = message.encode('utf-8')

        hash_obj = MD4.new(message)
        hash_hex = hash_obj.hexdigest()
        hash_decimal = int(hash_hex, 16)

        print(f"\n  • Message size: {len(message)} bytes")
        print(f"  • MD4 hash (hex): {hash_hex}")
        print(f"  • MD4 hash (decimal): {hash_decimal}")
        print("  • Verifying signature using public key...")

        try:
            pkcs1_15.new(self.public_key).verify(hash_obj, signature)
            print("\n  SIGNATURE IS VALID!")
            print("    The document was signed with the corresponding private key")
            print("    and has not been modified since signing.")
            return True
        except (ValueError, TypeError) as e:
            print("\n  SIGNATURE IS INVALID!")
            print(f"    Error: {e}")
            return False

    def sign_file(self, input_file, signature_file):
        print(f"\n{'='*70}")
        print("STEP 3: Signing the Document")
        print(f"{'='*70}")
        print(f"Document: {input_file}")

        try:
            with open(input_file, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found!")
            sys.exit(1)

        signature = self.sign_message(content)

        with open(signature_file, 'wb') as f:
            f.write(signature)
        print(f"\n✓ Signature saved to: {signature_file}")

        return signature

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
            with open(signature_file, 'rb') as f:
                signature = f.read()
        except FileNotFoundError:
            print(f"✗ Error: Signature file '{signature_file}' not found!")
            return False

        return self.verify_signature(content, signature)


def main():
    print("\n" + "="*70)
    print("RSA DIGITAL SIGNATURE - LABORATORY WORK 6")
    print("Cryptography and Security")
    print("="*70)
    print("\nRequirements:")
    print("  • RSA key size (n): 3072 bits")
    print("  • Hash algorithm: MD4")
    print("  • Document: message_multiline.txt")
    print("="*70)

    KEY_SIZE = 3072
    MESSAGE_FILE = "message_multiline.txt"
    SIGNATURE_FILE = "message_multiline.sig"
    PRIVATE_KEY_FILE = "private_key.pem"
    PUBLIC_KEY_FILE = "public_key.pem"

    if not os.path.exists(MESSAGE_FILE):
        print(f"\n✗ Error: Message file '{MESSAGE_FILE}' not found!")
        print("Please ensure the file exists in the current directory.")
        sys.exit(1)

    rsa = RSADigitalSignature(key_size=KEY_SIZE)

    rsa.generate_keys()

    rsa.save_keys_to_files(PRIVATE_KEY_FILE, PUBLIC_KEY_FILE)

    signature = rsa.sign_file(MESSAGE_FILE, SIGNATURE_FILE)

    is_valid = rsa.verify_file_signature(MESSAGE_FILE, SIGNATURE_FILE)

    print(f"\n{'='*70}")
    print("STEP 5: Testing Signature Security")
    print(f"{'='*70}")
    print("Testing what happens if the document is modified...")

    with open(MESSAGE_FILE, 'rb') as f:
        original_content = f.read()

    modified_file = "message_modified.txt"
    with open(modified_file, 'wb') as f:
        f.write(b"TAMPERED: " + original_content)

    print("\nVerifying signature on modified document...")
    rsa_verify = RSADigitalSignature()
    rsa_verify.public_key = rsa.public_key

    try:
        with open(modified_file, 'rb') as f:
            modified_content = f.read()
        with open(SIGNATURE_FILE, 'rb') as f:
            signature = f.read()

        is_valid_modified = rsa_verify.verify_signature(
            modified_content, signature)
    except:
        is_valid_modified = False

    if os.path.exists(modified_file):
        os.remove(modified_file)

    print(f"\n{'='*70}")
    print("SUMMARY - LABORATORY WORK RESULTS")
    print(f"{'='*70}")
    print("Configuration:")
    print(f"  • Key size (n): {KEY_SIZE} bits")
    print("  • Hash algorithm: MD4")
    print("  • Signature scheme: RSA with PKCS#1 v1.5")
    print("\nFiles:")
    print(f"  • Document: {MESSAGE_FILE}")
    print(f"  • Private key: {PRIVATE_KEY_FILE} (keep secret!)")
    print(f"  • Public key: {PUBLIC_KEY_FILE} (can be shared)")
    print(f"  • Signature: {SIGNATURE_FILE}")
    print("\nResults:")
    print(
        f"  • Original document signature: {'VALID ✓' if is_valid else 'INVALID ✗'}")
    print(
        f"  • Modified document signature: {'VALID ✓' if is_valid_modified else 'INVALID ✗ (as expected)'}")


if __name__ == "__main__":
    main()
