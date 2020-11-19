import json
FILENAME = "C:/Users/timof/Documents/Programming/DataBases/LabsDB/Lab05/tenantsCopy.json"

def readAttribute(jsonMas, attributeName):
    values = []
    flag = False
    # Assume that all array members are equal in structure >>
    if len(jsonMas) and attributeName in getAllKeys(jsonMas[0], values):
        flag = True
        values = []
        path = getPathfromAttributeName(jsonMas[0], attributeName)
        print(path)
        for i in range(len(jsonMas)):
            value = jsonMas[i]
            for key in path:
                value = value[key]
            values.append(value)
    return values

def getPathfromAttributeName(nestedDict, value, prepath=()):
    for k, v in nestedDict.items():
        path = prepath + (k,)
        if k == value: # found key
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = getPathfromAttributeName(v, value, path)
            if p is not None:
                return p

def getAllKeys(start, keys):
    if type(start) == dict:
        for key in start.keys():
            keys.append(key)
            getAllKeys(start[key], keys)
    return keys

if __name__ == "__main__":
    mas = []
    with open(FILENAME) as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            mas.append(data[i])
    #check = {"id":1, "info":{"name":"", "purchases":{"qty":5}, "surname":"", }}
    keys = []
    keys = getAllKeys(mas[0], keys)
    values = [{key:readAttribute(mas, key)} for key in keys[2:]]
    #values = [readAttribute(mas, key) for key in keys[2:]]
    #for value in values:
        #print(*value, sep = ', ', end = ';\n')
    print(values)
    with open('tableCols.json', 'w') as outfile:
        json.dump(values, outfile)