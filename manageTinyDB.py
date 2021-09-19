from tinydb import TinyDB, Query
from _smartbinAPI import get_data_type
from config import dataType

db = TinyDB('db.json')

Table_User = db.table('User')
Table_Data = db.table('Data_Pie')
Table_Type = db.table('Data_Type')
Table_CC = db.table('CC')
Table_DateTime = db.table('DateTime')
q = Query()

def update_access_token(uname, access_token):
    Table_User.update({
        'Username': uname, 
        'Access_Token': access_token
    })

def get_user_token():
    data = Table_User.all()[0]
    return data['Username'], data['Access_Token']

def get_date_time():
    data = Table_DateTime.all()[0]
    return data['date'], data['time']

def get_data_pie():
    data = Table_Data.all()[0]

    return str(data['can_pie']), str(data['pet_pie']), str(data['plastic_pie']), \
        str(data['trash_pie']), str(data['sum_pie']) 

def get_calculate_point():
    data = Table_Data.all()[0]
    return str(data['calculatescore'])

def update_data_pie(id):
    data = Table_Data.all()[0]
    # get point from db
    point = Table_Type.search(q.id == id)[0]['points']
    # new point score
    calculatescore = data['calculatescore'] + point

    new_can_pie = data['can_pie']
    new_pet_pie = data['pet_pie']
    new_plastic_pie = data['plastic_pie']
    new_trash_pie = data['trash_pie']

    if id == 0:     # can
        new_can_pie = data['can_pie'] + 1
    elif id == 1:   # pet
        new_pet_pie = data['pet_pie'] + 1
    elif id == 2:   # plastic
        new_plastic_pie = data['plastic_pie'] + 1
    else:           # trash
        new_trash_pie = data['trash_pie'] + 1

    new_sum_pie = new_can_pie + new_pet_pie + \
        new_plastic_pie + new_trash_pie

    Table_Data.update({
        "can_pie": new_can_pie,
        "pet_pie": new_pet_pie,
        "plastic_pie": new_plastic_pie,
        "trash_pie": new_trash_pie,
        "sum_pie": new_sum_pie,
        "calculatescore": calculatescore
    })

    return str(new_can_pie), str(new_pet_pie), str(new_plastic_pie), \
        str(new_trash_pie), str(new_sum_pie)

def update_data_type():
    data = get_data_type()
    
    if data == 404:
        return 404
    
    for elem in data:
        Table_Type.update(elem, q.id == elem['id'])

def update_cc(can_cc, pete_cc, plastic_cc, other_cc):
    # Table_CC.insert({
    #     "can_cc": can_cc,
    #     "pete_cc": pete_cc,
    #     "plastic_cc": plastic_cc,
    #     "other_cc": other_cc
    # })

    Table_CC.update({
        "can_cc": int(can_cc),
        "pete_cc": int(pete_cc),
        "plastic_cc": int(plastic_cc),
        "other_cc": int(other_cc)
    })

def get_cc():
    return Table_CC.all()


def get_data_type_from_db():
    data = Table_Type.all()
    data_dict = {}
    data_list = []

    for DICT in dataType:
        for elem in data:
            if DICT["id"] == elem["id"]:
                data_dict.update({
                    "id": DICT["id"],
                    "class": DICT['class'],
                    "points": elem['points']
                })
                data_list.append(data_dict.copy())
                # name.append(DICT['class'])
                # points.append(elem['points'])

    # return name and point
    return data_list

def reset_db():
    Table_Data.update({
        "can_pie": 0,
        "pet_pie": 0,
        "plastic_pie": 0,
        "trash_pie": 0,
        "sum_pie": 0,
        "calculatescore": 0
    })