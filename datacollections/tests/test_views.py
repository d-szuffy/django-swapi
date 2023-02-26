from django.test import TestCase
from datacollections.models import DataSet
from unittest.mock import patch, Mock
import os
from django.conf import settings


class CollectionPageView(TestCase):

    def test_uses_collections_template(self):
        response = self.client.get("/datacollections/")
        self.assertTemplateUsed(response, 'datacollections/collections.html')

    def test_displays_only_created_files(self):
        DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")

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

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_throws_TypeError_when_API_inaccesible(self,
                                                        mock_create_csv_file):
        mock_create_csv_file.return_value = None
        self.client.post('/datacollections/new_collection')

        self.assertRaises(TypeError)

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_creates_dataset_associated_with_fetched_CSV(self, mock_create_csv_file):
        file_name = '167777.csv'
        path_to_file = os.path.join(settings.MEDIA_ROOT, file_name)
        mock_create_csv_file.return_value = (file_name, path_to_file, 'Some table')
        self.client.post('/datacollections/new_collection')

        dataset = DataSet.objects.first()

        self.assertEqual(dataset.file_path, path_to_file)