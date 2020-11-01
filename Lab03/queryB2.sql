--B2) Рекурсивная хранимая процедура или хранимая процедура с рекурсивным ОТВ
-- Обновляет возраст у всех людей с заданным id

select *
into temp owners
from 
(
	select
		ensurance_num,
		row_number() over (partition by ensurance_num) as id,
		age
	from 
		re_owner
) as fr;

create procedure updateAgeInRange (idL int, idH int) as
$$
begin
	if (idL <= idH) then
	    update owners
     	set age = age + 1
    	where id = idl;
		call updateAgeInRange(idl + 1, idh);
    end if;
end;	
$$ language plpgsql;

call updateAgeInRange(1, 12);

select reo.age as old, o.age as new
from re_owner reo join owners o on o.ensurance_num = reo.ensurance_num