-- Пользовательская агрегатная функция
-- Считает количество владельцев квартиры по ее кадастровому номеру
-- Если квартира в индивидуальной собственности - вернуть 1 
create or replace function howManyOwners(cad_num bigint) returns integer
as
$$
data = plpy.execute("select * from re_ownership");
owners_num = 0
for d in data:
    if d["cad_num"] == cad_num:
        if d["ownership_type_id"] == 1:
            return 1
        else:
            owners_num += 1
return owners_num
$$ language plpython3u;

select * from howManyOwners(118808315392150);
select * from howManyOwners(443315876273126); -- ownership_type_id = 1, one owner possible