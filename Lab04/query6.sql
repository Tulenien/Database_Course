-- Определяемый пользователем тип данных CLR

create type obj_t as
(
    address varchar,
    value bigint,
    square smallint
);

-- drop type obj_t;
-- drop function getObjByCadNum;

create or replace function getObjByCadNum(cad_num bigint) returns obj_t
as
$$
plan = plpy.prepare("select obj_address, cad_value, obj_square from re_obj where cad_num = $1", ["bigint"])
obj = plpy.execute(plan, [cad_num])
return(obj[0]["obj_address"], obj[0]["cad_value"], obj[0]["obj_square"])
$$ language plpython3u;

select * from getObjByCadNum(824599521407922);