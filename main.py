from database.DTO.FilesDto import Metadata, File
from database.DuplicateInfoDAO import create_duplicate_info_table, drop_duplicate_info_table
from database.InfoFileDAO import create_file_info_table, drop_file_info_table, get_grouped_files, get_files_by_metadata
from Service.DuplicateService import handle_candidate_duplicate_file
from Service.FilesService import search_folders


def create_tables():
    create_file_info_table()
    create_duplicate_info_table()


def drop_tables():
    drop_file_info_table()
    drop_duplicate_info_table()


def main_process():
    drop_tables()
    create_tables()
    search_folders()
    handle_candidate_duplicate_file([get_files_by_metadata(metadata) for metadata in
                                     [Metadata(*metadata) for metadata in get_grouped_files()]])


if __name__ == '__main__':
    main_process()
