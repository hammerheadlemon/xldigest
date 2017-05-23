from xldigest.database.base_queries import check_db_table_duplicates, link_declared_p_name_with_project
from xldigest.widgets.master import DatamapView, DatamapCellItem
from ..database.models import Portfolio, Project, Series, SeriesItem

from collections import deque


def test_alphabet_order(session):
    # let's create some cells!
    # These are heading cells, added to a queue in a random order. Perhaps they
    # are in the order of a project_id, for instance, which does not necessarily
    # correlate with their project name, hence "P1", "P2", etc in their title
    # references here.
    heading1 = DatamapCellItem("B - P1-DCI1 Header", 2, 0, True, session)
    heading2 = DatamapCellItem("D - P2-DCI2 Header", 3, 0, True, session)
    heading3 = DatamapCellItem("A - P3-DCI3 Header", 4, 0, True, session)
    heading4 = DatamapCellItem("C - P4-DCI4 Header", 5, 0, True, session)

    # these are initial data cells for Project 1 - which have been added to the queue but
    # have not been sorted, therefore their y values are all 0 in
    # the unsorted state. However, their initial x value corresponds
    # to the datamapitem order.
    # Project 1
    p1_d1 = DatamapCellItem("P1_DCI1 Data", 2, 0, session)
    p1_d2 = DatamapCellItem("P1_DCI2 Data", 3, 0, session)
    p1_d3 = DatamapCellItem("P1_DCI3 Data", 4, 0, session)
    p1_d4 = DatamapCellItem("P1_DCI4 Data", 5, 0, session)

    # Project 2
    p2_d1 = DatamapCellItem("P2_DCI1 Data", 2, 0, session)
    p2_d2 = DatamapCellItem("P2_DCI2 Data", 3, 0, session)
    p2_d3 = DatamapCellItem("P2_DCI3 Data", 4, 0, session)
    p2_d4 = DatamapCellItem("P2_DCI4 Data", 5, 0, session)

    # Project 3
    p3_d1 = DatamapCellItem("P3_DCI1 Data", 2, 0, session)
    p3_d2 = DatamapCellItem("P3_DCI2 Data", 3, 0, session)
    p3_d3 = DatamapCellItem("P3_DCI3 Data", 4, 0, session)
    p3_d4 = DatamapCellItem("P3_DCI4 Data", 5, 0, session)

    # Project 3
    p4_d1 = DatamapCellItem("P4_DCI1 Data", 2, 0, session)
    p4_d2 = DatamapCellItem("P4_DCI2 Data", 3, 0, session)
    p4_d3 = DatamapCellItem("P4_DCI3 Data", 4, 0, session)
    p4_d4 = DatamapCellItem("P4_DCI4 Data", 5, 0, session)

    # so, through an external function not tested in this case, these
    # dmcis are added to a collection or queue of some sort. This models the
    # 'holding' area of the DatamapView object, where DatamapCellItem objects
    # are created on the basis of a project, seriesitem and the corresponding
    # returnitem values that are pulled from the database as a result. Each
    # returnitem produces a DatamapCellItem. An additional DatamapCellItem object
    # whose header flag is set to True is also created by this external function
    # to sit at the top of the column (or in the headers list in the QTableVIew.
    # This is also modelled here.

    queue = deque([
        heading1, heading2, heading3, heading4, p1_d1, p1_d2, p1_d3, p1_d4,
        p2_d1, p2_d2, p2_d3, p2_d4, p3_d1, p3_d2, p3_d3, p3_d4, p4_d1, p4_d2,
        p4_d3, p4_d4
    ])
