import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import xldigest.database.models as models

#engine = create_engine("sqlite:///" + ':memory:')
engine = create_engine("sqlite:///" + '/tmp/new-test.sqlite')
Session = sessionmaker(bind=engine)

models.create_tables(engine)


@pytest.fixture(scope='module')
def session() -> Session:
    session = Session()

    portfolio = models.Portfolio(name="Major Portfolio")
    session.add(portfolio)

    series = models.Series(name="Financial Quarters")
    session.add(series)

    series_items = [models.SeriesItem(name=f"Q{x} 20{y}/{y + 1}",
                                      series=1,
                                      start_date=None,
                                      end_date=None)
                    for x in range(1, 5)
                    for y in range(16, 21)
                    ]
    session.add_all(series_items)

    projects = [models.Project(name=f"Project {x}")
                for x in range(1, 10)]
    session.add_all(projects)

    datamap_items = [models.DatamapItem(
        key=f"Datamap Key {x}",
        bicc_sheet="Summary",
        bicc_cellref=f"B{x}",
        gmpp_sheet=f"GMPP Sheet",
        gmpp_cellref=f"G{x}",
        bicc_ver_form="")
        for x in range(1, 101)]
    session.add_all(datamap_items)

    return_items = []
    for p in range(1, 10):
        return_items.append([models.ReturnItem(
            project_id=p,
            series_item_id=y,
            datamap_item_id=x,
            value=f"Return Value {x}")
            for y in range(1, 21)
            for x in range(1, 101)])

    for r in return_items:
        session.add_all(r)

    session.commit()
    yield session
    session.close()
