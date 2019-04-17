import mysql.connector


def create_conn(**kw):
    """
    创建数据库连接并返回
    """
    bms = mysql.connector.connect(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw.get('port', "root"),    # 数据库用户名
        passwd=kw.get('password', "xxm19981028"),   # 数据库密码
        database=kw.get('database', 'bms'),
    )
    return bms


def select(sql, args, size=None):
    """
    执行 select 语句, size 为返回的查询到的元素的数量
    """
    print("当前执行的sql语句:", sql, args)
    conn = create_conn()
    cur = conn.cursor()

    try:
        # SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换。
        cur.execute(sql.replace('?', '%s'), args or ())
        if size:
            rs = cur.fetchmany(size)
        else:
            rs = cur.fetchall()
    except:
        print("QUERY Error: unable to fecth data")

    cur.close()
    conn.close()
    print('rows returned: {}'.format(len(rs)))
    return rs


def execute(sql, args):
    """
    执行INSERT、UPDATE、DELETE语句
    """
    print("当前执行的sql语句:", sql, args)
    conn = create_conn()
    cur = conn.cursor()

    try:
        # 执行sql语句
        cur.execute(sql.replace('?', '%s'), args)
        affected = cur.rowcount
        # 提交到数据库执行, 一定要提交
        conn.commit()
    except:
        # 出现错误就回滚
        conn.rollback()
        print("SQL Execute ERROR")

    cur.close()
    conn.close()
    return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)

# 缺省值可以作为函数对象传入，在调用save()时自动计算

class Field(object):
    """
    Field 类保存数据库表的字段名和字段类型
    """

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<{}, {}:{}>'.format(self.__class__.__name__, self.column_type, self.name)


class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class BooleanField(Field):

    def __init__(self, name=None, default=False):
        super().__init__(name, 'boolean', False, default)


class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0, ddl='numeric(10,2)'):
        super().__init__(name, ddl, primary_key, default)


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        # 默认表名为类名
        tableName = attrs.get('__table__', None) or name
        print('found model: {} (table: {})'.format(name, tableName))

        # object 属性与列的关系映射
        mappings = dict()
        # 除主键外的其他所有字段
        fields = []
        # 主键
        primaryKey = None

        # 遍历类属性, 仅将 Field 类中定义的属性保存起来
        for k, v in attrs.items():
            if isinstance(v, Field):        # 判读当前的字段类型是否是在Field子类中已定义的
                print('  found mapping: {} ==> {}'.format(k, v))
                # 将类属性和列的映射关系保存到字典
                mappings[k] = v
                if v.primary_key:
                    # find primaryKey
                    if primaryKey:
                        raise SyntaxError(
                            'ERROR:  Duplicate primary key for field: {}'.format(k))
                    primaryKey = k
                else:
                    fields.append(k)

        if not primaryKey:
            raise SyntaxError('Primary key not found.')

        # 去除掉 attr (类属性)中有的，但是 mappings 中也有的属性
        # 避免属性覆盖, 保证只有在实例中可以访问这些类
        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda f: '%s' % f, fields))
        attrs['__mappings__'] = mappings  # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select {}, {} from {}'.format(
            primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into {} ({}, {}) values ({})'.format(
            tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update {} set {} where {}=?'.format(tableName, ', '.join(
            map(lambda f: '%s=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from {} where {}=?'.format(
            tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)    # 创建一个对象, 这里是类对象



class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                print('using default value for {}: {}'.format(key, str(value)))
                setattr(self, key, value)
        return value

    def __getattr__(self, key):
        """获得model的某个属性值"""
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'Model' object has no attribute '{}'".format(key))

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        根据参数 new 一个对象，注意同时会存入数据库中
        """
        # 获得该model的所有字段
        fields = []
        fields.append(cls.__primary_key__)
        fields.append(cls.__fields__)

        if form is None:
            form = {}
        # 新建一个空对象
        m = cls()

        # 根据form设置空对象的属性值
        for f in fields:
            if f in form:
                setattr(m, f, form[f])

        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError

        m.save()
        return m

    @classmethod
    def _new_with_tuple(cls, tuple):
        """
        根据sql查询到的tuple数据，组装成字典
        返回一个对象
        """
        d = {}
        d[cls.__primary_key__] = tuple[0]
        for idx, k in enumerate(cls.__fields__):
            d[k] = tuple[idx+1]
        m = cls(**d)
        return m

    @classmethod
    def _find(cls, size=None, **kwargs):
        """
        find objects by where clause.
        """
        sql = [cls.__select__]
        where = ''
        args = []
        for id, k in enumerate(kwargs):
            if id == 0:
                where += k + '=' + '?'
            else:
                where += ',' + k + '=' + '?'
            args.append(kwargs[k])
        if where != '':
            sql.append('where')
            sql.append(where)
        rs = select(' '.join(sql), args, size=size)

        return [cls._new_with_tuple(r) for r in rs]

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find(cls, pk):
        ' find object by primary key. '
        rs = select('%s where %s=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls._new_with_tuple(rs[0])

    @classmethod
    def find_one(cls, **kwargs):
        """
        未找到满足条件的记录则返回None
        """
        res = cls._find(size=1, **kwargs)
        if res == []:
            return None
        else:
            return res[0]

    def save(self):
        """
        创建了一个新对象后, 可调用该函数将新对象作为记录写入数据库
        如果使用new 方法, 无需调用该函数
        如果对象已经写入数据库, 仅仅是修改对象的属性值, 应该调用update()函数
        """
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = execute(self.__insert__, args)
        if rows != 1:
            print('failed to insert record: affected rows: {}'.format(rows))

    def update(self):
        """
        修改了对象的属性之后，调用该函数更新数据库中该记录
        """
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = execute(self.__update__, args)
        if rows != 1:
            print('failed to update by primary key: affected rows: {}'.format(rows))

    def remove(self):
        """
        将该对象所对应的记录从数据库中删除
        """
        args = [self.getValue(self.__primary_key__)]
        rows = execute(self.__delete__, args)
        if rows != 1:
            print('failed to remove by primary key: affected rows: {}'.format(rows))
