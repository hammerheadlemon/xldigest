import reprlib
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# engine = create_engine('sqlite:////home/lemon/code/python/xldigest/xldigest/'
#                       'db.sqlite')

class SeriesItem(Base):
    __tablename__ = 'series_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    series = Column(Integer, ForeignKey('series.id'))
    start_date = Column(Date)
    end_date = Column(Date)

    def __repr__(self):
        return reprlib.repr(self.name)


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    series_items = relationship("SeriesItem")

    def __repr__(self):
        return reprlib.repr(self.name)


class Portfolio(Base):
    __tablename__ = 'portfolios'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    projects = relationship("Project")

    def __repr__(self):
        return reprlib.repr(self.name)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    portfolio = Column(Integer, ForeignKey('portfolios.id'))
    returnitems = relationship("ReturnItem")

    def __repr__(self):
        return "<Project(name='{0}')>".format(self.name)


class RetainedSourceFile(Base):
    __tablename__ = 'retained_source_files'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    portfolio_id = Column(Integer, ForeignKey('portfolios.id'))
    series_item_id = Column(Integer, ForeignKey('series_items.id'))
    uuid = Column(String)

    def __repr__(self):
        return "Retained Source File {} - {}".format(self.id, self.project_id)


class DatamapItem(Base):
    __tablename__ = 'datamap_items'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    bicc_sheet = Column(String)
    bicc_cellref = Column(String)
    gmpp_sheet = Column(String)
    gmpp_cellref = Column(String)
    bicc_ver_form = Column(String)
    return_items = relationship("ReturnItem")

    def __repr__(self):
        return reprlib.repr(self.key)


class ReturnItem(Base):
    __tablename__ = 'returns'

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    series_item_id = Column(Integer, ForeignKey('series_items.id'))
    datamap_item_id = Column(Integer, ForeignKey('datamap_items.id'))
    value = Column(String)

    def __repr__(self):
        return reprlib.repr(self.value)


def create_tables(engine):
    Base.metadata.create_all(engine)
