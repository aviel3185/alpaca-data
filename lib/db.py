from peewee import PostgresqlDatabase, Model, CharField, DateField, IntegerField, BooleanField, DateTimeField, \
    DoubleField

db = PostgresqlDatabase('postgres', user='alpaca', password='0nlyAlpaca!',
                        host='18.219.96.252', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class EarningsDate(BaseModel):
    ticker = CharField()
    cik = IntegerField()
    date = DateField()
    has_arrived = BooleanField(default=False)
    arrived_at = DateTimeField(null=True)

    class Meta:
        indexes = (
            (('ticker', 'date'), True),
        )


class Price(BaseModel):
    ticker = CharField()
    cik = IntegerField()
    iteration_uuid = CharField()
    price = DoubleField()
    created_at = DateTimeField()


db.connect()
db.create_tables([EarningsDate, Price])
