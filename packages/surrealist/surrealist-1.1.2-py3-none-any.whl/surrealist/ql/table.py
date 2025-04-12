from typing import Callable, Dict, List, Optional, Tuple, Union

from surrealist.connections import Connection
from surrealist.errors import WrongCallError
from surrealist.ql.statements.create import Create
from surrealist.ql.statements.delete import Delete
from surrealist.ql.statements.insert import Insert
from surrealist.ql.statements.live import Live
from surrealist.ql.statements.rebuild_index import RebuildIndex
from surrealist.ql.statements.remove import Remove
from surrealist.ql.statements.select import Select
from surrealist.ql.statements.show import Show
from surrealist.ql.statements.statement import Statement
from surrealist.ql.statements.update import Update
from surrealist.ql.statements.upsert import Upsert
from surrealist.result import SurrealResult
from surrealist.utils import StrOrRecord


class Table:
    """
    Represents a table of the database including not (yet) existing one.
    Can use only statements of the table level (CRUD).
    If you need a raw query, DEFINE or transactions - you need database level

    Please refer to: https://github.com/kotolex/surrealist?tab=readme-ov-file#methods-and-query-language

    SurrealQL: https://docs.surrealdb.com/docs/surrealql/overview

    Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/
    """

    def __init__(self, name: str, connection: Connection):
        self._connection = connection
        self._name = name

    @property
    def name(self) -> str:
        """
        Return name of the table

        :return: table name
        """
        return self._name

    def info(self) -> Dict:
        """
        Returns full table info

        :return: Result of the request
        """
        return self._connection.table_info(self._name).result

    def count(self) -> int:
        """
        Returns the number of records at current table, returns 0 if table is empty or not exist

        :return: number of records
        """
        return self._connection.count(self._name).result

    def select(self, *args, alias: Optional[List[Tuple[str, Union[str, Statement]]]] = None,
               value: Optional[str] = None) -> Select:
        """
        Represents SELECT statement and its abilities as refer here:
        https://docs.surrealdb.com/docs/surrealql/statements/select

        Example: table.select('id', 'name').run()

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_select_examples.py

        :param alias: list of pairs of names and values for AS statement
        :param value: on exists an add VALUE statement
        :param args: which fields to select, if no fields or "*" - selects all
        :return: Select object
        """
        return Select(self._connection, self.name, *args, alias=alias, value=value)

    def create(self, record_id: Optional[Union[StrOrRecord, int]] = None) -> Create:
        """
        Represent CREATE a statement and its abilities as refer here:
        https://docs.surrealdb.com/docs/surrealql/statements/create

        Example:
        db.table("article").create("first").content({"author": "author:john", "title": uid}).run()

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_create_examples.py

        :param record_id: optional, if specified transform to 'table_name:record_id'
        :return: Create object
        """
        return Create(self._connection, self.name, record_id)

    def show_changes(self, since: Optional[str] = None) -> Show:
        """
        Represents SHOW CHANGES statement for the Change Feed

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/show

        Refer to: https://github.com/kotolex/surrealist?tab=readme-ov-file#change-feeds

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_show_examples.py

        :return: Show object
        """
        return Show(self._connection, self._name, since=since)

    def delete(self, record_id: Optional[StrOrRecord] = None) -> Delete:
        """
        Represent DELETE statement

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/delete

        Example:
        db.table("author").delete("john").return_none().run()

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_delete_examples.py

        :param record_id: optional, if specified transform to 'table_name:record_id'
        :return: Delete object
        """
        return Delete(self._connection, self._name, record_id)

    def delete_all(self) -> SurrealResult:
        """
        Deletes all records at the database and returns nothing.
        If you need to get back all data ot id's - use query builder or raw_query on database level.
        This action does not remove table, just records in it.
        If you need to delete table itself - use **drop** method

        :return: result with [] as a response
        """
        return Delete(self._connection, self._name).return_none().run()

    def drop(self) -> SurrealResult:
        """
        Fully removes table with all records in it if table exists.
        This method never returns error, cause use IF EXISTS query

        If you need to just delete all records and keep table - use **delete_all** method

        :return: result of response
        """
        return Remove(self._connection, self._name).if_exists().run()

    def remove(self) -> SurrealResult:
        """
        Fully removes table with all records in it if table exists.
        This method never returns error, cause use IF EXISTS query

        If you need to just delete all records and keep table - use **delete_all** method

        :return: result of response
        """
        return self.drop()

    def live(self, callback: Callable[[Dict], None], select: Optional[str] = None, use_diff: bool = False) -> Live:
        """
        Represents LIVE statement for a live query

        Example:
        db.person.live(func).alias("first_name", "NAME").where("age > 22").run()

        Refer to: https://surrealdb.com/docs/surrealdb/surrealql/statements/live

        Refer to: https://github.com/kotolex/surrealist?tab=readme-ov-file#live-query

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_live_examples.py

        :param callback: function to call on live query event
        :param select: raw query to insert between LIVE SELECT and FROM {table}, so the result will be
        LIVE SELECT {select} FROM {table_name}.
        If it is provided, other parameters (diff, alias, value) will be ignored
        :param use_diff: return result in DIFF format
        :return: Live object
        """
        return Live(self._connection, self._name, callback, select, use_diff)

    def kill(self, live_id: str) -> SurrealResult:
        """
        Represents a KILL statement, for killing a live query

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/kill

        :param live_id: id of the query
        :return: result
        """
        return self._connection.kill(live_id)

    def insert(self, *args) -> Insert:
        """
        Represent INSERT INTO statement.
        Arguments here are:
          - the only one which is Dict or List or Statement

          OR

          - multiple arguments where first are names and other - values

        Example:
        db.person.insert(("name", "age"), ("Tobie", 33)).run()
        db.person.insert({("name":"Tobie", "age": 33)}).run()

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/insert

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_insert_examples.py

        :param args: args for insert, it can be list of records, one record, one statement or 2 or more tuples of names
        and values
        :return: Insert object
        """
        return Insert(self._connection, self._name, *args)

    def update(self, record_id: Optional[StrOrRecord] = None) -> Update:
        """
        Represent UPDATE object

        Example:
        db.table("user").update("alex").only().merge({"active": True}).run()

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/update

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_update_examples.py

        :param record_id: optional, if specified transform to 'table_name:record_id'
        :return: Update object
        """
        return Update(self._connection, self._name, record_id)

    def upsert(self, record_id: Optional[StrOrRecord] = None) -> Upsert:
        """
        Represent UPSERT object

        Example:
        db.table("user").upsert("alex").only().merge({"active": True}).run()

        Refer to: https://docs.surrealdb.com/docs/surrealql/statements/upsert

        Examples: https://github.com/kotolex/surrealist/blob/master/examples/surreal_ql/ql_upsert_examples.py

        :param record_id: optional, if specified transform to 'table_name:record_id'
        :return: Upsert object
        """
        return Upsert(self._connection, self._name, record_id)

    def rebuild_index(self, index_name: str, if_exists: bool = False) -> RebuildIndex:
        """
        Represents REBUILD INDEX object, used to rebuild resources.

        Example:
        db.table("user").rebuild_index("my_index").run()

        Refer to: https://surrealdb.com/docs/surrealdb/surrealql/statements/rebuild

        :param index_name: name of the index
        :param if_exists: use IF EXISTS statement if True
        :return: RebuildIndex object
        """
        return RebuildIndex(self._connection, index_name=index_name, table_name=self._name, if_exists=if_exists)

    def __repr__(self):
        return f"Table(name={self._name}, connection with {self._connection.transport().value} transport)"

    def __call__(self, *args, **kwargs):
        raise WrongCallError(f"Table object is not callable. \n"
                             f"It looks like you misspelled the method name of Database({self._name})")
