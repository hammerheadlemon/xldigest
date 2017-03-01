from xldigest.widgets.datamap import pull_all_data_from_db


def test_datamap_data_from_sqlalchemy():
    data = pull_all_data_from_db()
#   print(data)
    assert data[0][0] == 1
