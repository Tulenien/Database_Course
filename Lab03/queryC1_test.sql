insert into re_ownership
values
(
    2234, 313951370789349, 15923086991, 1
);

select *
from new_inserts_re_ownership;

delete from re_ownership
where id = 2234 or id = 2235