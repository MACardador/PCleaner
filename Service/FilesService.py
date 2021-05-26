import cv2

from repository.duplicate_collection import DuplicateCollection
from repository.files_collection import FilesCollection


def get_drives():
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    return drives


def recursive_folder(self, folders: list):
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
                    recursive_folder(new, folders)
                elif extension.search(new):

                    im = cv2.imread(new)
                    if im is not None:

                        new_dict = create_dict(file.search(new).group(1), file.search(new).group(2),
                                               metadata(im.shape, extension.search(new).group()))
                        if new_dict not in folders:
                            folders.append(new_dict)

    except PermissionError:
        print(f"Access denied to read")


def get_folders(drive):
    print(f" Drive -> {drive}")
    folders = list()
    recursive_folder(drive, folders)
    # check async process in python, could be done separate process for each drive

    return folders




def add_files(files):
    FilesCollection.insert_all(files)


def compare_image(f_file: str, s_file: str):
    image_a = cv2.imread(f_file)
    image_b = cv2.imread(s_file)

    differences = cv2.subtract(image_a, image_b)
    b, q, r = cv2.split(differences)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(q) == 0 and cv2.countNonZero(r) == 0:
        DuplicateCollection.insert(DuplicateCollection.create_duplicate_dict(f_file, s_file))
        print("insert mongo")


def handle_candidate_duplicate_file():
    for results in FilesCollection.get_duplicated_size_and_type():
        results_files = results["results"]
        for res in results_files:
            results_files.remove(res)
            for other_res in results_files:
                print(res['_id'])
                print(other_res['_id'])
                compare_image(res['folder']+"\\\\"+res['file'], other_res['folder']+"\\\\"+other_res['file'])
