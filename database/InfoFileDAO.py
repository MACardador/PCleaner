from database.DTO.FilesDto import Metadata
from database.DataBase import cursor, conn


def create_file_info_table():
    cursor.execute("""CREATE TABLE file_info (
        id integer PRIMARY KEY,
        directory text,
        file text,
        metadata_width integer,
        metadata_height integer,
        metadata_channel integer,
        metadata_type text
    )""")


def drop_file_info_table():
    cursor.execute("DROP TABLE file_info;")


def insert_file_info(file):
    with conn:
        cursor.execute("""Insert INTO file_info (directory, file, metadata_width, metadata_height, metadata_channel, metadata_type)
        VALUES (:directory, :file, :metadata_width, :metadata_height, :metadata_channel, :metadata_type)""",
                       {'directory': file.directory,
                        'file': file.file,
                        'metadata_width': file.metadata_width,
                        'metadata_height': file.metadata_height,
                        'metadata_channel': file.metadata_channel,
                        'metadata_type': file.metadata_type})


def get_grouped_files():
    cursor.execute("""SELECT metadata_width, metadata_height, metadata_channel, metadata_type
    FROM file_info
    GROUP BY metadata_width, metadata_height, metadata_channel, metadata_type
    HAVING COUNT() > 1;""")
    return cursor.fetchall()


def get_files_by_metadata(metadata: Metadata):
    cursor.execute("""SELECT id, directory, file
    FROM file_info
    WHERE metadata_width = :width
    AND metadata_height = :height
    AND metadata_channel = :channel
    AND metadata_type = :type""",
                   {'width': metadata.width, 'height': metadata.height, 'channel': metadata.channel,
                    'type': metadata.file_type})
    return cursor.fetchall()
