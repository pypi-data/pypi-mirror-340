import unittest
from unittest.mock import patch, MagicMock, mock_open
import sys
import os
import tempfile
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.signing.file_signer import FileSigner


class TestFileSigner(unittest.TestCase):
    """Test the FileSigner class"""

    def setUp(self):
        # Generate a test private key
        self.private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

        # Generate a PEM for the private key
        self.private_key_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

        # Create a self-signed certificate for testing
        subject = issuer = x509.Name(
            [
                x509.NameAttribute(x509.NameOID.COMMON_NAME, "Test Certificate"),
            ]
        )

        self.certificate = (
            x509.CertificateBuilder()
            .subject_name(subject)
            .issuer_name(issuer)
            .public_key(self.private_key.public_key())
            .serial_number(x509.random_serial_number())
            .not_valid_before(x509.datetime.datetime.utcnow())
            .not_valid_after(
                x509.datetime.datetime.utcnow() + x509.datetime.timedelta(days=10)
            )
            .sign(self.private_key, hashes.SHA256(), default_backend())
        )

        # Create a PEM for the certificate
        self.certificate_pem = self.certificate.public_bytes(serialization.Encoding.PEM)

        # Create a DER for the certificate (simulating Azure Key Vault certificate)
        self.certificate_der = self.certificate.public_bytes(serialization.Encoding.DER)

        # Create a mock Azure certificate with cer attribute
        self.mock_azure_cert = MagicMock()
        self.mock_azure_cert.cer = self.certificate_der

    def test_init_with_pem(self):
        """Test initialization with PEM format certificate and key"""
        signer = FileSigner(self.certificate_pem, self.private_key_pem)
        self.assertIsNotNone(signer.cert_obj)
        self.assertIsNotNone(signer.key_obj)

    def test_init_with_azure_cert(self):
        """Test initialization with Azure certificate object"""
        signer = FileSigner(self.mock_azure_cert, self.private_key_pem)
        self.assertIsNotNone(signer.cert_obj)
        self.assertIsNotNone(signer.key_obj)

    def test_sign_file(self):
        """Test signing a file"""
        # Create a temp file to sign
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content to sign")
            temp_path = temp_file.name

        try:
            # Create signer and sign the file
            signer = FileSigner(self.certificate_pem, self.private_key_pem)
            signature_path = signer.sign_file(temp_path)

            # Check that the signature file exists
            self.assertTrue(os.path.exists(signature_path))

            # Check that verification works
            self.assertTrue(signer.verify_signature(temp_path, signature_path))

            # Cleanup
            os.remove(signature_path)
        finally:
            # Cleanup
            os.remove(temp_path)

    def test_verify_signature(self):
        """Test verifying a signature"""
        # Create a temp file to sign
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(b"Test content to verify")
            temp_path = temp_file.name

        try:
            # Create signer and sign the file
            signer = FileSigner(self.certificate_pem, self.private_key_pem)
            signature_path = signer.sign_file(temp_path)

            # Create a new signer (to simulate reloading)
            signer2 = FileSigner(self.certificate_pem, self.private_key_pem)

            # Verify the signature
            self.assertTrue(signer2.verify_signature(temp_path, signature_path))

            # Modify the file and verify it fails
            with open(temp_path, "wb") as f:
                f.write(b"Modified content")

            self.assertFalse(signer2.verify_signature(temp_path, signature_path))

            # Cleanup
            os.remove(signature_path)
        finally:
            # Cleanup
            os.remove(temp_path)

    def test_sign_nonexistent_file(self):
        """Test signing a file that doesn't exist"""
        signer = FileSigner(self.certificate_pem, self.private_key_pem)
        result = signer.sign_file("/path/to/nonexistent/file")
        self.assertIsNone(result)

    def test_verify_nonexistent_file(self):
        """Test verifying a file that doesn't exist"""
        signer = FileSigner(self.certificate_pem, self.private_key_pem)
        result = signer.verify_signature("/path/to/nonexistent/file")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
