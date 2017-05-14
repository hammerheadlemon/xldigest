import os

from ..database.connection import Connection


def test_connection():
    session = Connection.session_for_test('/tmp/db.sqlite')
    from xldigest.database.models import Project
    p = Project(name="Test Project 1", portfolio=1)
    session.add(p)
    session.commit()
    assert os.path.exists('/tmp/db.sqlite')
