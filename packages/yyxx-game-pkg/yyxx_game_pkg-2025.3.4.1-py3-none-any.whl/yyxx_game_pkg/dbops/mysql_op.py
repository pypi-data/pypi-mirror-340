# -*- coding: utf-8 -*-
"""
@File: mysql_op.py
@Author: ltw
@Time: 2023/4/4
"""
import re
import pandas as pd
from yyxx_game_pkg.dbops.base import DatabaseOperation
from yyxx_game_pkg.utils import xListStr
from sqlalchemy.engine import Connection as AlchemyConnection
from yyxx_game_pkg.statistic.log import debug_log


class MysqlOperation(DatabaseOperation):
    """
    Mysql数据库操作
    """

    @staticmethod
    def check_sql(sql, conn=None, params=None):
        """
        检查sql表述是否正确
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        if sql and isinstance(sql, str):
            if "%" in sql and not params:
                before_sql = sql
                if isinstance(conn, AlchemyConnection):
                    # 将单个%替换成%%
                    sql = re.sub(r"(?<!%)(%)(?!%)", r"%\1", sql)
                else:
                    # 将%%替换成%
                    sql = re.sub(r"(?<!%)(%%)(?!%)", r"%", sql)
                if sql != before_sql:
                    debug_log(f"[MysqlOperation][check_sql] 前=>{before_sql}")
                    debug_log(f"[MysqlOperation][check_sql] 后=>{sql}")
        return sql

    def execute(self, sql, conn, params=None):
        """
        执行sql返回处理结果
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        with conn:
            if isinstance(conn, AlchemyConnection):
                if params is None:
                    conn.execute(sql)
                else:
                    conn.execute(sql, params)
            else:
                with conn.cursor() as cursor:
                    if params is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, params)
                    conn.commit()

    def get_one(self, sql, conn, params=None):
        """
        查询一条数据, 返回元组结构
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        with conn:
            if isinstance(conn, AlchemyConnection):
                if params is None:
                    return conn.execute(sql).fetchone()
                else:
                    return conn.execute(sql, params).fetchone()
            else:
                with conn.cursor() as cursor:
                    if params is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, params)
                    return cursor.fetchone()

    def get_all(self, sql, conn, params=None):
        """
        查询多条数据，返回list(元组) 结构
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        with conn:
            if isinstance(conn, AlchemyConnection):
                if params is None:
                    return conn.execute(sql).fetchall()
                else:
                    return conn.execute(sql, params).fetchall()
            else:
                with conn.cursor() as cursor:
                    if params is None:
                        cursor.execute(sql)
                    else:
                        cursor.execute(sql, params)
                    return cursor.fetchall()

    def get_one_df(self, *args, **kwargs):
        """
        获取单次数据
        :param args:
        :param kwargs:
        :return:
        """

    def get_all_df(self, sql, connection):
        """
        获取所有数据 dataframe
        :param sql:
        :param connection:
        :return:
        """
        sql = self.check_sql(sql, connection)
        return pd.read_sql(sql, connection)

    def insert(self, conn, save_table="", results=(), insert_sql=""):
        """
        :param conn:
        :param save_table:
        :param results:
        :param insert_sql:
        :return:
        """
        if not results:
            return

        def get_field_str(_data):
            """
            根据数据长度生成{data_value}
            :param _data:
            :return:
            """
            _size = len(_data[0])
            _list = []
            for _ in range(_size):
                _list.append("%s")
            _str = ",".join(_list)
            return _str

        def get_table_desc(_table_name, _data_list, _cs):
            """
            :param _table_name:
            :param _data_list:
            :return:
            """
            sql = f"describe {_table_name}"
            if isinstance(_cs, AlchemyConnection):
                _desc = _cs.execute(sql).fetchall()
            else:
                _cs.execute(sql)
                _desc = _cs.fetchall()
            _column = []
            for _data in _desc:
                if _data[0] in ("id", "create_time"):  # 自增id和默认插入时间过滤
                    continue
                _column.append(_data[0])
            _size = len(_data_list[0])
            table_column = _column[:_size]
            return ",".join(table_column)

        insert_sql_template = "INSERT INTO {save_table} ({column_value}) VALUES({data_value})"
        results = xListStr.split_list(results)
        with conn:
            if isinstance(conn, AlchemyConnection):
                for result in results:
                    if not result:
                        continue
                    if not insert_sql:
                        field_str = get_field_str(result)
                        column_value = get_table_desc(save_table, result, conn)
                        insert_sql = insert_sql_template.format(
                            save_table=save_table, column_value=column_value, data_value=field_str
                        )
                    conn.execute(insert_sql, result)
            else:
                with conn.cursor() as cursor:
                    for result in results:
                        if not result:
                            continue
                        if not insert_sql:
                            field_str = get_field_str(result)
                            column_value = get_table_desc(save_table, result, cursor)
                            insert_sql = insert_sql_template.format(
                                save_table=save_table, column_value=column_value, data_value=field_str
                            )
                        cursor.executemany(insert_sql, result)
                        conn.commit()
