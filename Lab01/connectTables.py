from random import randint
import csv
'''
    Id's
    1 - personal (up to 10 flats)
    2 - partionary (5 and more persons on 1 flat)
    3 - common partionary (up to 3 persons)
    4 - cooperative partionary (2 persons - 1 flat)
    Do pop() from Obj bank if flat taken
    
    500 flats - 250 owners, type 4; 500 left
    250 flats - 1-6 owners each, 2; 250 left
    150 flats - 1-3 owners each, 3; 50 left
    100 flats -1-10 owned
    
'''
FILENAME1 = 'RE_Owners.csv'
FILENAME2 = 'RE_Obj.csv'
FILENAME3 = 'RE_Ownership.csv'
FILENAME4 = 'RE_Square.csv'

def copyInfo(filename):
    mas = []
    file = open(filename, mode = 'r', encoding = 'utf8')
    for line in file:
        mas.append(line[:len(line) - 1].split(','))
    file.close()
    return mas

def distribute(owners, objs):
    distributed = []
    current = []
    num = 1
## TYPE 4
    type_id = '4'
    for i in range(500):
        new_owner1 = owners.pop(0)
        new_owner2 = owners.pop(0)
        owners.append(new_owner1)
        owners.append(new_owner2)
        flat = objs.pop(0)
        current.append([str(num), flat[0], new_owner1[0],type_id])
        distributed.extend(current)
        current = []
        num += 1
        current.append([str(num), flat[0], new_owner2[0],type_id])
        distributed.extend(current)
        current = []
        num += 1
## TYPE 2
    type_id = '2'
    owners_num = randint(1, 6)
    new_owners = []
    for i in range(250):
        for j in range(owners_num):
            new_owner = owners.pop(0)
            new_owners.append(new_owner[0])
            owners.append(new_owner)
        flat = objs.pop(0)
        for k in range(len(new_owners)):
            current.append([str(num), flat[0], new_owners[k],type_id])
            distributed.extend(current)
            current = []
            num += 1
        owners_num = randint(1, 6)
        new_owners = []
## TYPE 3
    type_id = '3'
    owners_num = randint(1, 3)
    for i in range(150):
        for j in range(owners_num):
            new_owner = owners.pop(0)
            new_owners.append(new_owner[0])
            owners.append(new_owner)
        flat = objs.pop(0)
        for k in range(len(new_owners)):
            current.append([str(num), flat[0], new_owners[k],type_id])
            distributed.extend(current)
            current = []
            num += 1
        new_owners = []
## TYPE 1
    type_id = '1'
    flats = []
    owned = randint(1, 10)
    while len(objs) - owned > 0:
        new_owner = owners.pop(0)
        owners.append(new_owner)
        for i in range(owned):
            flats.append(objs.pop(0)[0])
        for j in range(len(flats)):
            current.append([str(num), flats[j], new_owner[0],type_id])
            distributed.extend(current)
            current = []
            num += 1
        owned = randint(1, 10)
        flats = []
    new_owner = owners.pop(0)
    if len(obj) > 0:
        for flat in obj:
            current.append([str(num), flat[0], new_owner[0],type_id])
            distributed.extend(current)
            current = []
            num += 1
    return distributed
    
def save_res(filename, res):
    file = open(filename, 'w', encoding = 'utf8', newline = '')
    writer = csv.writer(file)
    writer.writerows(res)
    file.close()
    
def create_square(objs):
    '''
    From 2,5 millions to 3 millions is Cheap, *1
    From 3 millions to 10 millions is Affordable, *1.25
    From 10 millions to 20 millions is Expensive, *1.5
    From 20 millions to 40 millions is Luxurious, *2
    '''
    sq_meter = 75757.58
    distributed = []
    for obj in objs:
        price = int(obj[len(obj) - 2])
        id_ = obj[0]
        if price >= 2500000 and price < 3000000:
            distributed.append([id_, round(price / sq_meter * 1.00)])
        elif price >= 3000000 and price < 10000000:
            distributed.append([id_, round(price / sq_meter * 1.25)])
        elif price >= 10000000 and price < 20000000:
            distributed.append([id_, round(price / sq_meter * 1.50)])
        elif price >= 20000000 and price < 40000000:
            distributed.append([id_, round(price / sq_meter * 2.00)])
    return distributed

#owners = copyInfo(FILENAME1)
#obj = copyInfo(FILENAME2)
#distributed = distribute(owners, obj)
#save_res(FILENAME3, distributed)
#distributed = create_square(obj)
#save_res(FILENAME4, distributed)

