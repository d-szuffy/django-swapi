from django.test import TestCase
from datacollections.models import DataSet
from unittest.mock import patch, Mock


class CollectionPageView(TestCase):

    def test_uses_collections_template(self):
        response = self.client.get("/datacollections/")
        self.assertTemplateUsed(response, 'datacollections/collections.html')

    def test_displays_only_created_files(self):
        file1 = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        file2 = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")

        response = self.client.get("/datacollections/")

        self.assertContains(response, "File1")
        self.assertContains(response, "File2")
        self.assertNotContains(response, "File3")
        self.assertNotContains(response, "File4")

    def test_passes_correct_file_to_template(self):
        wrong_file = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        correct_file = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")
        response = self.client.get(f"/datacollections/collection_details/{correct_file.id}/")
        self.assertEqual(response.context["dataset"], correct_file)


class NewCollectionTest(TestCase):

    def test_POST_returns_None_when_API_is_inaccesible(self):
        self.fail("Write this test")

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_fetch_data_to_json(self, mock_create_csv_file):
        self.client.post('/datacollections/new_collection')

        self.fail("Write me!")