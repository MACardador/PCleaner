import os.path
import unittest
from unittest import mock
from unittest.mock import patch

import jsonpickle
from jsonpickle import json

import process
import service
from unittest.mock import MagicMock
from dto import folder
from repository.files_collection import FilesCollection


class TestProcess(unittest.TestCase):

    def test_recursive_folder(self):
        with patch('os.listdir') as mocked_listdir:
            with patch('os.path.isdir') as mocked_isdir:
                mocked_listdir.return_value = ["Photos.jpeg"]
                mocked_isdir.side_effect = [False]
                directory = "C:\\some\\folder"
                folders = set()
                process.recursive_folder(directory, folders)
                self.assertTrue(len(folders) == 1)

    def test_get_folders(self):
        with patch('process.get_drives') as mocked_drives:
            with patch('os.listdir') as mocked_listdir:
                with patch('os.path.isdir') as mocked_isdir:
                    mocked_listdir.return_value = ["Photos.jpeg"]
                    mocked_isdir.side_effect = [False]
                    mocked_drives.return_value = ["C:\\"]

                    result = process.get_folders()
                    decoded = jsonpickle.decode(result)
            [print(u) for u in decoded]
            self.assertEqual(folder.Folder("C:\\").directory, next(iter(decoded)).directory)

    # def test_get_possible_duplicates(self):
    #     with patch("repository.files_collection.get_duplicated_size_and_type") as mocked_get_duplicate:
    #         mocked_get_duplicate.return_value = json.dumps([{
    #             "_id": "ObjectId('609c4f65db448caadd3cb8d6')",
    #             "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-bpmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
    #             "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 48, 106000)",
    #             "metadata": {
    #                 "width": 1152, "height": 768, "size": 884736, "type": "jpg"}
    #         }, {
    #             "_id": "ObjectId('609c4f65db448caadd3cb8dd')",
    #             "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-dmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
    #             "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 49, 375000)",
    #             "metadata": {
    #                 "width": 1152, "height": 768, "size": 884736, "type": "jpg"}
    #             }])
    #
    #     service.handle_candidate_duplicate_file()

    @staticmethod
    @mock.patch("FilesCollection.get_duplicated_size_and_type")
    def fake_get_duplicated_size_and_type():
        return json.dumps([
            {
                "_id": "ObjectId('609c4f65db448caadd3cb8d6')",
                "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-bpmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
                "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 48, 106000)",
                "metadata": {
                    "width": 1152, "height": 768, "size": 884736, "type": "jpg"
                }},
            {
                "_id": "ObjectId('609c4f65db448caadd3cb8dd')",
                "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-dmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
                "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 49, 375000)",
                "metadata": {
                    "width": 1152, "height": 768, "size": 884736, "type": "jpg"}
            }])

    def test_get_possible_duplicates(self):
        with patch.object(FilesCollection, "get_duplicated_size_and_type",
                          return_value=
                          [{"files": [
                               {
                                   "_id": "ObjectId('609c4f65db448caadd3cb8d6')",
                                   "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-bpmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
                                   "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 48, 106000)",
                                   "metadata": {
                                       "width": 1152, "height": 768, "size": 884736, "type": "jpg"
                                   }},
                               {
                                   "_id": "ObjectId('609c4f65db448caadd3cb8dd')",
                                   "file": "C:\\Users\\migue\\.vscode\\extensions\\redhat.vscode-extension-dmn-editor-0.8.3\\dist\\images\\pfbg_576@2x.jpg",
                                   "createdDate": "datetime.datetime(2021, 5, 12, 22, 55, 49, 375000)",
                                   "metadata": {
                                       "width": 1152, "height": 768, "size": 884736, "type": "jpg"}
                               }]
                           }]):
            service.handle_candidate_duplicate_file()

    def test_get_possible_duplicates_exec(self):
        service.handle_candidate_duplicate_file()


if __name__ == '__main__':
    unittest.main()
