# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool


class SQLAlchemyUtil(object):
    """
    # 使用示例：
    from algo_database_utils.mysql_util import SQLAlchemyUtil

    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'test_db',
        'username': 'root',
        'password': '123456',
        "charset": "utf8mb4",  # 字符类型
        "pool_size": 10,  # 连接池size
        "max_overflow": 10,  # 超过连接池最大连接数
        "pool_recycle": 60,  # 60s回收一次连接
        "autoflush": False,  # 自动刷新(事务过程中刷新数据)
        "autocommit": False,  # 自动提交事务
        "connect_timeout": 10,  # 连接超时10s
        "echo": False  # 打印sql语句
    }

    db = SQLAlchemyUtil(config)

    # 示例：根据用户id查询用户：
    # 1.使用原生sql：
    sql = "select * from user_table where id=:user_id"
    args = {"user_id": "123456"}
    res = db.session.execute(sql, args).first()

    # 2.使用orm：(先建好UserDao)
    user_id = "123456"
    res = db.session.query(UserDao).filter(UserDao.id == user_id).first()

    # 3.使用封装好的方法：
    kwargs = {"user_id": "132456"}
    res = db.query_one(UserDao, **kwargs)
    """

    def __init__(self, config):

        self._config = config
        self.session = self._get_session()

    @property
    def _get_session(self):
        if not hasattr(self, "conn"):
            self.session = self._get_mysql_conn()
        return self.session

    def _get_mysql_conn(self):
        mysql_env = "mysql+pymysql://{username}:{password}@{host}:{port}/{dbname}?charset={charset}".format(
            username=self._config.get("username"),
            password=self._config.get("password"),
            host=self._config.get("host"),
            port=self._config.get("port"),
            dbname=self._config.get("database"),
            charset=self._config.get("charset"),
        )
        engine = create_engine(
            mysql_env,
            echo=self._config.get('echo'),
            poolclass=QueuePool,
            pool_timeout=self._config.get("connect_timeout"),
            pool_size=self._config.get("pool_size"),
            max_overflow=self._config.get("max_overflow"),
            pool_recycle=self._config.get("pool_recycle"),
            isolation_level="READ COMMITTED",
        )

        Session = scoped_session(
            sessionmaker(
                bind=engine,
                autoflush=self._config.get("autoflush", False),
                autocommit=self._config.get("autocommit", False),
            )
        )
        return Session

    def init_dao(self, dao, **kwargs):
        obj = dao()
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    def add(self, dao, **kwargs):
        """
        :param :
        :return:
        """
        obj = self.init_dao(dao, **kwargs)
        self.session.add(obj)
        try:
            self.session.flush()
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            if hasattr(e, 'orig'):
                if e.orig.args[0] == 1062:
                    assert False, ("索引冲突", 4001)
            raise e
        else:
            return obj

    def add_without_commit(self, dao, **kwargs):
        """
        :param :
        :return:
        """
        obj = self.init_dao(dao, **kwargs)
        self.session.add(obj)
        try:
            self.session.flush()
        except Exception as e:
            self.session.rollback()
            if hasattr(e, 'orig'):
                if e.orig.args[0] == 1062:
                    assert False, ("索引冲突", 4001)
            raise e
        else:
            return obj

    def query_all(self, dao, **kwargs):
        query = self.session.query(dao)
        for key, val in kwargs.items():
            if hasattr(dao, key):
                query = query.filter(getattr(dao, key) == val)
        return query

    def query_one(self, dao, **kwargs):
        return self.query_all(dao, **kwargs).first()

    def get_all_obj_by_es_id(self, dao, es_id):
        return self.session.query(dao).filter(dao.es_id == es_id).all()

    def get_obj_by_es_id(self, dao, es_id):
        return self.session.query(dao).filter(dao.es_id == es_id).first()

    def real_delete_obj_by_es_id(self, dao, es_id):
        obj = self.get_obj_by_es_id(dao, es_id)
        if not obj:
            return False, 'obj is not exist', ''
        result = self.session.delete(obj)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        return result

    def real_delete_objs_by_kwargs_without_commit(self, dao, **kwargs):
        query = self.session.query(dao)
        for key, val in kwargs.items():
            if hasattr(dao, key):
                query = query.filter(getattr(dao, key) == val)
        query.delete(synchronize_session=False)

    def update_obj_by_es_id(self, dao, es_id, **kwargs):
        obj = self.get_obj_by_es_id(dao, es_id)
        if not obj:
            return False, 'obj is not exist', ''
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise
        return obj

    def update_obj_by_es_id_without_commit(self, dao, es_id, **kwargs):
        obj = self.get_obj_by_es_id(dao, es_id)
        if not obj:
            return False, 'obj is not exist', ''
        for k, v in kwargs.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj
