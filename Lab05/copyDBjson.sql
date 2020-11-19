copy
(
    select row_to_json(re_obj_data)
    from
    (
        select * from re_obj
    )re_obj_data
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_objCopy.json';

copy
(
    select row_to_json(re_ownership_data)
    from
    (
        select * from re_ownership
    )re_ownership_data
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownershipCopy.json';

copy
(
    select row_to_json(re_owner_data)
    from
    (
        select * from re_owner
    )re_owner_data
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownerCopy.json';

copy
(
    select row_to_json(re_ownership_type_data)
    from
    (
        select * from re_ownership_type
    )re_ownership_type_data
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownership_typeCopy.json';