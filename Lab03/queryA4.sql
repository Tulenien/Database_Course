-- Числа Фибоначчи (рекурсивно)
drop function if EXISTS Fib;

create function Fib (fvalue int, svalue int, n int)
returns table (previos int, current int)
as 
$$
begin
    return query select fvalue, svalue;
    if n > 0 then
        return query
        select *
        from Fib(svalue, fvalue + svalue, n - 1);
    end if;
end
$$;
language plpgsql

select * from Fib(3, 5, 10);

create or replace function getValuesFromTree(loc varchar)
returns setof locations
as
$$
begin
    return query
            select l.parent, l.loc_name
            from 
end;
$$ language plpgsql;

select * from getValuesFromTree('Россия');