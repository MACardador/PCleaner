from multiprocessing import Pool
from process import get_folders
from process import get_drives
from repository.duplicate_collection import DuplicateCollection
from repository.files_collection import FilesCollection
from service import add_files, handle_candidate_duplicate_file
import functools
import operator

result_list = []


def get_all_folders():
    pool = Pool()
    multiple_results = [pool.apply_async(func=get_folders, args=(drive,)) for drive
                        in get_drives()]
    pool.close()
    pool.join()

    return functools.reduce(operator.iconcat, map(lambda result: result.get(), multiple_results), [])


def drop_collections():
    FilesCollection.drop()
    DuplicateCollection.drop()


if __name__ == '__main__':
    drop_collections()

    folders = get_all_folders()

    add_files(folders)

    handle_candidate_duplicate_file()




