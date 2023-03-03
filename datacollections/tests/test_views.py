from django.test import TestCase, RequestFactory
from datacollections.models import DataSet
from unittest.mock import patch, Mock
import os
from django.conf import settings
from datacollections.fetch import COLUMNS
from pyfakefs.fake_filesystem_unittest import TestCase as FakefsTestCase
from parameterized import parameterized
from datacollections import views
from datacollections.fetch import FetchData
import constants

class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'datacollections/home.html')


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


class NewCollectionTest(TestCase):

    def new_collection_success(self):
        file_name = '167777.csv'
        path_to_file = os.path.join(settings.MEDIA_ROOT, file_name)
        return file_name, path_to_file, "some table"

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_adds_success_message(self, mock_create_csv_file):
        mock_create_csv_file.return_value = self.new_collection_success()
        response = self.client.post('/datacollections/new_collection', follow=True)
        message = list(response.context['messages'])[0]

        self.assertEqual(message.message,
                         "Data fetched successfully."
                         )

    @patch('datacollections.fetch.FetchData.create_csv_file')
    def test_adds_error_message(self, mock_create_csv_file):
        mock_create_csv_file.return_value = None
        response = self.client.post('/datacollections/new_collection', follow=True)
        message = list(response.context['messages'])[0]

        self.assertEqual(message.message,
                         "Something went wrong"
                         )

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_redirects_to_view_collections(self, mock_create_csv_file):
        mock_create_csv_file.return_value = self.new_collection_success()

        response = self.client.post('/datacollections/new_collection')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/datacollections/')

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_throws_TypeError_when_API_inaccessible(self,
                                                         mock_create_csv_file):
        mock_create_csv_file.return_value = None
        self.client.post('/datacollections/new_collection')

        self.assertRaises(TypeError)

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_invalid_API_response_nothing_saved_to_db(self,
                                                      mock_create_csv_file):
        mock_create_csv_file.return_value = None
        self.client.post('/datacollections/new_collection')

        self.assertEqual(DataSet.objects.count(), 0)

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_invalid_API_response_redirects_to_collection_template(self,
                                                                   mock_create_csv_file):
        mock_create_csv_file.return_value = None
        response = self.client.post('/datacollections/new_collection')

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/datacollections/')

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_invalid_API_response_shows_error_on_page(self,
                                                      mock_create_csv_file):
        mock_create_csv_file.return_value = None
        response = self.client.post('/datacollections/new_collection', follow=True)

        self.assertContains(response, "Something went wrong")

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_sends_request_to_external_api(self, mock_create_csv_file):
        mock_create_csv_file.return_value = self.new_collection_success()
        self.client.post('/datacollections/new_collection')

        self.assertTrue(mock_create_csv_file.called)

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_creates_dataset_associated_with_fetched_CSV(self, mock_create_csv_file):
        mock_create_csv_file.return_value = self.new_collection_success()
        self.client.post('/datacollections/new_collection')

        dataset = DataSet.objects.first()

        self.assertEqual(dataset.file_path, self.new_collection_success()[1])

    @patch('datacollections.views.FetchData.create_csv_file')
    def test_POST_success_message_on_page(self, mock_create_csv_file):
        mock_create_csv_file.return_value = self.new_collection_success()
        response = self.client.post('/datacollections/new_collection', follow=True)

        self.assertContains(response, "Data fetched successfully.")


class CollectionDetailsTest(TestCase):

    def test_uses_collection_details_template(self):
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        response = self.client.get(f'/datacollections/collection_details/{dataset.id}/')
        self.assertTemplateUsed(response, 'datacollections/collection_details.html')

    def test_passes_correct_dataset_to_template(self):
        correct_dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        wrong_dataset = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")

        response = self.client.get(f'/datacollections/collection_details/{correct_dataset.id}/')
        self.assertEqual(response.context['dataset'], correct_dataset)

    def test_shows_correct_dataset_title(self):
        correct_dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        wrong_dataset = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")

        response = self.client.get(f'/datacollections/collection_details/{correct_dataset.id}/')
        self.assertContains(response, 'File1')

    @patch('datacollections.utils.get_data')
    @patch('datacollections.utils.get_headers')
    def test_passes_correct_table_headers_to_template(self,
                                                      mock_get_headers,
                                                      mock_get_data):
        mock_get_headers.return_value = COLUMNS
        mock_get_data.return_value = [[i for i in range(1)] for i in range(1)]
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")

        response = self.client.get(f'/datacollections/collection_details/{dataset.id}/')

        self.assertEqual(response.context['headers'], COLUMNS)

    @parameterized.expand([('', 1),
                          ('?page=1', 1),
                          ('?page=4', 4)])
    @patch('datacollections.utils.get_data')
    @patch('datacollections.utils.get_headers')
    def test_passes_correct_number_of_pages_to_template(self,
                                                        page_number,
                                                        expected_result,
                                                        mock_get_headers,
                                                        mock_get_data):
        mock_get_headers.return_value = COLUMNS
        mock_get_data.return_value = [{'name': 'item{}'.format(i)} for i in range(1, 40)]
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")

        response = self.client.get(f'/datacollections/collection_details/{dataset.id}/{page_number}')

        self.assertEqual(len(response.context['data']), expected_result)

    def test_displays_error_message_when_file_not_found(self):
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        response = self.client.get(f'/datacollections/collection_details/{dataset.id}/')
        message = list(response.context['messages'])[0]

        self.assertEqual(message.message,
                         "Sorry, the file you are looking for was not found."
                         )


class ValueCountViewTest(FakefsTestCase):

    def setUp(self) -> None:
        self.setUpPyfakefs()

    def create_fake_csv(self):
        filename, path, table = FetchData().transform_data(constants.PAGE_PEOPLE['results'],
                                                           constants.PAGE_PLANETS['results'])


    @patch('datacollections.utils.group_by_columns')
    def test_uses_value_count_template(self, mock_group_by_columns):
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        checks = '?checks%5B%5D={}&checks%5B%5D={}'.format('name', 'homeworld')
        mock_group_by_columns.return_value = ['test']

        response = self.client.get(f'/datacollections/collection_details/value_count/{dataset.id}/{checks}')
        self.assertTemplateUsed(response, 'datacollections/value_count.html')

    @patch('datacollections.utils.group_by_columns')
    def test_passes_correct_dataset_to_template(self, mock_group_by_columns):
        correct_dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        wrong_dataset = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")
        checks = '?checks%5B%5D={}&checks%5B%5D={}'.format('name', 'homeworld')
        mock_group_by_columns.return_value = ['test']

        response = self.client.get(f'/datacollections/collection_details/value_count/{correct_dataset.id}/{checks}')
        self.assertEqual(response.context['dataset'], correct_dataset)

    @patch('datacollections.utils.group_by_columns')
    def test_shows_correct_dataset_title(self, mock_group_by_columns):
        correct_dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        wrong_dataset = DataSet.objects.create(filename="File2", file_path="/Desktop/example2.csv")
        checks = '?checks%5B%5D={0}&checks%5B%5D={1}'.format('name', 'homeworld')
        mock_group_by_columns.return_value = ['test']

        response = self.client.get(f'/datacollections/collection_details/value_count/{correct_dataset.id}/{checks}')
        self.assertContains(response, 'File1')

    @patch('datacollections.utils.group_by_columns')
    def test_parse_correct_columns_from_url(self, mock_group_by_columns):
        dataset = DataSet.objects.create(filename="File1", file_path="/Desktop/example1.csv")
        checks = '?checks%5B%5D={0}&checks%5B%5D={1}'.format('name', 'homeworld')
        mock_group_by_columns.return_value = ['test']

        response = self.client.get()

        #request = factory.get(f'/datacollections/collection_details/value_count/{dataset.id}/', {'checks[]': columns})
        #print(request)
        # response = self.client.get(f'/datacollections/collection_details/value_count/{dataset.id}/?{checks}')
        #
        # self.assertEqual(response.context("checks[]"), columns)
