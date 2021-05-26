import sqlite3

conn = sqlite3.connect('local_database.db')

cursor = conn.cursor()


def create_file_info_table():
    cursor.execute("""CREATE TABLE file_info (
        id integer PRIMARY KEY,
        directory text,
        file text,
        metadata_width integer
        metadata_height integer
        metadata_channel integer
        metadata_type text
    )""")


def insert_file_info(file):
    with conn:
        cursor.execute("""Insert INTO file_info 
        VALUES (:directory, :file, :metadata_width, :metadata_height, :metadata_channel, :metadata_type)""",
                       {'directory': file.directory,
                        'file': file.file,
                        'metadata_width': file.metadata_width,
                        'metadata_height': file.metadata_height,
                        'metadata_channel': file.metadata_channel,
                        'metadata_type': file.metadata_type})


def get_possible_duplicates():
    cursor.execute("""SELECT id, directory,file, metadata_width, metadata_height, metadata_channel, metadata_type, COUNT()
    FROM file_info
    GROUP BY metadata_width, metadata_height, metadata_channel, metadata_type
    HAVING COUNT() > 1;""")


def create_duplicate_info_table():
    cursor.execute("""CREATE TABLE duplicate_info (
        original_file_key integer,
        original_file text,
        duplicate_file_key integer
        duplicate_file text,
        FOREIGN KEY(original_file_key) REFERENCES file_info(id)
        FOREIGN KEY(duplicate_file_key) REFERENCES file_info(id)
    )""")


def insert_duplicated(info):
    with conn:
        cursor.execute("""Insert INTO duplicate_info 
        VALUES (:original_file_key, :original_file, :duplicate_file_key, :duplicate_file)""",
                       {'original_file_key': info.original_file_key,
                        'original_file': info.original_file,
                        'duplicate_file_key': info.duplicate_file_key,
                        'duplicate_file': info.duplicate_file
                        })

