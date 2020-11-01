drop view if ex
create view owner_view as
select *
from re_owner;

create or replace function UpdateInsteadAgeZero()
returns trigger as
$$
begin
	update re_owner
	set age = 0
	where ensurance_num = old.ensurance_num ;
	return old;
end;
$$ language plpgsql;

create trigger DeletedFromOwners
	instead of delete on owner_view
	for each row 
	execute procedure UpdateInsteadAgeZero()