import json

from django.test import TestCase
from django.urls import reverse

from techtest.article.models import Article
from techtest.author.models import Author
from techtest.region.models import Region


class ArticleListViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("articles-list")
        self.article_1 = Article.objects.create(title="Fake Article 1")
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.article_2 = Article.objects.create(
            title="Fake Article 2", content="Lorem Ipsum"
        )
        self.article_2.regions.set([self.region_1, self.region_2])

        self.author = Author.objects.create(
            first_name="First name",
            last_name="Last Name"
        )
        self.article_2.author = self.author
        self.article_2.save()

    def test_serializes_with_correct_data_shape_and_status_code(self):
        """There is no raw serializer test"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        jresp = response.json()
        self.assertCountEqual(
            jresp,
            [
                {
                    "id": self.article_1.id,
                    "title": "Fake Article 1",
                    "content": "",
                    "author": {},
                    "regions": [],
                },
                {
                    "id": self.article_2.id,
                    "title": "Fake Article 2",
                    "content": "Lorem Ipsum",
                    "author": {
                        "id": 1,
                        "first_name": "First name",
                        "last_name": "Last Name"
                    },
                    "regions": [
                        {
                            "id": self.region_1.id,
                            "code": "AL",
                            "name": "Albania",
                        },
                        {
                            "id": self.region_2.id,
                            "code": "UK",
                            "name": "United Kingdom",
                        },
                    ],
                },
            ],
        )

    def test_creates_new_article_with_regions(self):
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"code": "AU", "name": "Austria"},
            ],
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 3",
                "content": "To be or not to be",
                "author": {},
                "regions": [
                    {
                        "id": regions.all()[0].id,
                        "code": "US",
                        "name": "United States of America",
                    },
                    {"id": regions.all()[1].id, "code": "AU", "name": "Austria"},
                ],
            },
            response.json(),
        )


    def test_creates_new_article_with_author(self):
        """Create a new article and an author binded to it"""
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "author": {
                "first_name": "FN",
                "last_name": "LN"
            },
            "regions": [],
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 0)
        jresp = response.json()
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 3",
                "content": "To be or not to be",
                "author": {
                    "id": 2,
                    "first_name": "FN",
                    "last_name": "LN"
                },
                "regions": [
                ],
            },
            jresp,
        )

    def test_creates_new_article_with_existing_author(self):
        """Create a new article with an existing author by his ID"""
        new_author = Author.objects.create(first_name="New FN", last_name="New LN")
        payload = {
            "title": "Fake Article 3",
            "content": "To be or not to be",
            "author": {
                "id": new_author.pk
            },
            "regions": [],
        }
        response = self.client.post(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 0)
        jresp = response.json()
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 3",
                "content": "To be or not to be",
                "author": {
                    "id": new_author.id,
                    "first_name": new_author.first_name,
                    "last_name": new_author.last_name
                },
                "regions": [
                ],
            },
            jresp,
        )


class ArticleViewTestCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="First name",
            last_name="Last Name"
        )
        self.article = Article.objects.create(title="Fake Article 1", author=self.author)
        self.region_1 = Region.objects.create(code="AL", name="Albania")
        self.region_2 = Region.objects.create(code="UK", name="United Kingdom")
        self.article.regions.set([self.region_1, self.region_2])
        self.url = reverse("article", kwargs={"article_id": self.article.id})

    def test_serializes_single_record_with_correct_data_shape_and_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(
            response.json(),
            {
                "id": self.article.id,
                "title": "Fake Article 1",
                "content": "",
                "author": {
                    "id": 1,
                    "first_name": "First name",
                    "last_name": "Last Name"
                },
                "regions": [
                    {
                        "id": self.region_1.id,
                        "code": "AL",
                        "name": "Albania",
                    },
                    {
                        "id": self.region_2.id,
                        "code": "UK",
                        "name": "United Kingdom",
                    },
                ],
            },
        )

    def test_updates_article_and_regions(self):
        # Change regions
        payload = {
            "title": "Fake Article 1 (Modified)",
            "content": "To be or not to be here",
            "regions": [
                {"code": "US", "name": "United States of America"},
                {"id": self.region_2.id},
            ],
        }
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.first()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 2)
        self.assertEqual(Article.objects.count(), 1)
        jresp = response.json()
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 1 (Modified)",
                "content": "To be or not to be here",
                "author": {
                    "id": 1,
                    "first_name": "First name",
                    "last_name": "Last Name"
                },
                "regions": [
                    {
                        "id": self.region_2.id,
                        "code": "UK",
                        "name": "United Kingdom",
                    },
                    {
                        "id": regions.all()[1].id,
                        "code": "US",
                        "name": "United States of America",
                    },
                ],
            },
            jresp,
        )
        # Remove regions and the author
        payload["regions"] = []
        payload["author"] = None
        response = self.client.put(
            self.url, data=json.dumps(payload), content_type="application/json"
        )
        article = Article.objects.last()
        regions = Region.objects.filter(articles__id=article.id)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(article)
        self.assertEqual(regions.count(), 0)
        jresp = response.json()
        self.assertDictEqual(
            {
                "id": article.id,
                "title": "Fake Article 1 (Modified)",
                "content": "To be or not to be here",
                "author": {
                },
                "regions": [],
            },
            jresp,
        )

    def test_removes_article(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 0)
