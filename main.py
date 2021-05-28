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


if __name__ == '__main__':
    drop_tables()  # instead a file, could be in memory, that way after the process all storage info will disappear

    create_tables()

    search_folders()

    # files = [[File(*file_info) for file_info in get_files_by_metadata(Metadata(*metadata))]
    #          for metadata in get_grouped_files()]

    metadata_list = [Metadata(*metadata) for metadata in get_grouped_files()]

    results = [get_files_by_metadata(metadata) for metadata in metadata_list]

    files = [File(*file) for file in results]

    handle_candidate_duplicate_file(files)
