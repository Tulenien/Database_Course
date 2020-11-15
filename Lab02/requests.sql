--1. С предикатом сравнения.
select 
	owner_name,
	ownership_type_name
from 
	re_owner join re_ownership 
	on re_owner.ensurance_num = re_ownership.ensurance_num
	join re_ownership_type 
	on re_ownership.ownership_type_id = re_ownership_type.ownership_type_id
where 
	age > 40;

--2. С предикатом between.
select 
	owner_name,
	cad_value
from 
	re_owner join re_ownership on re_owner.ensurance_num = re_ownership.ensurance_num
	join re_obj on re_ownership.cad_num = re_obj.cad_num
where 
	cad_value between 3500000 and 4000000

--3. С предикатом like
select 
	owner_name,
	obj_address
from 
	re_obj join re_ownership on re_obj.cad_num = re_ownership.cad_num and obj_address 
like '%Каменск-Шахтинский%'
join re_owner on re_ownership.ensurance_num = re_owner.ensurance_num

--4. Инструкция SELECT, использующая предикат IN с вложенным подзапросом.
select 
	ownership_type_name, 
	re_obj.cad_num, 
	obj_address
from 
	re_obj join re_ownership on re_obj.cad_num = re_ownership.cad_num
	join re_ownership_type on re_ownership.ownership_type_id = re_ownership_type.ownership_type_id
where 
	ownership_type_name in 
(
	select 
		ownership_type_name
	from 
		re_ownership_type
	where 
		ownership_type_id = 4
)

--5. Инструкция SELECT, использующая предикат EXISTS с вложенным подзапросом.
select 
	ensurance_num,
	owner_name
from 
	re_owner
where exists
(
	select 
		re_owner.ensurance_num
	from 
		re_ownership join re_obj on re_obj.cad_num = re_ownership.cad_num
	where 
		cad_value > 35000000
		and re_owner.ensurance_num = re_ownership.ensurance_num
)

--6. Инструкция SELECT, использующая предикат сравнения с квантором.
select 
	re_obj.cad_num
from 
	re_obj
where 
	cad_value > all
(
	select 
		cad_value
	from 
		re_obj join re_ownership on re_ownership.cad_num = re_obj.cad_num 
		join re_ownership_type on re_ownership.ownership_type_id = re_ownership_type.ownership_type_id
	where 
		re_ownership_type.ownership_type_id = 1
)

--7. Инструкция SELECT, использующая агрегатные функции в выражениях столбцов.
select 
	cast(avg(cad_value) as numeric(11, 3))
from 
	re_obj

--8. Инструкция SELECT, использующая скалярные подзапросы в выражениях столбцов.
select
	(
		select
			min(cad_value)
		from 
			re_obj
	) 	as min_price,
	cad_value as actual_price,
	(
		select min(cad_value)
		from re_obj
	) as max_price
from
	re_ownership join re_obj on re_ownership.cad_num = re_obj.cad_num
where 
	re_ownership.ownership_type_id = 1

--9. Инструкция SELECT, использующая простое выражение CASE.
select 
	cad_num,
	case extract(year from approval_date)
		when extract(year from current_date) - 1 then 'Last Year'
		when extract(year from current_date) - 2 then 'Two years ago'
		when extract(year from current_date) - 3 then 'Three years ago'
		else 'Long ago'
	end as When_
from 
	re_obj

--10. Инструкция SELECT, использующая поисковое выражение CASE.
select cad_num,
	case 
		when cad_value < 3000000 then 'Cheap'
		when cad_value < 10000000 then 'Affordable'
		when cad_value < 20000000 then 'Expensive'
		else 'Luxurious'
	end as Price
from re_obj

--11. Создание новой временной локальной таблицы из результирующего набора данных инструкции SELECT. 
select 
	cast(avg(cad_value) as numeric(11, 3))
into temporary table Average
from 
	re_obj

select * from Average

--12. Инструкция SELECT, использующая вложенные коррелированные подзапросы в качестве производных таблиц в предложении FROM.
select re_obj.cad_num, obj_square
from re_obj join
(
	select 
		cad_num
	from 
		re_obj
	where 
		cad_value between 2500000 and 3000000
	order by 
		cad_value desc
	limit 
		1
) as cheap on cheap.cad_num = re_obj.cad_num
union
select 
	re_obj.cad_num, obj_square
from 
	re_obj join
	(
		select 
			cad_num
		from 
			re_obj
		where 
			cad_value between 3000000 and 10000000
		order by 
			cad_value desc
		limit 
			1
	) as affordable on affordable.cad_num = re_obj.cad_num
union
select 
	re_obj.cad_num, obj_square
from 
	re_obj join
	(
		select cad_num
		from re_obj
		where cad_value between 10000000 and 20000000
		order by cad_value desc
		limit 1
	) as expensive on expensive.cad_num = re_obj.cad_num
union
select 
	re_obj.cad_num, obj_square
from 
	re_obj join
	(
		select
			cad_num
		from 
			re_obj
		where 
			cad_value between 20000000 and 40000000
		order by
			cad_value desc
		limit
			1
	) as luxurious on luxurious.cad_num = re_obj.cad_num
order by 
	obj_square desc

-- 13. Инструкция SELECT, использующая вложенные подзапросы с уровнем вложенности 3.
select 
	re_obj.cad_num, 
	re_obj.cad_value
from re_obj join 
	(
		select 
			re_obj.cad_num
		from 
			re_obj
		where 
			cad_value / obj_square <
			(
				select 
					min(cad_value / obj_square) as min_sm
				from 
					(
						select 
							cad_value,
							obj_square
						from 
							re_obj
						where 
							cad_value between 2500000 and 3000000
					) as smth
			)
		order by 
			cad_value asc
	) as other on re_obj.cad_num = other.cad_num
where 
	re_obj.cad_value < 10000000

-- 14. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY, но без предложения HAVING.
select 
	re_obj.cad_num, 
	cast(avg(cad_value) as numeric(11, 0)) as Average_price, 
	min(cad_value) as Min_price
from 
	re_obj join re_ownership on re_obj.cad_num = re_ownership.cad_num
join 
	re_ownership_type as rot on re_ownership.ownership_type_id = rot.ownership_type_id
where 
	ownership_type_name like '%_олевая %'
group by 
	re_obj.cad_num, cad_value
order by 
	min_price desc

-- 15. Инструкция SELECT, консолидирующая данные с помощью предложения GROUP BY и предложения HAVING.
select 
	re_obj.cad_num, cast(avg(cad_value) as numeric(11, 0)) as Average_price
from 
	re_ownership as ro join re_obj on ro.cad_num = re_obj.cad_num
where 
	ro.ownership_type_id = 2 or ro.ownership_type_id = 3 
group by 
	re_obj.cad_num
having avg(obj_square) >
	(
		select 
			avg(obj_square)
		from 
			re_obj
		where 
			cad_value between 10000000 and 20000000
	)

-- 16. Однострочная инструкция INSERT, выполняющая вставку в таблицу одной строки значений.
insert into 
	re_obj(cad_num, obj_address, cad_value, approval_date, obj_square)
values 
	(
		838083205810851, 
		'г. Москва, Московская обл., ул. Николо-Хованская, Испанские кварталы, д. 32 стр. 2/4 к. 69, 108814',
		6556000,
		NULL,
		30
	)

select
	re_obj.cad_num, 
	cad_value, 
	obj_address, 
	obj_square, 
	approval_date
from 
	re_obj
where 
	re_obj.cad_num = 838083205810851

-- 17. Многострочная инструкция INSERT, выполняющая вставку в таблицу результирующего набора данных вложенного подзапроса.
-- insert !!!into!!! для postgresql --
insert into 
	re_ownership(id, cad_num, ensurance_num, ownership_type_id)
	select 
		(
			select max(id) + 1
			from re_ownership
		), 
		838083205810851,
		ensurance_num, reo.ownership_type_id
	from 
		re_ownership as reo join re_obj on reo.cad_num = re_obj.cad_num
	group by 
		reo.ensurance_num, 
		reo.ownership_type_id
	order by 
		sum(re_obj.cad_value) asc
	limit 
		1


-- 18. Простая инструкция UPDATE.
update 
	re_obj
set 
	approval_date = current_date
where 
	approval_date is null

-- 19. Инструкция UPDATE со скалярным подзапросом в предложении SET.
update 
	re_obj
set 
	cad_value =
	(
		select 
			avg(cad_value)
		from 
			re_obj
		where 
			cad_value between 10000000 and 20000000
	)
where 
	cad_num = 838083205810851

-- 20. Простая инструкция DELETE.
-- delete !!!from!!! для postgresql --
delete from 
	re_obj
where 
	cad_value < 2500000


-- 21. Инструкция DELETE с вложенным коррелированным подзапросом в предложении WHERE.
delete from 
	re_obj
where 
	cad_num in
	(
		select 
			re_obj.cad_num
		from 
			re_obj join re_ownership as reo on reo.cad_num = re_obj.cad_num
			join re_owner on reo.ensurance_num = re_owner.ensurance_num
		where 
			owner_name like '%Алина Павловна%'
	)

-- 22. Инструкция SELECT, использующая простое обобщенное табличное выражение
-- ищет среднее количество квартир у каждого владельца
with CTE(ensurance, num)
as
	(
		select 
			reo.ensurance_num, count(*)
		from 
			re_ownership as reo
		group by 
			reo.ensurance_num
	)
select 
	cast(avg(num) as numeric (1, 0)) 
from 
	CTE

-- 23. Инструкция SELECT, использующая рекурсивное обобщенное табличное выражение.
--drop TABLE if exists locations;

create table if not exists Locations
(
    Loc_Name char(40) not null primary key,
    Parent char(40)
); 
insert into 
	locations(Loc_Name, Parent)
values
(
    'Балашиха',
    'Московская область'
);
-- создание таблицы --
with recursive hier
as
(
    select 
		l.loc_name, l.parent
    from 
		locations as l
    where 
		parent is null
    union all
    select 
		l.loc_name, l.parent
    from 
		locations as l join hier as h on l.parent = h.loc_name
)
select hier.loc_name, hier.parent
from hier;

-- 24. Оконные функции. Использование конструкций MIN/MAX/AVG OVER()
select 
	re_obj.cad_num, 
	reot.ownership_type_id, 
	reo.ensurance_num, 
	re_obj.cad_value, 
	cast(min(cad_value) over(partition by reot.ownership_type_id) as numeric(11, 3)) as MinPrice,
	cast(avg(cad_value) over(partition by reot.ownership_type_id) as numeric(11, 3)) as AvgPrice,
	cast(max(cad_value) over(partition by reot.ownership_type_id) as numeric(11, 3)) as MaxPrice
from 
	re_ownership as reo 
	join re_ownership_type as reot on reo.ownership_type_id = reot.ownership_type_id
	join re_obj on reo.cad_num = re_obj.cad_num

-- 25. Оконные функции для устранения дублей.
select 
	cad_num, 
	otype,  
	rn
from 
	(
		select 
			cad_num, 
			ownership_type_id as otype, 
			row_number() over(partition by cad_num) as rn
		from 
			re_ownership as reo
	) as smth
where
	smth.rn = 1
	
-- Дополнительное задание --
CREATE TABLE public.table1
(
    id integer,
    var1 "char",
    valid_from_dttm date,
    valid_to_dttm date
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;
ALTER TABLE public.table1
    OWNER to postgres;
-- Table: public.table2
-- DROP TABLE public.table2;
CREATE TABLE public.table2
(
    id integer,
    var2 "char",
    valid_from_dttm date,
    valid_to_dttm date
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.table2
    OWNER to postgres;
	
select 
	t1.var1, 
	t2.var2, 
	dates.id, 
	dates.valid_from_dttm, 
	dates.valid_to_dttm
from
(
	select
	dates_from_ordered_witn_rn.rn,
	dates_from_ordered_witn_rn.id,
	dates_from_ordered_witn_rn.valid_from_dttm,
	dates_to_ordered_witn_rn.valid_to_dttm
	from
	(
		select
			row_number() over (order by id, valid_from_dttm) as rn,
			id,
			valid_from_dttm
		from
		(
			select distinct id, valid_from_dttm
			from(
					select id, valid_from_dttm
					from table1
					union all
					select id, valid_from_dttm
					from table2
				) dates_from_all
        ) dates_from_uniq
	) dates_from_ordered_witn_rn,
	(
		select
		row_number() over (order by id, valid_to_dttm) as rn,
		id,
		valid_to_dttm
		from
        (
			select distinct id, valid_to_dttm
			from (
					select id, valid_to_dttm
					FROM table1
					union all
					SELECT id, valid_to_dttm
					FROM table2
				) dates_to_all
        ) dates_to_uniq
	) dates_to_ordered_witn_rn
	where dates_from_ordered_witn_rn.id = dates_to_ordered_witn_rn.id
	and dates_from_ordered_witn_rn.rn = dates_to_ordered_witn_rn.rn
) dates left outer join table1 t1 on
	dates.id = t1.id
	and t1.valid_from_dttm <= dates.valid_from_dttm
	and t1.valid_to_dttm >= dates.valid_to_dttm
	left outer join table2 t2 on
	dates.id = t2.id
	and t2.valid_from_dttm <= dates.valid_from_dttm
	and t2.valid_to_dttm >= dates.valid_to_dttm
order by 
	dates.id, 
	dates.valid_from_dttm, 
	dates.valid_to_dttm