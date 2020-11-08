--drop function getObjByAddress;
-- Определяемая пользователем табличная функция CLR
-- Находит объекты недвижимости, чей адрес содержит подстроку

create or replace function getObjByAddress(address varchar)
returns table
(
    cad_num bigint, 
    obj_address varchar, 
    cad_value bigint, 
    approval_date date, 
    obj_square smallint
)
as
$$
objs = plpy.execute("select * from re_obj")
result = []
for obj in objs:
    if address in obj["obj_address"]:
        result.append(obj)
return result
$$ language plpython3u;

select * from getObjByAddress('Москва');