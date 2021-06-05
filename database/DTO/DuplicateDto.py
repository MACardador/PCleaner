from datetime import datetime


class Duplicate:
    def __init__(self, main_key, main_dir, original_file, other_key, other_dir, other_file):
        self.main_key = main_key
        self.main_dir = main_dir
        self.main_file = original_file
        self.other_key = other_key
        self.other_dir = other_dir
        self.other_file = other_file
        self.modified_date = datetime

