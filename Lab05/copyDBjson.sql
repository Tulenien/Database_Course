copy
(
    select jsonb_agg(reo)
    from re_obj reo
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_objCopy.json';

copy
(
    select jsonb_agg(reow)
    from re_ownership reow
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownershipCopy.json';

copy
(
    select jsonb_agg(reo)
    from re_owner reo
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownerCopy.json';

copy
(
    select jsonb_agg(reot)
    from re_ownership_type reot
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\re_ownership_typeCopy.json';

copy
(
    select jsonb_agg(tns)
    from tenants tns
)
to 'C:\Users\timof\Documents\Programming\DataBases\LabsDB\Lab05\tenantsCopy.json';