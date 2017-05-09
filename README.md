# kiwi

A simple python orm.

It requries `MySQL-Python` library to work.


## Usage

### Model definition

```
from kiwi import Model, fields, MySQLDatabase


db = MySQLDatabase(host='127.0.0.1', port=3306, user='root', password='123456', database='test')

class User(Model):
    __tablename__ = 'users'

    name = fields.CharField()
    country = fields.CharField()
```

### Store Data

```
user = User(name='Mike', country='America')
user.save()
```

which is equivalent to :

```
mike = User.create(name='Mike', country='America')
```

Then a record can be deleted from database:


```
mike.delete()
```

### Retrieve Data


Get a single record:

```
user = User.get(country='America')
```

Or get all records that match a certain condition:

```
users = User.filter(name='Mike')
for u in user:
    print u.name, u.country
```

### Update data

```
user = User.get(name='Mike')
user.country = 'England'
user.save()
```

or update multiple objects at once:


```
User.where(country='America').update(country='England')
```
