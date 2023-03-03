import petl


def group_by_columns(path, columns):
    """
    This function cuts only specified columns from petl table and then groups data rows by them.
    """
    table = petl.fromcsv(path)
    table2 = petl.cut(table, *columns)
    headers = petl.fieldnames(table2)

    return petl.aggregate(table, key=headers, aggregation=len, field="Count")


def get_data(path):
    """
    This function reads rows of data from petl table.
    """

    table = petl.fromcsv(path)
    return petl.data(table)


def get_headers(path, columns=None):
    """
    This function headers of petl table. If there are no columns specified it returns all of them.
    """
    table = petl.fromcsv(path)
    return petl.fieldnames(petl.cut(table, *columns)) if columns else petl.fieldnames(table)

