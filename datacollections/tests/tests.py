from django.test import TestCase


class HomePageView(TestCase):
    def test_uses_home_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, 'datacollections/home.html')


class CollectionPageView(TestCase):

    def test_uses_collections_template(self):
        response = self.client.get("/datacollections/")
        self.assertTemplateUsed(response, 'datacollections/collections.html')
