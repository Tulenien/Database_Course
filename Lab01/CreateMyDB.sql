--drop TABLE if EXISTS re_ownership;
--drop TABLE if EXISTS re_obj;
--drop TABLE if EXISTS re_owner;
--drop TABLE if EXISTS re_ownership_type;

create table if not exists RE_Owner(
    Ensurance_Num bigint not null primary key,
	Owner_Name varchar(80),
    Age smallint,
	Gender varchar(4)    
);
create table if not exists RE_Obj(
    Cad_Num bigint not null primary key,
    Obj_Address varchar(100),
    Cad_Value bigint,
    Approval_Date date
);
create table if not exists RE_Ownership_Type(
    Ownership_Type_Id smallint not null primary key,
    Ownership_Type_Name varchar(40)
);
create table if not exists RE_Ownership(
    id serial not null primary key,
    Cad_Num bigint references RE_Obj(Cad_Num),
    Ensurance_Num bigint references RE_Owner(Ensurance_Num),
    Ownership_Type smallint references RE_Ownership_Type(Ownership_Type_Id)
);

--copy Re_obj(Cad_Num, Obj_Address, Cad_Value, Approval_Date) from 'C:\Users\...\RE_ESTATE_DB\RE_Obj.csv' delimiter ',' csv;
--copy RE_Owner(Ensurance_Num, Owner_Name, Age, Gender) from 'C:\Users\...\RE_ESTATE_DB\RE_Owners.csv' delimiter ',' csv;
--copy RE_Ownership_Type(Ownership_Type_Id, Ownership_Type_Name) from 'C:\Users\...\RE_ESTATE_DB\RE_OwnershipType.csv' delimiter ',' csv;
--copy RE_Ownership(id, cad_num, ensurance_num, ownership_type_id) from 'C:\Users\...\RE_ESTATE_DB\RE_Ownership.csv' delimiter ',' csv;

--alter table re_obj add column obj_square smallint
--create temporary table sq(id bigint not null primary key, sqr SMALLINT);

-- Update BD with a new column values with id pre-generated 4 em

--copy sq(id, sqr) from 'C:\Users\...\RE_ESTATE_DB\RE_Square.csv' delimiter ',' csv;
--update re_obj
--set obj_square = sqr
--from sq
--where id = cad_num;

--alter table re_owner add constraint gender_constraint CHECK (Gender = 'жен.' or Gender = 'муж.');
-- Доп.задание