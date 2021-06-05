import cv2
import os
import re
import win32api
from database.DTO.FilesDto import File, Metadata
from database.InfoFileDAO import insert_file_info


def get_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives


def recursive_folder(self):
    ignore_folder = re.compile(r"(.*.(sys|Msi|logbin)|Windows|lib|winutils|System Volume Information|AppData|\$)",
                               re.IGNORECASE)
    extension = re.compile(r'(s*(bmp|pbm|pgm|ppm|jpeg|jpg|jpe|jp2|tiff|tif)$)', re.IGNORECASE)
    file = re.compile(r'(.*[\\])(.*[.\\]\S*.$)', re.IGNORECASE)
    # for directory in directories:
    try:
        for entry in os.listdir(self):
            if not ignore_folder.match(entry):
                new = os.path.join(self, entry)
                if os.path.isdir(new):
                    recursive_folder(new)
                elif extension.search(new):
                    im = cv2.imread(new)
                    if im is not None:
                        height, width, channel = im.shape
                        insert_file_info(
                            File(None, file.search(new).group(1), file.search(new).group(2),
                                 Metadata(width, height, channel, extension.search(new).group())))

    except PermissionError:
        print(f"Access denied to read")


def search_folders():
    [recursive_folder(drive) for drive in get_drives()]
