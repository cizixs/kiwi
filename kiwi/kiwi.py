from .fields import Field


class ModelMetaClass(type):
    """Metaclass for Model"""
    def __new__(cls, name, bases, attrs):
        mapping = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                mapping[key] = value

        # remove the origin fields
        for key in mapping.keys():
            del attrs[key]

        table_name = attrs.get('__tablename__', str(name).lower())

        real_attrs = {
            '__db_fields__': mapping,
            '__db_tablename__': table_name,
        }
        real_attrs.update(attrs)

        cls_obj = type.__new__(cls, name, bases, real_attrs)
        return cls_obj


class Model(object):
    __metaclass__ = ModelMetaClass

    @classmethod
    def create(cls, **kwargs):
        table_name = cls.__db_tablename__
        fields = []
        args = []

        for field, _ in cls.__db_fields__.items():
            fields.append(field)
            args.append(kwargs[field])

        sql = 'INSERT into %s (%s) VALUES (%s);' % (
            table_name, ', '.join(fields), ', '.join(['%s'] * len(fields))
        )

        Database.execute(sql, tuple(args))


class Database(object):
    db_conn = None
    auto_commit = True

    @classmethod
    def connect(cls, **kwargs):
        import MySQLdb
        cls.db_conn = MySQLdb.connect(
            host=kwargs.get('host', 'localhost'),
            port=int(kwargs.get('port', 3306)),
            user=kwargs.get('user', 'root'),
            passwd=kwargs.get('password', ''),
            db=kwargs.get('database', 'test'),
            charset=kwargs.get('charset', 'utf8'),
        )
        cls.db_conn.autocommit(cls.auto_commit)

    @classmethod
    def get_conn(cls):
        if cls.db_conn:
            return cls.db_conn
        raise RuntimeError("Database is not connected")

    @classmethod
    def execute(cls, *args):
        cursor = cls.get_conn().cursor()
        cursor.execute(*args)
        return cursor

    def __del__(self):
        if self.db_conn and self.db_conn.open:
            self.db_conn.close()
