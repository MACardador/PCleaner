import cv2

from database.DTO.FilesDto import File
from database.DTO.DuplicateDto import Duplicate
from database.DuplicateInfoDAO import insert_duplicate


def compare_image(f_file: File, s_file: File):
    image_a = cv2.imread(f_file.get_all_path)
    image_b = cv2.imread(s_file.get_all_path)

    differences = cv2.subtract(image_a, image_b)
    b, q, r = cv2.split(differences)

    if cv2.countNonZero(b) == 0 and cv2.countNonZero(q) == 0 and cv2.countNonZero(r) == 0:
        file = Duplicate(f_file.id, f_file.directory, f_file.file, s_file.id, s_file.directory, s_file.file)
        insert_duplicate(file)


def handle_candidate_duplicate_file(results):
    for result in results:
        for file in result:
            result.remove(file)
            for other_file in result:
                compare_image(File.id_directory_file(*file), File.id_directory_file(*other_file))
