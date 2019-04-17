from .mysql_orm import(
    Model,
    StringField,
    FloatField,
    BooleanField,
    IntegerField,
)
from models import next_id


class Card(Model):

    __table__ = 'card'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    dept = StringField(ddl='varchar(50)')
    type = StringField(ddl='varchar(1)')

    @classmethod
    def apply_card(cls, user, form):
        """
        用户user申请一张借书证
        """
        if user.has_card():
            raise "ERROR"
        else:
            c = Card()
            c.name = form.get('name', '')
            c.dept = form.get('dept', '')
            c.type = form.get('type', '')
            c.save()
            c = Card.find_one(name=c.name)
            user.card_id = c.id
            user.update()
