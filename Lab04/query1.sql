-- create extension if not exists plpython3u;

-- Скалярная функция CLR определяемая пользователем
-- Находит дату подтверждения по кадастровому номеру квартиры
create or replace function getDateByCadNum(cad_num bigint) returns date
as
$$
ppl = plpy.execute("select * from re_obj")
for obj in ppl:
    if obj["cad_num"] == cad_num:
        return obj["approval_date"]
return "None"
$$ language plpython3u;

select * from getDateByCadNum(639289004476470);