-- Delete owners of the most expensive property in chosen ownership type
create or replace function DeleteMostExpensivePropertyByType(varchar) returns table
(
	ensurance bigint,
	property bigint,
	property_value bigint
)
as
$$
	declare r record;
	begin
		for r in
		(
			select
				ensurance_num,
				reo.cad_num,
				cad_value
			from 
				re_ownership reo join re_obj rob 
				on reo.cad_num = rob.cad_num
			where ensurance_num = 
			(
				select 
					ensurance_num
				from 
				(
					select
						reo.ensurance_num,
						sum(cad_value) over(partition by reo.ensurance_num) as PrPrice,
						row_number() over(partition by reo.ensurance_num) as num
					from
						re_ownership reo join re_ownership_type reot 
						on reo.ownership_type_id = reot.ownership_type_id
						join re_obj obj 
						on obj.cad_num = reo.cad_num
						join re_owner reow on reo.ensurance_num = reow.ensurance_num
					where 
						ownership_type_name = $1 and reow.age <> 0
				) as propSum
				where 
					propSum.num = 1
				order by 
					PrPrice desc
				limit 1
			)
			order by cad_value desc
		) loop
			ensurance = r.ensurance_num;
			property = r.cad_num;
			property_value = r.cad_value;
			delete from owner_view
			where owner_view.ensurance_num = r.ensurance_num;
			return next;
		end loop;
	end;
$$ language plpgsql;


select *
from DeleteMostExpensivePropertyByType('Индивидуальная собственность') join owner_view
on ensurance_num = ensurance;