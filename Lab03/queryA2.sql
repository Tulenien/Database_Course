create or replace function getOwnerByEnsurance(varchar) returns setof re_owner as
$$
	select *
	from re_owner
	where owner_name = $1;
$$ language sql;

select *
from getOwnerByEnsurance('Евстафий Георгиевич Красильников'); 

--drop FUNCTION if EXISTS getOwnerByEnsurance;