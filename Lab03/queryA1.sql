-- Максимальная стоимость квартиры
create function maxObjValue() returns int as
'
	select max(cad_value)
	from re_obj
' language sql;

select maxObjValue();

drop function if exists maxObjValue;