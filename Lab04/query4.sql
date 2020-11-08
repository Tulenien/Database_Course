-- Хранимая процедура CLR
-- Добавляет новые объекты недвижимости в таблицу
-- Генерирует уникальный кадастровый номер самостоятельно

-- Тестирование процедуры выполняется на копии таблицы re_obj
select *
into temp obj
from re_obj;

--drop procedure addObj;

create or replace procedure addObj
(
    address varchar, 
    value integer,
    appdate date, 
    square integer
)
as
$$
cadn = plpy.execute("select min(cad_num) cn from obj;")
cadn = cadn[0]["cn"]
cadn -= 1
plan = plpy.prepare("insert into obj(cad_num, obj_address, cad_value, approval_date, obj_square) values($1, $2, $3, $4, $5);", ["bigint", "varchar", "bigint", "date", "smallint"])
plpy.execute(plan, [cadn, address, value, appdate, square])
$$ language plpython3u;

call addObj('г.Москва *****', 26000000, '2002-10-09', 67);
call addObj('г.Москва *****', 26000000, '2002-10-09', 68);
call addObj('г.Москва *****', 26000000, '2002-10-09', 69);

select *
  from obj
 where approval_date = '2002-10-09';