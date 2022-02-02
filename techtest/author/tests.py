import json
import random
import string

from django.test import TestCase
from django.urls import reverse

from techtest.author.models import Author


def random_string(number):
    return ''.join(random.choice(string.ascii_letters) for _ in range(number))

class AuthorListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("author-list")
        self.author = Author.objects.create(
            first_name="First name",
            last_name="Last Name"
        )
        self.author_2 = self.create_author()

    def create_author(self):
        return Author.objects.create(
            first_name=random_string(8),
            last_name=random_string(8),
        )

    def test_serializes_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        jresp = response.json()
        self.assertCountEqual(
            jresp,
            [
                {
                    "id": self.author.pk,
                    "first_name": self.author.first_name,
                    "last_name": self.author.last_name,
                },
                {
                    "id": self.author_2.pk,
                    "first_name": self.author_2.first_name,
                    "last_name": self.author_2.last_name,
                },
            ],
        )

    def test_creates_new_author(self):
        payload = {
            "first_name": "Test FN",
            "last_name": "Test LN",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(author)
        
        jresp = response.json()
        payload["id"] = author.pk
        self.assertDictEqual(
            jresp,
            payload
        )

    def test_creates_new_author_new(self):
        """Should fail — we don't create the new author when the ID is specidifed"""
        payload = {
            "id": self.author_2.id,
            "first_name": "Test FN",
            "last_name": "Test LN",
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(author)
        
        jresp = response.json()
        payload["id"] = author.pk
        self.assertNotEqual(
            jresp,
            {
                "id": self.author_2.id,
                "first_name": "Test FN",
                "last_name": "Test LN",
            }
        )


class AuthorViewTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name=random_string(8),
            last_name=random_string(8)
        )
        self.url = reverse("author", kwargs={"pk": self.author.id})

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        jresp = response.json()
        self.assertCountEqual(
            jresp,
            {
                "id": self.author.pk,
                "first_name": self.author.first_name,
                "last_name": self.author.last_name
            },
        )

    def test_updates_author(self):
        # Change regions
        payload = {
            "first_name": random_string(12),
            "last_name": random_string(12),
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        author = Author.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(author)
        self.assertEqual(Author.objects.count(), 1)
        jresp = response.json()
        self.assertDictEqual(
            jresp,
            {
                "id": author.id,
                "first_name": author.first_name,
                "last_name": author.last_name,
            },
        )

    def test_removes_author(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Author.objects.count(), 0)
