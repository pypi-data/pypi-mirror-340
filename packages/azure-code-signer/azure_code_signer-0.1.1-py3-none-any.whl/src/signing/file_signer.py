import os
import logging
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class FileSigner:
    def __init__(self, certificate, private_key):
        """
        Initialize a file signer with certificate and private key

        Args:
            certificate: Certificate object from Azure Key Vault
            private_key: Private key for signing (PEM format)
        """
        self.certificate = certificate
        self.private_key = private_key
        self.logger = logging.getLogger(__name__)

        # Load certificate and private key into usable objects
        self._load_certificate_and_key()

    def _load_certificate_and_key(self):
        """Load certificate and private key into cryptography objects"""
        try:
            # Convert certificate to usable format
            if hasattr(self.certificate, "cer"):
                # If it's an Azure certificate object
                cert_bytes = self.certificate.cer
                # Ensure cert_bytes is bytes, not bytearray
                if isinstance(cert_bytes, bytearray):
                    cert_bytes = bytes(cert_bytes)
                self.cert_obj = x509.load_der_x509_certificate(
                    cert_bytes, default_backend()
                )
                self.cert_pem = self.cert_obj.public_bytes(
                    encoding=serialization.Encoding.PEM
                )
            else:
                # If it's already a PEM string or bytes
                if isinstance(self.certificate, str):
                    self.cert_pem = self.certificate.encode("utf-8")
                elif isinstance(self.certificate, bytearray):
                    self.cert_pem = bytes(self.certificate)
                else:
                    self.cert_pem = self.certificate
                self.cert_obj = x509.load_pem_x509_certificate(
                    self.cert_pem, default_backend()
                )

            # Convert private key to usable format
            if isinstance(self.private_key, str):
                private_key_bytes = self.private_key.encode("utf-8")
            elif isinstance(self.private_key, bytearray):
                private_key_bytes = bytes(self.private_key)
            else:
                private_key_bytes = self.private_key

            self.key_obj = serialization.load_pem_private_key(
                private_key_bytes, password=None, backend=default_backend()
            )

            self.logger.debug("Successfully loaded certificate and private key")
        except Exception as e:
            self.logger.error(
                f"Failed to load certificate and/or private key: {str(e)}"
            )
            raise

    def sign_file(self, file_path, output_path=None):
        """
        Sign a file using the certificate and private key

        Args:
            file_path (str): Path to the file to sign
            output_path (str, optional): Path where to save the signature
                                         If None, creates a .sig file next to the original

        Returns:
            str: Path to the signature file or None if signing failed
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return None

        try:
            # Determine output path for signature
            if not output_path:
                output_path = f"{file_path}.sig"

            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()

            # Create hash of the file
            file_hash = hashes.Hash(hashes.SHA256(), default_backend())
            file_hash.update(file_content)
            digest = file_hash.finalize()

            # Sign the hash
            signature = self.key_obj.sign(digest, padding.PKCS1v15(), hashes.SHA256())

            # Save signature to file
            with open(output_path, "wb") as f:
                f.write(signature)

            self.logger.debug(f"Successfully signed file: {file_path}")

            return output_path

        except Exception as e:
            self.logger.error(f"Failed to sign file {file_path}: {str(e)}")
            return None

    def verify_signature(self, file_path, signature_path=None):
        """
        Verify file signature using the certificate

        Args:
            file_path (str): Path to the file to verify
            signature_path (str, optional): Path to the signature file
                                            If None, assumes file_path + '.sig'

        Returns:
            bool: True if signature is valid, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.error(f"File not found: {file_path}")
            return False

        # Determine signature path
        if not signature_path:
            signature_path = f"{file_path}.sig"

        if not os.path.exists(signature_path):
            self.logger.error(f"Signature file not found: {signature_path}")
            return False

        try:
            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()

            # Create hash of the file
            file_hash = hashes.Hash(hashes.SHA256(), default_backend())
            file_hash.update(file_content)
            digest = file_hash.finalize()

            # Read signature
            with open(signature_path, "rb") as f:
                signature = f.read()

            # Get public key from certificate
            public_key = self.cert_obj.public_key()

            # Verify signature
            public_key.verify(signature, digest, padding.PKCS1v15(), hashes.SHA256())

            self.logger.debug(f"Signature is valid for file: {file_path}")
            return True

        except Exception as e:
            self.logger.debug(f"Signature verification failed: {str(e)}")
            return False
