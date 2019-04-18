from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)

from models import next_id
from utils import log


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
        """
        判断这本书是否有库存
        """
        if self.stock > 0:
            return True
        else:
            return False

    def stock_add_one(self):
        """
        将该书库存加1... 相当于还书了
        """
        if self.stock >= self.total:
            log("未知错误: ({})库存数将大于初始总量".format(self.title))
            raise Exception("库存数大于初始总量")
        else:
            try:
                self.stock = self.stock + 1
                self.update()
            except Exception:
                log("数据库更新错误")
                exit()
            else:
                log("({})库存数加1".format(self.title))

    def stock_minus_one(self):
        """
        将该书库存减1...
        """
        if self.stock <= 0:
            raise Exception("Error:库存数已为0")
        else:
            try:
                self.stock = self.stock - 1
                self.update()
            except Exception:
                log("数据库更新错误")
                # 数据库如果更新错误的话直接退出?
                exit()
            else:
                log("({})库存数减1".format(self.title))
