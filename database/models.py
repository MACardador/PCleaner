from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, func, and_, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database.DTO.FilesDto import Metadata

engine = create_engine('sqlite:///sales.db', echo=True)
Base = declarative_base()

Base.metadata.create_all(engine)


class File(Base):
    __tablename__ = 'file_info'
    id = Column(Integer, primary_key=True)

    directory = Column(String)
    file = Column(String)
    metadata_width = Column(Integer)
    metadata_height = Column(Integer)
    metadata_channel = Column(Integer)
    metadata_type = Column(Integer)


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
        subquery()


def get_files_by_metadata(metadata: Metadata):
    session = sessionmaker(bind=engine)()
    return session.query(File).filter(
        and_(
            File.metadata_width == metadata.width,
            File.metadata_height == metadata.height,
            File.metadata_channel == metadata.channel,
            File.metadata_type == metadata.file_type)
    )


class Duplicate(Base):
    __tablename__ = 'duplicate_info'
    main_key = Column(Integer, ForeignKey(File.id))
    main_dir = Column(String)
    main_file = Column(String)
    other_key = Column(Integer, ForeignKey(File.id))
    other_dir = Column(String)
    other_file = Column(String)
    modified_date = Column(DateTime(timezone=True), server_default=func.now())


def insert_duplicate(info: Duplicate):
    session = sessionmaker(bind=engine)()
    session.add(info)
    session.commit()


def get_duplicate():
    session = sessionmaker(bind=engine)()
    session.query(Duplicate). \
        order_by(Duplicate.modified_date.desc()). \
        first()
