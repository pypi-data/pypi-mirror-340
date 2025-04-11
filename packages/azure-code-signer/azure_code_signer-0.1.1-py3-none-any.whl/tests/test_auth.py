import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from azure.core.exceptions import ResourceNotFoundError

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.auth.azure_auth import AzureAuth


class TestAzureAuth(unittest.TestCase):
    """Test the AzureAuth class"""

    def setUp(self):
        self.vault_url = "https://test-vault.vault.azure.net/"
        self.cert_name = "test-certificate"

    @patch("src.auth.azure_auth.DefaultAzureCredential")
    @patch("src.auth.azure_auth.CertificateClient")
    @patch("src.auth.azure_auth.SecretClient")
    def test_initialize(self, mock_secret_client, mock_cert_client, mock_credential):
        """Test the initialization of AzureAuth"""
        # Setup
        mock_credential.return_value = MagicMock()

        # Execute
        auth = AzureAuth(self.vault_url, self.cert_name)

        # Assert
        self.assertEqual(auth.key_vault_url, self.vault_url)
        self.assertEqual(auth.certificate_name, self.cert_name)
        self.assertIsNotNone(auth.credential)

    @patch("src.auth.azure_auth.DefaultAzureCredential")
    @patch("src.auth.azure_auth.CertificateClient")
    @patch("src.auth.azure_auth.SecretClient")
    def test_authenticate_success(
        self, mock_secret_client, mock_cert_client, mock_credential
    ):
        """Test successful authentication to Azure Key Vault"""
        # Setup
        mock_credential.return_value = MagicMock()
        mock_cert_client_instance = MagicMock()
        mock_cert_client_instance.list_properties_of_certificates.return_value = iter(
            [MagicMock()]
        )
        mock_cert_client.return_value = mock_cert_client_instance
        mock_secret_client.return_value = MagicMock()

        # Execute
        auth = AzureAuth(self.vault_url, self.cert_name)
        result = auth.authenticate()

        # Assert
        self.assertTrue(result)
        self.assertIsNotNone(auth.certificate_client)
        self.assertIsNotNone(auth.secret_client)
        mock_cert_client.assert_called_once_with(
            vault_url=self.vault_url, credential=auth.credential
        )
        mock_secret_client.assert_called_once_with(
            vault_url=self.vault_url, credential=auth.credential
        )

    @patch("src.auth.azure_auth.DefaultAzureCredential")
    @patch("src.auth.azure_auth.CertificateClient")
    @patch("src.auth.azure_auth.SecretClient")
    def test_authenticate_failure(
        self, mock_secret_client, mock_cert_client, mock_credential
    ):
        """Test authentication failure with Azure Key Vault"""
        # Setup
        mock_credential.return_value = MagicMock()
        mock_cert_client_instance = MagicMock()
        mock_cert_client_instance.list_properties_of_certificates.side_effect = (
            Exception("Authentication failed")
        )
        mock_cert_client.return_value = mock_cert_client_instance

        # Execute
        auth = AzureAuth(self.vault_url, self.cert_name)
        result = auth.authenticate()

        # Assert
        self.assertFalse(result)

    @patch("src.auth.azure_auth.DefaultAzureCredential")
    @patch("src.auth.azure_auth.CertificateClient")
    @patch("src.auth.azure_auth.SecretClient")
    def test_get_certificate_success(
        self, mock_secret_client, mock_cert_client, mock_credential
    ):
        """Test successful certificate retrieval"""
        # Setup
        mock_credential.return_value = MagicMock()
        mock_cert_client_instance = MagicMock()
        mock_cert_client_instance.list_properties_of_certificates.return_value = iter(
            [MagicMock()]
        )

        # Mock certificate
        mock_certificate = MagicMock()
        mock_certificate.cer = b"test-certificate-data"
        mock_cert_client_instance.get_certificate.return_value = mock_certificate

        mock_cert_client.return_value = mock_cert_client_instance

        # Mock secret
        mock_secret = MagicMock()
        mock_secret.value = "test-private-key"
        mock_secret_client_instance = MagicMock()
        mock_secret_client_instance.get_secret.return_value = mock_secret
        mock_secret_client.return_value = mock_secret_client_instance

        # Execute
        auth = AzureAuth(self.vault_url, self.cert_name)
        auth.authenticate()
        result = auth.get_certificate()

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result[0], mock_certificate)
        self.assertEqual(result[1], "test-private-key")
        mock_cert_client_instance.get_certificate.assert_called_once_with(
            self.cert_name
        )
        mock_secret_client_instance.get_secret.assert_called_once_with(self.cert_name)

    @patch("src.auth.azure_auth.DefaultAzureCredential")
    @patch("src.auth.azure_auth.CertificateClient")
    @patch("src.auth.azure_auth.SecretClient")
    def test_get_certificate_not_found(
        self, mock_secret_client, mock_cert_client, mock_credential
    ):
        """Test certificate not found in Key Vault"""
        # Setup
        mock_credential.return_value = MagicMock()
        mock_cert_client_instance = MagicMock()
        mock_cert_client_instance.list_properties_of_certificates.return_value = iter(
            [MagicMock()]
        )
        mock_cert_client_instance.get_certificate.side_effect = ResourceNotFoundError(
            "Certificate not found"
        )
        mock_cert_client.return_value = mock_cert_client_instance

        mock_secret_client_instance = MagicMock()
        mock_secret_client.return_value = mock_secret_client_instance

        # Execute
        auth = AzureAuth(self.vault_url, self.cert_name)
        auth.authenticate()
        result = auth.get_certificate()

        # Assert
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
