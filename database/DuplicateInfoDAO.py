from database.DTO.DuplicateDto import Duplicate
from database.DataBase import cursor, conn


def create_duplicate_info_table():
    cursor.execute("""CREATE TABLE duplicate_info (
        main_key integer,
        main_dir text,
        main_file text,
        other_key integer,
        other_dir text,
        other_file text,
        modified_date DEFAULT CURRENT_TIMESTAMP NOT NULL,
        FOREIGN KEY(main_key) REFERENCES file_info(id)
        FOREIGN KEY(other_key) REFERENCES file_info(id)
    )""")


def drop_duplicate_info_table():
    cursor.execute("PRAGMA foreign_keys = OFF;")
    cursor.execute("DROP TABLE duplicate_info;")


def insert_duplicate(info: Duplicate):
    with conn:
        cursor.execute("""Insert INTO duplicate_info (main_key, main_dir, main_file, other_key, other_dir, other_file)
        VALUES (:main_key, :main_dir, :main_file, :other_key, :other_dir, :other_file)""",
                       {'main_key': info.main_key,
                        'main_dir': info.main_dir,
                        'main_file': info.main_file,
                        'other_key': info.other_key,
                        'other_dir': info.other_dir,
                        'other_file': info.other_file,
                        })


def get_duplicate():
    cursor.execute("""Select main_key, main_dir, main_file, other_key, other_dir, other_file, count()
                      FROM duplicate_info
                      ORDER BY modified_date ASC
                      LIMIT 1;""")
