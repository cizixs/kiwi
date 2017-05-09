import unittest

from faker import Factory

from kiwi import Model, fields, Database


fake = Factory.create()
Database.connect(host='127.0.0.1', password='123456', database='test')


class User(Model):
    name = fields.Field()
    country = fields.Field()
    phone_number = fields.Field()


class TestModel(unittest.TestCase):
    def setUp(self):
        pass

    def test_model(self):
        # add a record
        name, country, phone_number = fake.name(), fake.country(), fake.phone_number()
        User.create(name=name, country=country, phone_number=phone_number)


        # retrieve the record, and make sure the data is correct
        user = User.get(name=name)
        self.assertEqual(user.name, name)
        self.assertEqual(user.country, country)
        self.assertEqual(user.phone_number, phone_number)

        # update the method
        user.name = 'cizixs'
        user.save()
        self.assertEqual(user.name, 'cizixs')

        user.delete()

if __name__ == '__main__':
    unittest.main()
