
from Service.DuplicateService import handle_candidate_duplicate_file
from Service.FilesService import search_folders
from database.models import get_files_by_metadata, Metadata, get_grouped_files, drop_tables, create_tables


def main_process():
    drop_tables()
    create_tables()
    search_folders()
    handle_candidate_duplicate_file([get_files_by_metadata(metadata) for metadata in
                                     [Metadata(*metadata) for metadata in get_grouped_files()]])


if __name__ == '__main__':
    main_process()
