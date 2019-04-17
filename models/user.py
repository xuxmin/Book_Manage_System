from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)
import time

from models import next_id


class User(Model):
    __table__ = 'user'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(65)')
    role = IntegerField(default=11)
    username = StringField(ddl='varchar(50)')
    created_time = FloatField(default=time.time)
    card_id = StringField(ddl='varchar(50)', default='None')

    def from_form(self, form):
        """
        根据 form 的内容设置对象的属性值
        """
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.email = form.get('email', '')

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_one(username=name) is None:
            # 创建一个User对象
            u = User()
            # 根据form生成属性值
            u.from_form(form)
            u.password = u.salted_password(pwd)
            # 将对象保存到数据库中
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.from_form(form)
        print('u:', u.password)
        user = User.find_one(username=u.username)
        print('user:', user)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None
    
    def has_card(self):
        if self.card_id == '' or self.card_id == 'None':
            return False
        else:
            return True