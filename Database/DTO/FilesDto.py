from datetime import date


class File:
    def __init__(self, directory, file, width, height, channel, file_type : str):
        self.directory = directory
        self.file = file
        self.created_date = date.datetime.now()
        self.metadata_width = width
        self.metadata_height = height
        self.metadata_channel = channel
        self.metadata_type = file_type
