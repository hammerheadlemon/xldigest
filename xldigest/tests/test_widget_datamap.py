from xldigest.widgets.datamap import pull_all_data_from_db
from xldigest.database.models import DatamapItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_datamap_data_from_sqlalchemy():
    data = pull_all_data_from_db()
    engine = create_engine('sqlite:///../db.sqlite')
    Session = sessionmaker(bind=engine)
    session = Session()
    db_items = session.query(DatamapItem).filter_by(bicc_sheet='Summary').all()
    print(db_items)
    assert data[0] == 'test_data'
