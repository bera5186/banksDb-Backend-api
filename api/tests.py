from rest_framework.test import APITestCase
from rest_framework import status


class BranchTests(APITestCase):

    def test_bad_request_error_branch_autocomplete(self):
        """Fails due to q (query) not provided"""
        response = self.client.get("/api/branches/autocomplete/?format=json")
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.json()["error"])

    def test_status_ok_branch_autocomplete(self):
        """Response ok"""
        response = self.client.get("/api/branches/autocomplete/?format=json&limit=10&offset=1&q=east")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["error"])

    def test_bad_request_branch_search(self):
        """Fails due to q (query) not provided"""
        response = self.client.get("/api/branches/search/?format=json&city=mumbai")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.json()["error"])

    def test_bad_request_branch_search(self):
        """Fails due to city not provided"""
        response = self.client.get("/api/branches/search/?format=json&q=east")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.json()["error"])

    def test_status_ok_branch_search(self):
        """Response OK"""
        response = self.client.get("/api/branches/search/?format=json&q=east&city=mumbai")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["error"])


class BankTest(APITestCase):

    def test_not_found_id_not_passed(self):
        """Fails due to id not provided"""
        response = self.client.get("/api/bank/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_status_ok(self):
        """Response OK"""
        response = self.client.get("/api/banks/1")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()["error"])
