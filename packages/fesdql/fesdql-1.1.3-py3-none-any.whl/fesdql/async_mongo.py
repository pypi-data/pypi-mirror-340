#!/usr/bin/env python3
# coding=utf-8

"""
@author: guoyanfeng
@software: PyCharm
@time: 18-12-25 下午3:41
"""

from collections.abc import MutableSequence
from typing import Any, Dict, List, Optional, Tuple, Union

import aelog
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from pymongo.errors import (ConnectionFailure, DuplicateKeyError, InvalidName, PyMongoError)

from ._alchemy import AlchemyMixIn, BaseMongo, BasePagination, SessionMixIn
from .err import HttpError, MongoDuplicateKeyError, MongoError, MongoInvalidNameError
from .query import Query

__all__ = ("AsyncMongo", "AsyncSession", "AsyncPagination")


class AsyncPagination(BasePagination):
    """Internal helper class returned by :meth:`BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.

    """

    def __init__(self, session: 'AsyncSession', query: Query, total: int, items: List[Dict[str, Any]],
                 whereclause: Dict[str, Any]) -> None:
        super().__init__(session, query, total, items, whereclause)

    # noinspection PyProtectedMember
    async def prev(self, ) -> List[Dict[str, Any]]:
        """Returns a :class:`Pagination` object for the previous page."""
        self.page -= 1
        return await self.session._find_many(self.cname, self.whereclause, self.columns, self.per_page,
                                             (self.page - 1) * self.per_page, self.order_by)

    # noinspection PyProtectedMember
    async def next(self, ) -> List[Dict[str, Any]]:
        """Returns a :class:`Pagination` object for the next page."""
        self.page += 1
        return await self.session._find_many(self.cname, self.whereclause, self.columns, self.per_page,
                                             (self.page - 1) * self.per_page, self.order_by)


# noinspection PyProtectedMember
class AsyncSession(SessionMixIn, object):
    """
    query session
    """

    def __init__(self, db: Database, message: Dict[int, Dict[str, str]], msg_zh: str,
                 max_per_page: Optional[int] = None) -> None:
        """
            query session
        Args:
            db: db engine
            message: 消息提示
            msg_zh: 中文提示或者而英文提示
            max_per_page: 每页最大的数量
        """
        self.db: Database = db
        self.message: Dict[int, Dict[str, str]] = message
        self.msg_zh: str = msg_zh
        self.max_per_page: Optional[int] = max_per_page

    async def _insert_one(self, cname: str, document: Union[List[Dict[str, Any]], Dict[str, Any]],
                          insert_one: bool = True) -> Union[Tuple[str, ...], str]:
        """
        插入一个单独的文档
        Args:
            cname:collection name
            document: document obj
            insert_one: insert_one insert_many的过滤条件，默认True
        Returns:
            返回插入的Objectid
        """
        try:
            if insert_one:
                result = await self.db.get_collection(cname).insert_one(document)
            else:
                result = await self.db.get_collection(cname).insert_many(document)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except DuplicateKeyError as e:
            raise MongoDuplicateKeyError("Duplicate key error, {}".format(e))
        except PyMongoError as err:
            aelog.exception("Insert one document failed, {}".format(err))
            raise HttpError(400, message=self.message[100][self.msg_zh], error=err)
        else:
            return str(result.inserted_id) if insert_one else tuple(str(val) for val in result.inserted_ids)

    async def _insert_many(self, cname: str, document: List[Dict[str, Any]]) -> Tuple[str, ...]:
        """
        批量插入文档
        Args:
            cname:collection name
            document: document obj
        Returns:
            返回插入的Objectid列表
        """
        result = await self._insert_one(cname, document, insert_one=False)
        return tuple(result)

    async def _find_one(self, cname: str, whereclause: Dict[str, Any], columns: Optional[Dict[str, bool]] = None,
                        order_by: Optional[List[Tuple[str, int]]] = None) -> Optional[Dict[str, Any]]:
        """
        查询一个单独的document文档
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
            columns: 过滤返回值中字段的过滤条件
            order_by: 根据字段排序
        Returns:
            返回匹配的document或者None
        """
        try:
            find_data = await self.db.get_collection(cname).find_one(whereclause, projection=columns, sort=order_by)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except PyMongoError as err:
            aelog.exception("Find one document failed, {}".format(err))
            raise HttpError(400, message=self.message[103][self.msg_zh], error=err)
        else:
            if find_data and find_data.get("_id") is not None:
                find_data["id"] = str(find_data.pop("_id"))
            return find_data

    async def _find_many(self, cname: str, whereclause: Dict[str, Any], columns: Optional[Dict[str, bool]] = None,
                         skip: int = 0, limit: int = 0, order_by: Optional[List[Tuple[str, int]]] = None
                         ) -> List[Dict[str, Any]]:
        """
        批量查询document文档
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
            columns: 过滤返回值中字段的过滤条件
            skip: 从查询结果中调过指定数量的document
            limit: 限制返回的document条数
            order_by: 排序方式，可以自定多种字段的排序，值为一个列表的键值对， eg:[('field1', pymongo.ASCENDING)]
        Returns:
            返回匹配的document列表
        """
        try:
            find_data: List[Dict[str, Any]] = []
            # find_data = await cursor.to_list(None)
            async for doc in self.db.get_collection(cname).find(
                    whereclause, projection=columns, skip=skip, limit=limit, sort=order_by):
                if doc.get("_id") is not None:
                    doc["id"] = str(doc.pop("_id"))
                find_data.append(doc)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except PyMongoError as err:
            aelog.exception("Find many document failed, {}".format(err))
            raise HttpError(400, message=self.message[104][self.msg_zh], error=err)
        else:
            return find_data

    async def _find_count(self, cname: str, whereclause: Dict[str, Any]) -> int:
        """
        查询document的数量
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
        Returns:
            返回匹配的document数量
        """
        try:
            return await self.db.get_collection(cname).count(whereclause)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except PyMongoError as err:
            aelog.exception("Find many document failed, {}".format(err))
            raise HttpError(400, message=self.message[104][self.msg_zh], error=err)

    async def _update_one(self, cname: str, whereclause: Dict[str, Any], update_data: Dict[str, Any],
                          upsert: bool = False, update_one: bool = True) -> Dict[str, Optional[Union[str, int]]]:
        """
        更新匹配到的一个的document
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
            update_data: 对匹配的document进行更新的document
            upsert: 没有匹配到document的话执行插入操作，默认False
            update_one: update_one or update_many的匹配条件
        Returns:
            返回匹配的数量和修改数量的dict, eg:{"matched_count": 1, "modified_count": 1, "upserted_id":"f"}
        """
        try:
            if update_one:
                result = await self.db.get_collection(cname).update_one(whereclause, update_data, upsert=upsert)
            else:
                result = await self.db.get_collection(cname).update_many(whereclause, update_data, upsert=upsert)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except DuplicateKeyError as e:
            raise MongoDuplicateKeyError("Duplicate key error, {}".format(e))
        except PyMongoError as err:
            aelog.exception("Update document failed, {}".format(err))
            raise HttpError(400, message=self.message[101][self.msg_zh], error=err)
        else:
            return {"matched_count": result.matched_count, "modified_count": result.modified_count,
                    "upserted_id": str(result.upserted_id) if result.upserted_id else None}

    async def _update_many(self, cname: str, whereclause: Dict[str, Any], update_data: Dict[str, Any],
                           upsert: bool = False) -> Dict[str, Optional[Union[str, int]]]:
        """
        更新匹配到的所有的document
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
            update_data: 对匹配的document进行更新的document
            upsert: 没有匹配到document的话执行插入操作，默认False
        Returns:
            返回匹配的数量和修改数量的dict, eg:{"matched_count": 2, "modified_count": 2, "upserted_id":"f"}
        """
        return await self._update_one(cname, whereclause, update_data, upsert, update_one=False)

    async def _delete_one(self, cname: str, whereclause: Dict[str, Any], delete_one: bool = True) -> int:
        """
        删除匹配到的一个的document
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
            delete_one: delete_one delete_many的匹配条件
        Returns:
            返回删除的数量
        """
        try:
            if delete_one:
                result = await self.db.get_collection(cname).delete_one(whereclause)
            else:
                result = await self.db.get_collection(cname).delete_many(whereclause)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except PyMongoError as err:
            aelog.exception("Delete document failed, {}".format(err))
            raise HttpError(400, message=self.message[102][self.msg_zh], error=err)
        else:
            return result.deleted_count

    async def _delete_many(self, cname: str, whereclause: Dict[str, Any]) -> int:
        """
        删除匹配到的所有的document
        Args:
            cname: collection name
            whereclause: 查询document的过滤条件
        Returns:
            返回删除的数量
        """
        return await self._delete_one(cname, whereclause, delete_one=False)

    async def _aggregate(self, cname: str, pipline: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
        """
        根据pipline进行聚合查询
        Args:
            cname: collection name
            pipline: 聚合查询的pipeline,包含一个后者多个聚合命令
        Returns:
            返回聚合后的document
        """
        result: List[Dict[str, Any]] = []
        try:
            async for doc in self.db.get_collection(cname).aggregate(pipline, **kwargs):
                if doc.get("_id") is not None:
                    doc["id"] = doc.pop("_id")
                result.append(doc)
        except InvalidName as e:
            raise MongoInvalidNameError("Invalid collention name {} {}".format(cname, e))
        except PyMongoError as err:
            aelog.exception("Aggregate document failed, {}".format(err))
            raise HttpError(400, message=self.message[105][self.msg_zh], error=err)
        else:
            return result

    # noinspection DuplicatedCode
    async def insert_many(self, query: Query) -> Tuple[str, ...]:
        """
        批量插入文档
        Args:
            query: Query class
                cname:collection name
                document: document obj
        Returns:
            返回插入的转换后的_id列表
        """
        if not isinstance(query._insert_data, list):
            raise MongoError("insert many document failed, document is not a iterable type.")
        document: List[Dict[str, Any]] = query._insert_data
        for document_ in document:
            if not isinstance(document_, dict):
                raise MongoError("insert one document failed, document is not a mapping type.")
            self._update_doc_id(document_)
        return await self._insert_many(query._cname, document)

    async def insert_one(self, query: Query) -> str:
        """
        插入一个单独的文档
        Args:
            query: Query class
                cname:collection name
                document: document obj
        Returns:
            返回插入的转换后的_id
        """
        if not isinstance(query._insert_data, dict):
            raise MongoError("insert one document failed, document is not a mapping type.")
        result = await self._insert_one(query._cname, self._update_doc_id(query._insert_data))
        return str(result)

    async def find_one(self, query: Query) -> Optional[Dict[str, Any]]:
        """
        查询一个单独的document文档
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
                exclude_key: 过滤返回值中字段的过滤条件
        Returns:
            返回匹配的document或者None
        """
        return await self._find_one(query._cname, self._update_query_key(query._whereclause), query._columns,
                                    query._order_by)

    # noinspection DuplicatedCode
    async def find_many(self, query: Query) -> AsyncPagination:
        """
        批量查询document文档,分页数据
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
                exclude_key: 过滤返回值中字段的过滤条件
                per_page: 每页数据的数量
                page: 查询第几页的数据
                sort: 排序方式，可以自定多种字段的排序，值为一个列表的键值对， eg:[('field1', pymongo.ASCENDING)]
        Returns:
            Returns a :class:`AsyncPagination` object.
        """

        query_key = self._update_query_key(query._whereclause)
        items = await self._find_many(query._cname, query_key, query._columns, limit=query._limit_clause,
                                      skip=query._offset_clause, order_by=query._order_by)

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if query._page == 1 and len(items) < query._per_page:
            total = len(items)
        else:
            total = await self.find_count(query)

        return AsyncPagination(self, query, total, items, query_key)

    async def find_all(self, query: Query) -> List[Dict[str, Any]]:
        """
        批量查询document文档
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
                exclude_key: 过滤返回值中字段的过滤条件
                sort: 排序方式，可以自定多种字段的排序，值为一个列表的键值对， eg:[('field1', pymongo.ASCENDING)]
        Returns:
            返回匹配的document列表
        """
        return await self._find_many(query._cname, self._update_query_key(query._whereclause), query._columns,
                                     order_by=query._order_by)

    async def find_count(self, query: Query) -> int:
        """
        查询document的数量
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
        Returns:
            返回匹配的document数量
        """
        return await self._find_count(query._cname, self._update_query_key(query._whereclause))

    async def update_many(self, query: Query) -> Dict[str, Optional[Union[str, int]]]:
        """
        更新匹配到的所有的document
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
                update_data: 对匹配的document进行更新的document
                upsert: 没有匹配到document的话执行插入操作，默认False
        Returns:
            返回匹配的数量和修改数量的dict, eg:{"matched_count": 2, "modified_count": 2, "upserted_id":"f"}
        """
        return await self._update_many(query._cname, self._update_query_key(query._whereclause),
                                       self._update_update_data(query._update_data), upsert=query._upsert)

    async def update_one(self, query: Query) -> Dict[str, Optional[Union[str, int]]]:
        """
        更新匹配到的一个的document
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
                update_data: 对匹配的document进行更新的document
                upsert: 没有匹配到document的话执行插入操作，默认False
        Returns:
            返回匹配的数量和修改数量的dict, eg:{"matched_count": 1, "modified_count": 1, "upserted_id":"f"}
        """
        return await self._update_one(query._cname, self._update_query_key(query._whereclause),
                                      self._update_update_data(query._update_data), upsert=query._upsert)

    async def delete_many(self, query: Query) -> int:
        """
        删除匹配到的所有的document
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
        Returns:
            返回删除的数量
        """
        return await self._delete_many(query._cname, self._update_query_key(query._whereclause))

    async def delete_one(self, query: Query) -> int:
        """
        删除匹配到的一个的document
        Args:
            query: Query class
                cname: collection name
                query_key: 查询document的过滤条件
        Returns:
            返回删除的数量
        """
        return await self._delete_one(query._cname, self._update_query_key(query._whereclause))

    # noinspection DuplicatedCode
    async def aggregate(self, query: Query, **kwargs) -> List[Dict[str, Any]]:
        """
        根据pipline进行聚合查询
        Args:
            query: Query class
                cname: collection name
                pipline: 聚合查询的pipeline,包含一个后者多个聚合命令
                per_page: 每页数据的数量
                page: 查询第几页的数据
        Returns:
            返回聚合后的document
        """
        kwargs.setdefault("allowDiskUse", True)
        pipline: List[Dict[str, Any]] = query._pipline
        if not isinstance(pipline, MutableSequence):
            raise MongoError("Aggregate query failed, pipline arg is not a iterable type.")
        if query._limit_clause and query._per_page:
            pipline.extend([{'$skip': query._limit_clause}, {'$limit': query._per_page}])
        return await self._aggregate(query._cname, pipline, **kwargs)


class AsyncMongo(AlchemyMixIn, BaseMongo):
    """
    mongo 非阻塞工具类
    """

    def __init__(self, app=None, *, username: str = "", passwd: str = "", host: str = "127.0.0.1",
                 port: int = 27017, dbname: str = "", pool_size: int = 25,
                 fesdql_binds: Optional[Dict[str, Dict]] = None, **kwargs) -> None:
        """
        mongo 非阻塞工具类
        Args:
            app: app应用
            username: mongo user
            passwd: mongo password
            host:mongo host
            port:mongo port
            dbname: database name
            pool_size: mongo pool size
            fesdql_binds: binds config, eg:{"first":{"fesdql_mongo_host":"127.0.0.1",
                                        "fesdql_mongo_port":3306,
                                        "fesdql_mongo_username":"root",
                                        "fesdql_mongo_passwd":"",
                                        "fesdql_mongo_dbname":"dbname",
                                        "fesdql_mongo_pool_size":10}}

        """
        super().__init__(app, username=username, passwd=passwd, host=host, port=port, dbname=dbname,
                         pool_size=pool_size, fesdql_binds=fesdql_binds, **kwargs)

    def init_app(self, app) -> None:
        """
        mongo 实例初始化
        Args:
            app: app应用
        Returns:

        """
        self._verify_sanic_app(app)  # 校验APP类型是否正确
        super().init_app(app)

        # noinspection PyUnusedLocal
        @app.listener('before_server_start')
        async def open_connection(app_, loop):
            """

            Args:

            Returns:

            """
            self.bind_pool[None] = self._create_engine(
                host=self.host, port=self.port, username=self.username, passwd=self.passwd,
                pool_size=self.pool_size, dbname=self.dbname)

        # noinspection PyUnusedLocal
        @app.listener('after_server_stop')
        async def close_connection(app_, loop):
            """

            Args:

            Returns:

            """
            for _, engine in self.engine_pool.items():
                if engine:
                    engine.close()

    def _create_engine(self, host: str, port: int, username: str, passwd: str, pool_size: int,
                       dbname: str) -> Database:
        # host和port确定了mongodb实例,username确定了权限,其他的无关紧要
        engine_name = f"{host}_{port}_{username}"
        try:
            if engine_name not in self.engine_pool:
                self.engine_pool[engine_name] = AsyncIOMotorClient(
                    host, port, username=username, password=passwd, maxPoolSize=pool_size)
            db = self.engine_pool[engine_name].get_database(name=dbname)
        except ConnectionFailure as e:
            aelog.exception("Mongo connection failed host={} port={} error:{}".format(host, port, e))
            raise MongoError("Mongo connection failed host={} port={} error:{}".format(host, port, e))
        except InvalidName as e:
            aelog.exception("Invalid mongo db name {} {}".format(dbname, e))
            raise MongoInvalidNameError("Invalid mongo db name {} {}".format(dbname, e))
        except PyMongoError as err:
            aelog.exception("Mongo DB init failed! error: {}".format(err))
            raise MongoError("Mongo DB init failed!") from err
        else:
            return db

    @property
    def query(self, ) -> Query:
        """

        Args:

        Returns:

        """
        return Query(self.max_per_page)

    @property
    def session(self, ) -> AsyncSession:
        """
        session default bind
        Args:

        Returns:

        """
        if None not in self.bind_pool:
            raise ValueError("Default bind is not exist.")
        if None not in self.session_pool:
            self.session_pool[None] = AsyncSession(self.bind_pool[None], self.message, self.msg_zh)
        return self.session_pool[None]

    def gen_session(self, bind: str) -> AsyncSession:
        """
        session bind
        Args:
            bind: engine pool one of connection
        Returns:

        """
        self._create_pooldb(bind)
        if bind not in self.session_pool:
            self.session_pool[bind] = AsyncSession(self.bind_pool[bind], self.message, self.msg_zh)
        return self.session_pool[bind]
