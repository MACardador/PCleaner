from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, func, and_, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///local_database.db', echo=True)
Base = declarative_base()


def create_tables():
    Base.metadata.create_all(engine)


class Metadata:
    def __init__(self, width: int, height: int, channel: int, file_type: str):
        self.file_type = file_type
        self.channel = channel
        self.height = height
        self.width = width


class File(Base):
    __tablename__ = 'file_info'
    id = Column(Integer, primary_key=True)

    directory = Column(String)
    file = Column(String)
    metadata_width = Column(Integer)
    metadata_height = Column(Integer)
    metadata_channel = Column(Integer)
    metadata_type = Column(String)

    def __init__(self, _id, directory: str, file: str, metadata: Metadata):
        self.id = _id
        self.directory = directory
        self.file = file
        self.metadata_width = metadata.width
        self.metadata_height = metadata.height
        self.metadata_channel = metadata.channel
        self.metadata_type = metadata.file_type

    # @staticmethod
    # def id_directory_file(_id: int, directory: str, file: str):
    #     return File(_id, directory, file, None)

    @property
    def get_all_path(self):
        return '{}\\{}'.format(self.directory, self.file)


def insert_file_info(file):
    session = sessionmaker(bind=engine)()
    session.add(file)
    session.commit()


def get_grouped_files():
    session = sessionmaker(bind=engine)()
    return session.query(
        File.metadata_width, File.metadata_height, File.metadata_channel, File.metadata_type). \
        group_by(File.metadata_width, File.metadata_height, File.metadata_channel, File.metadata_type). \
        having(func.count() > 1). \
        all()


def get_files_by_metadata(metadata: Metadata):
    session = sessionmaker(bind=engine)()
    return session.query(File).filter(
        and_(
            File.metadata_width == metadata.width,
            File.metadata_height == metadata.height,
            File.metadata_channel == metadata.channel,
            File.metadata_type == metadata.file_type)
    ).all()


class Duplicate(Base):
    __tablename__ = 'duplicate_info'
    id = Column(Integer, primary_key=True)
    main_key = Column(Integer, ForeignKey(File.id))
    main_dir = Column(String)
    main_file = Column(String)
    other_key = Column(Integer, ForeignKey(File.id))
    other_dir = Column(String)
    other_file = Column(String)
    modified_date = Column(DateTime(timezone=True), server_default=func.now())

    def __init__(self, main_key, main_dir, original_file, other_key, other_dir, other_file):
        self.main_key = main_key
        self.main_dir = main_dir
        self.main_file = original_file
        self.other_key = other_key
        self.other_dir = other_dir
        self.other_file = other_file

def insert_duplicate(info: Duplicate):
    session = sessionmaker(bind=engine)()
    session.add(info)
    session.commit()


def get_duplicate():
    session = sessionmaker(bind=engine)()
    session.query(Duplicate). \
        order_by(Duplicate.modified_date.desc()). \
        first()


def drop_tables():
    File.__table__.drop(engine)
    Duplicate.__table__.drop(engine)
