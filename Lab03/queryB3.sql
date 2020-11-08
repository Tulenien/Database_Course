--B3) Хранимая процедура с курсором
-- Обновить дату подтверждения на текущую дату для квартир по стоимости

select *
into temp obj
from re_obj
order by re_obj.approval_date desc;

create or replace procedure updateApprovalDate(minPrice bigint, maxPrice bigint, dt date) as
$$
declare c cursor
	for select * 
	from obj
	where cad_value between minPrice and maxPrice;
	row record;
begin
	open c;
	loop
		fetch c into row;
		exit when not found;
		update obj
		set approval_date = dt
		where obj.cad_num = row.cad_num;
	end loop;
	close c;		
end
$$ language plpgsql;
call updateApprovalDate(10000000, 20000000, '2020-10-29');

select reo.approval_date, o.approval_date
from re_obj reo join obj o on reo.cad_num = o.cad_num
where reo.cad_value between 10000000 and 20000000;

drop procedure updateApprovalDate;
create or replace procedure updateApprovalDate(minPrice bigint, maxPrice bigint, dt date) as
$$
	declare c scroll cursor
		for select * 
		from obj
		where cad_value between minPrice and maxPrice;
	row record;
begin
	open c;
	move last from c;
	loop
		fetch backward from c into row;
		exit when not found;
		update obj
		set approval_date = dt
		where obj.cad_num = row.cad_num;
	end loop;
	close c;		
end
$$ language plpgsql;