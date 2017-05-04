from xldigest.database.populate import (
    import_datamap_csv, merge_gmpp_datamap, populate_portfolio_table,
    populate_series_table, populate_projects_table_from_gui, populate_series_item_table)


def main_startup(datamap_csv, gmpp_csv, portfolio_name, series_name,
                 projects, series_items):
        import_datamap_csv(datamap_csv[0])
        merge_gmpp_datamap(gmpp_csv[0])
        populate_portfolio_table(portfolio_name)
        populate_series_table(series_name)
        populate_projects_table_from_gui(1, projects)
        populate_series_item_table(series_items)
