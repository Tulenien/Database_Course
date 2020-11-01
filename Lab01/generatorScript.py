from faker import Faker
from random import randint
import csv

FILENAME1 = 'RE_Owners.csv'
FILENAME2 = 'RE_Obj.csv'
FILENAME3 = 'RE_OwnershipType.csv'
COUNT = 1000
START_VALUE = 2500000
END_VALUE =  40000000
def genOwners():
    RE_Owners = []
    gender_m = ',муж.'
    gender_f = ',жен.'
    fake = Faker('ru_RU')
    for i in range (COUNT):
        current = str(randint(10000000000, 99999999999)) + ','
        current += fake.name() + ','
        current += str(randint(18,70))
        if current[len(current) - 1] == 'а':
            current += gender_f
        else:
            current += gender_m
        current = current.split(',')
        RE_Owners.append(current)
    file = open(FILENAME1, 'w', encoding = 'utf8', newline = '')
    writer = csv.writer(file)
    writer.writerows(RE_Owners)
    file.close()

def genObj():
    RE_Obj = []
    fake = Faker('ru_RU')
    for i in range(COUNT):
        current = []
        current.append(randint(100000000000000, 999999999999999))
        current.append(fake.address())
        current.append(randint(START_VALUE, END_VALUE))
        current.append(fake.date())
        RE_Obj.append(current)
    file = open(FILENAME2, 'w', encoding = 'utf8', newline = '')
    writer = csv.writer(file)
    writer.writerows(RE_Obj)
    file.close()

def genOwnershipType():
    mas = [[1, 'Индивидуальная собственность'],
           [2, 'Долевая собственность'],
           [3, 'Общая долевая собственность'], 
           [4, 'Общая совместная собственность']]
    file = open(FILENAME3, 'w', encoding = 'utf8', newline = '')
    writer = csv.writer(file)
    writer.writerows(mas)
    file.close()

#genObj()
#genOwners()
#genOwnershipType()
