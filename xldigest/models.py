from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///test_sqa.db', echo=True)

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Project(name='{0}')>".format(self.name)


class Quarter(Base):
    __tablename__ = 'quarters'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class DatamapItem(Base):
    __tablename__ = 'datamap_items'

    id = Column(Integer, primary_key=True)
    key = Column(String)
    bicc_sheet = Column(String)
    bicc_cellref = Column(String)
    gmpp_sheet = Column(String)
    gmpp_cellref = Column(String)
    bicc_ver_form = Column(String)

    def __repr__(self):
        return "<DatamapItem('{}')>"/format(key[0:15])


Base.metadata.create_all(engine)
