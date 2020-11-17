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
	where ensurance_num = old.ensurance_num;
	return old;
end;
$$ language plpgsql;

create trigger DeletedFromOwners
	instead of delete on owner_view
	for each row
	execute procedure UpdateInsteadAgeZero()

-- TODO: When smth is deleted from re_ownership -
-- get all cad_nums and check owners
-- if their number of properties - 1 = 0, then
-- delete them in table. Check trigger on deletion
-- Does it work on deletion under other triggers
-- not connected to view or its own table
create or replace function NoProperty()
returns trigger as 
$$
begin
	
end;