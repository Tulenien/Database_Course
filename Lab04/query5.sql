-- Триггер CLR
-- При добавлении новой строки в таблицу re_ownership
-- добавляет владельца, если его не существовало
-- до этого, в таблицу re_ownership

create or replace function controlOwnership()
returns trigger
as
$$
person = TD['new']["ensurance_num"]
owners = plpy.execute("select ensurance_num from re_owner")
flag = 1
for owner in owners:
    if owner["ensurance_num"] == person:
        flag = 0
        break
if flag == 1:
    try:
        plan = plpy.prepare("insert into re_owner(ensurance_num, owner_name, age, gender) values($1, $2, $3, $4);", ["bignum", "varchar", "smallint", "varchar"])
        plan = plpy.execute(plan, [person, null, null, null])
        plpy.notice("new owner added")
    except:
        plpy.notice("problems on adding new owner")
plpy.notice("owner exists in base")
$$ language plpython3u;

--drop trigger control_ownership on re_ownership;

create trigger control_ownership
before insert on re_ownership for each row
execute procedure controlOwnership();

insert into re_ownership
(
    id, cad_num, ensurance_num, ownership_type_id
)
values
(
    2235,
    824599521407922,
    92177177109,
    4
);

select max(id) from re_ownership;
select ensurance_num, cad_num from re_ownership 
where ownership_type_id = 4;

select * from re_ownership
where ensurance_num = 92177177109 
and cad_num = 824599521407922;

delete from re_ownership
where ensurance_num = 92177177109 
and cad_num = 824599521407922;