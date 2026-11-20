import base64
import unittest

from crypto_lab import (
    CryptoInputError, create_hmac, decrypt, encrypt, load_aes_key, verify_hmac,
)


class CryptoLabTests(unittest.TestCase):
    def setUp(self):
        self.key = bytes(range(32))

    def test_aes_gcm_round_trip(self):
        envelope = encrypt(b"secret payload", self.key, b"tenant=alpha")
        self.assertEqual(decrypt(envelope, self.key), b"secret payload")

    def test_aad_mismatch_fails(self):
        envelope = encrypt(b"payload", self.key, b"tenant=alpha")
        with self.assertRaises(CryptoInputError):
            decrypt(envelope, self.key, b"tenant=beta")

    def test_ciphertext_tampering_fails(self):
        envelope = encrypt(b"payload", self.key)
        raw = bytearray(base64.b64decode(envelope["ciphertext_b64"]))
        raw[0] ^= 1
        envelope["ciphertext_b64"] = base64.b64encode(raw).decode()
        with self.assertRaises(CryptoInputError):
            decrypt(envelope, self.key)

    def test_wrong_key_fails(self):
        envelope = encrypt(b"payload", self.key)
        with self.assertRaises(CryptoInputError):
            decrypt(envelope, bytes(reversed(self.key)))

    def test_nonce_is_fresh(self):
        first = encrypt(b"same", self.key)
        second = encrypt(b"same", self.key)
        self.assertNotEqual(first["nonce_b64"], second["nonce_b64"])

    def test_rejects_bad_key_length(self):
        with self.assertRaises(CryptoInputError):
            encrypt(b"x", b"short")

    def test_hmac_valid_and_invalid(self):
        tag = create_hmac(b"message", self.key)
        self.assertTrue(verify_hmac(b"message", self.key, tag))
        self.assertFalse(verify_hmac(b"modified", self.key, tag))

    def test_hmac_rejects_short_key(self):
        with self.assertRaises(CryptoInputError):
            create_hmac(b"message", b"tiny")

    def test_strict_base64_key_loading(self):
        encoded = base64.b64encode(self.key).decode()
        self.assertEqual(load_aes_key(encoded), self.key)
        with self.assertRaises(CryptoInputError):
            load_aes_key("not-base64!")
        with self.assertRaises(CryptoInputError):
            load_aes_key(base64.b64encode(b"short").decode())


if __name__ == "__main__":
    unittest.main()
