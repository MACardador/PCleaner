

class Metadata:
    def __init__(self, width: int, height: int, channel: int, file_type: str):
        self.file_type = file_type
        self.channel = channel
        self.height = height
        self.width = width


class File:
    def __init__(self, _id, directory: str, file: str, metadata: Metadata = None):
        self.id = _id
        self.directory = directory
        self.file = file
        self.metadata = metadata

    @staticmethod
    def id_directory_file(_id: int, directory: str, file: str):
        return File(_id, directory, file, None)

    @property
    def get_all_path(self):
        return '{}\\{}'.format(self.directory, self.file)
