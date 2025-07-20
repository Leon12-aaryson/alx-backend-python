#!/usr/bin/env python3
"""
Unit tests for client module.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value."""
        mock_get_json.return_value = {"payload": True}

        client = GithubOrgClient(org_name)
        result = client.org

        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        self.assertEqual(result, {"payload": True})

    def test_public_repos_url(self):
        """Test that GithubOrgClient._public_repos_url returns expected."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/google/repos"
            }

            client = GithubOrgClient("google")
            result = client._public_repos_url

            expected = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected)

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that GithubOrgClient.public_repos returns expected repos."""
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ]

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/google/repos"

            client = GithubOrgClient("google")
            result = client.public_repos()

            expected_repos = ["repo1", "repo2", "repo3"]
            self.assertEqual(result, expected_repos)
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/google/repos"
            )
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that GithubOrgClient.has_license returns expected result."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
