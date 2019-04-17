from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)

from models import next_id
import time


class Borrow(Model):

    __table__ = 'borrow'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    card_id = StringField(ddl='varchar(50)')
    book_id = StringField(ddl='varchar(50')
    admin_id = StringField(ddl='vaarchar(50)')
    borrow_time = FloatField(default=time.time)
    return_time = FloatField(default=time.time)
    
    @classmethod
    def borrow_book(self, form):
        title = form.get("title", '')
        book = Book.find_by(title=title)
        book_id = form.get("book_id", '')
        if book is not None and book.in_stock():
            book.borrow()
            print("借书成功, 书名:{}".format(book.title))
        else:
            print("借书失败")

    def return_book(self, form):
        card_id = form.get("card_id", '')
        book_id = form.get("book_id", '')
        # 找到该借书证借阅的所有书
        book = Borrow.find_by(card_id=card_id)
        if book_id in book[book_id]:
            # 如何表示书已经还了, 需要删除数据库中的记录吗?
            book.return_book()
        else:
            print("并没有借这本书")
