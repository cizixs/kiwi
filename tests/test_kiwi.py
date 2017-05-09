from kiwi import Model, fields, Database


Database.connect(host='127.0.0.1', password='123456', database='test')


class User(Model):
    name = fields.Field()
    country = fields.Field()
    phone_number = fields.Field()


User.create(name='cizixs', country='China', phone_number='2434-3489-3478')
