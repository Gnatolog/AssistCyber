from peewee import (
    SqliteDatabase,
    Model,
    CharField,
    IntegerField,
    AutoField,
    ForeignKeyField,
    DateTimeField,
)

from config_data.config import DB_PATH, DATE_FORMAT

db = SqliteDatabase(DB_PATH)  # подключение к бд


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_id = IntegerField(primary_key=True)
    username = CharField()


class SearchHistory(BaseModel):
    history_id = AutoField()
    user = ForeignKeyField(User, backref="search")
    title = CharField()
    due_date = DateTimeField()

    def __str__(self):
        return "{history_id}. {title} - {due_date}".format(
            history_id=self.history_id,
            title=self.title,
            due_date=self.due_date.strftime(DATE_FORMAT),
        )


def create_models():
    db.create_tables(BaseModel.__subclasses__())


create_models()
