-- Tenants are people who pay rent to owners
create table if not exists tenants 
(
    id serial not null primary key,
    info json not null
);

insert into tenants(info)
values('{"name":"James",    "surname":"Bond",       "rent":1000}'),
      ('{"name":"Pew",      "surname":"Blind",      "rent":-10}'),
      ('{"name":"Billy",    "surname":"Bones",      "rent":10}'),
      ('{"name":"Jack",     "surname":"Sparrow",    "rent":-1000}'),
      ('{"name":"Harry",    "surname":"Potter",     "rent":13}'),
      ('{"name":"Indiana",  "surname":"Jones",      "rent":-20000}'),
      ('{"name":"Lara",     "surname":"Croft",      "rent":-19999}'),
      ('{"name":"Bruce",    "surname":"Wayne",      "rent":10000}'),
      ('{"name":"Ebenezer", "surname":"Scrooge",    "rent":20000}'),
      ('{"name":"Scrooge",  "surname":"McDuck",     "rent":19999}');

insert into tenants(info)
values('{"surname":"NoName",    "rent":1}'),
      ('{"name":"NoSurname",    "rent":1}'),
      ('{"name":"No",           "surname":"Rent"}');

insert into tenants(info)
values('{"rent":1}');

select * from tenants;
select info ->> 'name' n, info ->> 'surname' surname
from tenants;