from sqlalchemy.sql.expression import func


def get_select_random_record_query(table):
    return table.select().order_by(func.random()).limit(1)
