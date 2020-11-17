-- Получение значений иерархии locations рекурсивно
-- drop function getValuesFromTree;

create or replace function getValuesFromTree(base varchar)
returns setof locations
as
$$
begin
    return query
    select (getValuesFromTree(l.Loc_Name)).*
    from locations l where l.Parent = base;

    return query
    select loc.Loc_Name, loc.Parent
    from locations loc
    where loc.Parent = base;
end
$$ language plpgsql;

select * from getValuesFromTree('Московская область');