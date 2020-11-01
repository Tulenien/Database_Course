--B1) Хранимая процедура без параметров или с параметрам
-- Меняем цену в соответствии с новой ценой за квадратный метр площади

select *
into temp obj
from re_obj;

create or replace procedure update_price(newPrice real, SqrL int, SqrH int) as
$$
	update obj
	set cad_value = obj_square * newPrice
	where obj_square between SqrL and SqrH 
$$	language sql;

call update_price(30000, 100, 200);

select re_obj.cad_value as newValue, obj.cad_value as OldValue
from obj join re_obj on obj.cad_num = re_obj.cad_num
where obj.obj_square between 100 and 200
order by obj.cad_value desc;
