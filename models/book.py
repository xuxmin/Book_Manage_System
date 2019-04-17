from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)

from models import next_id


class Book(Model):

    __table__ = 'book'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    title = StringField(ddl='varchar(50)')
    press = StringField(ddl='varchar(50)')
    year = IntegerField()
    author = StringField(ddl='varchar(50)')
    price = FloatField(ddl='real')
    total = IntegerField()
    stock = IntegerField()

    def from_form(self, form):
        """
        根据提交的表单, 设置对象的属性
        """
        self.title = form.get('title', 'Unknown')
        self.press = form.get('press', 'Unknown')
        self.year = int(form.get('year', 0000))
        self.author = form.get('author', 'Unknown')
        self.price = float(form.get('price', 0.0))
        self.total = int(form.get('total', 0))
        self.stock = int(form.get('stock', self.total))

    @classmethod
    def has_book(cls, name):
        """
        判断数据库中是否有书名为name的书
        """
        if Book.find_one(title=name) is None:
            return False
        else:
            return True

    @classmethod
    def search(cls, form):
        """
        条件搜索
        """


    def in_stock(self):
        if self.stock > 0:
            return True
        else:
            return False

    def borrow(self):
        if self.stock > 0:
            self.stock = self.stock - 1
            print("{}书库存数减1".format(self.title))
        else:
            print("error:尝试借阅没有库存的书")

    def return_book(self):
        self.stock = self.stock + 1
