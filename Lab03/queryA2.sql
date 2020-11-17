create or replace function getOwnerByEnsurance(varchar, int) returns setof re_owner as
$$
	select *
	from re_owner
	where owner_name = $1
	and age = $2;
$$ language sql;

select *
from getOwnerByEnsurance('Евстафий Георгиевич Красильников', 23); 

--drop FUNCTION if EXISTS getOwnerByEnsurance;