from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from py_linq import Enumerable

engine = create_engine('postgresql+psycopg2://postgres:1&0O#_)"d@localhost/Real_Estate', executemany_mode='batch')

connection = engine.connect()
result = connection.execute("select * from re_owner")

print(result)
collection = Enumerable()

class Owners:
    def __init__(self, ensurance_num, owner_name, age, gender):
        self.ensurance_num = ensurance_num
        self.owner_name = owner_name
        self.age = age
        self.gender = gender
    def __repr__(self):
        return 'Owner ensurance: {}, name: {}, age: {}, gender {}\n'.format(self.ensurance_num, self.owner_name, self.age, self.gender)

for row in result:
    owner = Owners(row[0], row[1], row[2], row[3])
    collection.append(owner)

print(collection[0].owner_name)

men_from_twenty_to_fourty = collection.where(lambda x: x.age < 20 and x.gender == "муж.").select(lambda y: (y.owner_name, y.age, y.gender))
print(men_from_twenty_to_fourty)

oldest_woman_sorted_by_name_with_age_stats = collection.where(lambda x: x.gender == "жен.").order_by_descending(lambda x: (x.age, x.owner_name), ).select(lambda y: (y.owner_name, y.age, y.gender)).first()
print(oldest_woman_sorted_by_name_with_age_stats)




