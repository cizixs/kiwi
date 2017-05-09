from .fields import Field


class ModelMetaClass(type):
    """Metaclass for Model"""
    def __new__(mcs, name, bases, attrs):
        mapping = {key: value for key, value in attrs.items()
                   if isinstance(value, Field)}
        # remove the origin fields
        for key in mapping.keys():
            del attrs[key]

        real_attrs = {
            '__db_fields__': mapping,
            '__db_tablename__': attrs.get('__tablename__', str(name).lower()),
        }
        real_attrs.update(attrs)

        cls_obj = type.__new__(mcs, name, bases, real_attrs)
        return cls_obj


class Model(object):
    """Base class for all models."""
    __metaclass__ = ModelMetaClass

    @classmethod
    def create(cls, **kwargs):
        """Add a record in table."""
        table_name = cls.__db_tablename__
        fields, args = [], []

        for field, _ in cls.__db_fields__.items():
            fields.append(field)
            args.append(kwargs[field])

        sql = 'INSERT into %s (%s) VALUES (%s);' % (
            table_name, ', '.join(fields), ', '.join(['%s'] * len(fields))
        )
        Database.execute(sql, tuple(args))

    @classmethod
    def get(cls, **kwargs):
        """Return one record from database."""
        table_name = cls.__db_tablename__
        filters = 'where ' + ' and '.join([key + '=%s' for key in kwargs]) \
            if kwargs else ''

        sql = 'SELECT %s from %s %s LIMIT 1' % (
            ' ,'.join(cls.__db_fields__.keys()), table_name, filters)
        result = Database.execute(sql, tuple(kwargs.values()))
        record = result.fetchone()
        instance = cls()
        for index, field in enumerate(record):
            setattr(instance, cls.__db_fields__.keys()[index], field)
        return instance

    def save(self):
        """Save current instance to database."""
        self.__class__.create(**self.__dict__)

    def delete(self):
        """Delete current instance from database."""
        table_name = self.__db_tablename__
        fields, args = [], []
        for field, _ in self.__db_fields__.items():
            fields.append(field)
            args.append(self.__dict__[field])

        filters = ' WHERE ' + ' and '.join([key + '=%s' for key in fields]) \
            if fields else ''

        sql = 'DELETE FROM %s %s' % (table_name, filters)
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
