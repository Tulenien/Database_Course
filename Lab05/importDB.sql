-- Structure:
--RE_Obj(Cad_Num, Obj_Address, Cad_Value, Approval_Date, Obj_square)
--RE_Owner(Ensurance_Num, Owner_Name, Age, Gender)
--RE_Ownership_Type(Ownership_Type_Id, Ownership_Type_Name)
--RE_Ownership(id, cad_num, ensurance_num, ownership_type_id)
-- Paths:
--'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_objCopy.json';
--'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownershipCopy.json';
--'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownerCopy.json';
--'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownership_typeCopy.json';

create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_objCopy.json';

create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownershipCopy.json';

create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownerCopy.json';

create temp table import(doc json);
copy import from 
'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownership_typeCopy.json';

select *
into temp tbl
from
(
    select p.*
    from import, json_populate_record(null::re_obj, doc) as p
) imp;

select * from tbl;

