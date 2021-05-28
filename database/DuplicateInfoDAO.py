from database.DataBase import cursor, conn


def create_duplicate_info_table():
    cursor.execute("""CREATE TABLE duplicate_info (
        original_file_key integer,
        original_file text,
        duplicate_file_key integer
        duplicate_file text,
        FOREIGN KEY(original_file_key) REFERENCES file_info(id)
        FOREIGN KEY(duplicate_file_key) REFERENCES file_info(id)
    )""")


def drop_duplicate_info_table():
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DROP TABLE duplicate_info;")


def insert_duplicated(info):
    with conn:
        cursor.execute("""Insert INTO duplicate_info 
        VALUES (:original_file_key, :original_file, :duplicate_file_key, :duplicate_file)""",
                       {'original_file_key': info.original_file_key,
                        'original_file': info.original_file,
                        'duplicate_file_key': info.duplicate_file_key,
                        'duplicate_file': info.duplicate_file
                        })

