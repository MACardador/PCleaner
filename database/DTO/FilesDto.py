

class Metadata:
    def __init__(self, width: int, height: int, channel: int, file_type: str):
        self.file_type = file_type
        self.channel = channel
        self.height = height
        self.width = width


class File:
    def __init__(self, directory: str, file: str, metadata: Metadata):
        self.id = None
        self.directory = directory
        self.file = file
        self.metadata_width = metadata.width
        self.metadata_height = metadata.height
        self.metadata_channel = metadata.channel
        self.metadata_type = metadata.file_type


    def __init__(self, directory: str, file: str):
        self.id = None
        self.directory = directory
        self.file = file

    @property
    def get_all_path(self):
        return '{}\\{}'.format(self.directory, self.file)
