from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)

from models import next_id
from models.book import Book
from utils import log
import time


class Borrow(Model):

    __table__ = 'borrow'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    card_id = StringField(ddl='varchar(50)')
    book_id = StringField(ddl='varchar(50')
    admin_id = StringField(ddl='vaarchar(50)', default='-1')
    borrow_date = FloatField(default=time.time)
    return_date = FloatField(default=None)
    deleted = BooleanField(default=False)

    @classmethod
    def borrow_book(self, title, user):
        """
        返回1表示借阅成功
        """
        book = Book.find_one(title=title)

        bs = user.borrowed_books()
        if book in bs:
            log("Borrow: 无法重复借阅同一名字的书")
            return 0

        if book is not None and book.in_stock():
            log("Borrow: {}有库存".format(title))
            new_borrow = Borrow()
            new_borrow.card_id = user.card_id
            new_borrow.book_id = book.id
            new_borrow.return_date = None
            try:
                book.stock_minus_one()
            except Exception:
                # 库存数不足
                log("借书失败")
                return 0
            else:
                new_borrow.save()
                log("Borrow: 借书成功, 书名:{}".format(book.title))
                return 1
        else:
            log("Borrow: 借书失败: 书籍不存在或库存不足")
            return 0

    @classmethod
    def return_book(self, title, user):
        """
        归还书籍，返回1表示成功归还
        """
        book = Book.find_one(title=title)
        if book is not None:
            log("Return: 找到该书{}".format(title))
            # 找到借书记录
            b = Borrow.find_one(card_id=user.card_id,
                                book_id=book.id, deleted=False)

            if b is None:
                log("Return: 未找到这条借书记录")
                return 0

            if b.deleted:
                log("Return: 已经归还了书籍, 不可重复归还")
                return 0

            try:
                book.stock_add_one()
            except Exception:
                log("还书失败")
                return 0
            else:
                b.return_date = int(time.time())
                b.deleted = True
                try:
                    b.update()
                except Exception:
                    log("数据库更新错误")
                    exit()
                else:
                    log("Return: 还书成功, 书名:({})".format(book.title))
                    return 1
        else:
            log("Return: 还书失败: 书籍不存在")
            return 0
