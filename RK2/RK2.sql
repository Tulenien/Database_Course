create table if not exists automobil
(
    id serial not null primary key,
    marka varchar(100),
    model varchar(100),
    create_date date,
    reg_date date
);
create table if not exists driver
(
    id serial primary key,
    lic_num integer,
    phone bigint,
    fio varchar(100),
    car serial references automobil(id)
);
create table if not exists penalty
(
    id serial not null primary key,
    ptype varchar(100),
    pvalue integer,
    warning boolean
);
create table if not exists dp
(
    id serial not null primary key,
    dr serial references driver(id),
    p serial references penalty(id)
);

select * from automobil;
select * from driver;
select * from penalty;
select * from dp;

insert into automobil(marka,model,create_date,reg_date)
values  ('Nissan', 'GT-R', '2017-11-13', '2017-10-14'),
        ('Porsche', '911', '2017-11-13', '2017-11-24'),
        ('Ferrari', '488', '2016-09-04', '2017-01-03'),
        ('Mercedes', 'AMG GT', '2019-06-25', '2020-11-21'),
        ('Audi', 'R8', '2020-04-03', '2020-11-07'),
        ('Aston Martin', 'V12 Vantage', '2020-03-05', '2020-11-11'),
        ('Chevrolet', 'Corvette (C7)', '2020-01-04', '2020-11-10'),
        ('Lamborghini', 'Huracan', '2020-02-05', '2020-11-11'),
        ('Honda Civic', 'Si Coupe', '2019-03-06', '2020-11-12'),
        ('Audi', 'R8', '2020-04-07', '2020-11-15');

insert into driver(lic_num,phone,fio,car)
values  (3151, 88005553535, 'Скайвокер Люк Вейдорович', 5),
        (1234, 88005553535, 'Иванов Иван Иванович', 1),
        (1235, 88005553536, 'Иванова Мария Петровна', 2),
        (1239, 88005553537, 'сэр Джуффин Халли', 3),
        (1233, 88005553538, 'Шурф Лонли Локли', 4),
        (3245, 88005553539, 'Рюрикович Иван Васильевич', 5),
        (9797, 88005553540, 'Раздорнов Иван Никифорович', 6),
        (1195, 88005553541, 'Павел Иванович Чичиков', 7),
        (1354, 88005553542, 'Штамп Петр Антонович', 8),
        (4626, 88005553543, 'Примеров Ион Валерьевич', 9),
        (3511, 88005553543, 'Секундов Вий Святович', 10);

insert into penalty(ptype, pvalue, warning)
values  ('Пересечение двойной сплошной', 10000, 'f'),
        ('Пересечение двойной сплошной', 100000, 't'),
        ('Остановка в неположенном месте', 2000, 't'),
        ('Остановка в неположенном месте', 2000, 'f'),
        ('Превышение скорости', 2000, 't'),
        ('Превышение скорости', 2000, 'f'),
        ('Пересечение разметки', 2000, 't'),
        ('Пересечение разметки', 2000, 'f'),
        ('Кирпич', 8888, 't'),
        ('Кирпич', 8888, 'f');


insert into dp(dr, p)
values  (1, 1),
        (2, 4),
        (2, 5),
        (3, 9),
        (6, 10),
        (7, 1),
        (8, 4),
        (9, 6),
        (2, 2),
        (11, 5);

-- Выбрать штрафы стоимостью > 2000
select ptype, pvalue
from penalty
where pvalue > 2000;

-- Организовать штрафы по водителям(кто сколько и какие получил)
select row_number() over (partition by dr) rn, dr, p
from dp;


-- Все штрафы водителя со штрафом Пересечение двойнй сплошной
select p, driver.fio
from dp join
(
    select dp.dr r
    from dp
    where p = 2
) as a on dp.dr = a.r
join driver on dp.dr = driver.id;

create or replace function tr_1()
returns trigger as
$example_table$
    begin
        return old;
    end;
$example_table$ language plpgsql;

create trigger tr1 after delete on driver for each row execute procedure tr_1();
create trigger tr2 after delete on driver for each row execute procedure tr_1();
create trigger tr3 after delete on driver for each row execute procedure tr_1();
create trigger tr4 after delete on driver for each row execute procedure tr_1();

-- TODO
create or replace function(varchar sch, obj) as
$$
    DECLARE
    INTEGER I;
    begin
    select
        schemaName = $1
        objectName = $2
    from
        sys.triggers tr
        join sys.objects o on o.object_id = tr.parent_id
        join sys.schemas s on s.schema_id = o.schema_id
    where
        tr.parent_class_desc = 'OBJECT_OR_COLUMN'
    order by
        s.name, o.name, tr.name

    return i;
$$ language plpgsql;