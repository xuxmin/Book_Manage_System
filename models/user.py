from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)
import time

from models import next_id
from models.borrow import Borrow
from models.book import Book
from utils import log


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
        log('u:', u.password)
        user = User.find_one(username=u.username)
        log('user:', user)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None

    def has_card(self):
        if self.card_id == '' or self.card_id == 'None':
            return False
        else:
            return True

    def borrow_record(self):
        """
        返回用户的借书记录，格式为：书名，借阅时间，归还时间，是否归还
        """
        card_id = self.card_id
        infos = []
        bs = Borrow.find_all(card_id=card_id)
        for b in bs:
            info = {}
            print(b)
            book = Book.find_one(id=b.book_id)
            info['book'] = book.title
            info['bt'] = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.localtime(b.borrow_date))
            if b.return_date is None:
                info['rt'] = ""
            else:
                info['rt'] = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(b.return_date))
            info['de'] = b.deleted
            infos.append(info)
        log("infos:", infos)
        return infos

    def borrowed_books(self):
        """
        返回用户借阅的所有书
        """
        borrows = Borrow.find_all(card_id=self.card_id, deleted=False)

        books = []
        for b in borrows:
            book = Book.find_one(id=b.book_id)
            books.append(book)
        return books
