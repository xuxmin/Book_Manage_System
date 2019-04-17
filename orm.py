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

    # SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换。
    cur.execute(sql.replace('?', '%s'), args or ())
    if size:
        rs = cur.fetchmany(size)
    else:
        rs = cur.fetchall()

    cur.close()
    conn.close()
    print('rows returned: {}'.format(len(rs)))
    return rs


def execute(sql, args):
    """
    执行INSERT、UPDATE、DELETE语句
    """
    print("当前执行的sql语句:", sql)
    conn = create_conn()

    try:
        cur = conn.cursor()
        cur.execute(sql.replace('?', '%s'), args)
        affected = cur.rowcount
        cur.close()
        conn.close()
    except BaseException as e:
        raise
    return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


"""
Python内置类属性
__dict__ : 类的属性（包含一个字典，由类的数据属性组成）
__doc__ :类的文档字符串
__name__: 类名
__module__: 类定义所在的模块（类的全名是'__main__.className'，如果类位于一个导入模块mymod中，那么className.__module__ 等于 mymod）
__bases__ : 类的所有父类构成元素（包含了一个由所有父类组成的元组）

self 代表类的实例，而非类
"""


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


class VarcharField(Field):

    def __init__(self, name=None, primary_key=False, default=None, ddl='varchar(100)'):
        super().__init__(name, ddl, primary_key, default)


class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)


class FloatField(Field):

    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'real', primary_key, default)


"""
type 可以作为函数, 创建一个类, 看下面的例子

def sayHello(self,name):
    print("hello,"+name)

#通过type来创建一个类对象，名称为Person，这个类对象有一个方法sayHello
Person = type("Person",(),{"sayHello":sayHello})

#通过类对象来创建实例
p = Person()

p.sayHello("andy")  # hello andy 

"""


"""
__new__ 是在__init__之前被调用的特殊方法，__new__是用来创建对象并返回之的方法，__new_()是一个类方法
而__init__只是用来将传入的参数初始化给对象，它是在对象创建之后执行的方法

改写 __new__ 时, 表示我们希望控制对象的创建
"""


class ModelMetaclass(type):
    """
    定义metaclass，就可以创建类，最后创建实例。
    metaclass 允许我们创建类和修改类

    metaclass是类的模板，所以必须从type类型派生：
    """
    def __new__(cls, name, bases, attrs):
        """
        cls 当前准备创建的类的对象
        name 类的名字
        bases 类继承的父类集合
        attrs 类的方法集合
        """
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


# 当我们传入关键字参数metaclass时，它指示Python解释器在创建Model时，要通过ModelMetaclass.__new__()来创建

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

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

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                print('using default value for {}: {}'.format(key, str(value)))
                setattr(self, key, value)
        return value

    @classmethod
    def findAll(cls, where=None, args=None, **kw):
        """
        find objects by where clause.

        **kw:
        orderBy
        limit
        """
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)
        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = select(' '.join(sql), args)
        for r in rs:
            print('r:', r)
        return [cls(**r) for r in rs]

    @classmethod
    def findNumber(cls, selectField, where=None, args=None):
        ' find number by select and where. '
        sql = ['select {} _num_ from {}'.format(selectField, cls.__table__)]
        if where:
            sql.append('where')
            sql.append(where)
        rs = select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    @classmethod
    def find(cls, pk):
        ' find object by primary key. '
        rs = select('%s where %s=?' % (cls.__select__, cls.__primary_key__), [pk], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = execute(self.__insert__, args)
        if rows != 1:
            print('failed to insert record: affected rows: {}'.format(rows))

    def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = execute(self.__update__, args)
        if rows != 1:
            print('failed to update by primary key: affected rows: {}'.format(rows))

    def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = execute(self.__delete__, args)
        if rows != 1:
            print('failed to remove by primary key: affected rows: {}'.format(rows))


class User(Model):
    # 定义类的属性到列的映射, 相当于元类中的attrs, key--> value
    id = IntegerField('id', 'True')
    name = VarcharField('name')
    password = VarcharField('password')
    __table__ = 'user'


if __name__ == "__main__":
    print(User)
    print(User())
