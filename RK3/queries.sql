--create database rk3;

create table if not exists ctrl
(
    id serial not null primary key,
    emp serial references emps(id),
    sdate date,
    week_day varchar(20),
    stime time,
    typ integer
);

create table if not exists emps
(
    id serial not null primary key,
    fio varchar(80),
    birthday date,
    dep varchar(40)
);

insert into emps(fio, birthday, dep)
values ('Иванов Иван Иванович', '1990-11-05', 'Менеджер'),
       ('Шурф Лонли Локли', '1948-07-07', 'IT'),
       ('Штамп Петр Антонович', '1990-11-07', 'Менеджер'),
       ('Примеров Ион Валерьевич', '1983-06-23', 'Менеджер'),
       ('Секундов Вий Святович', '1956-04-15', 'Бухгалтерия');

select * from emps;

insert into ctrl(emp, sdate, week_day, stime, typ)
values (1, '2020-12-19', 'Суббота', '08:58:59', 1),
       (2, '2020-12-19', 'Суббота', '09:59:59', 1),
       (5, '2020-12-19', 'Суббота', '09:00:01', 1),
       (4, '2020-12-19', 'Суббота', '09:11:00', 1),
       (4, '2020-12-19', 'Суббота', '15:00:00', 2),
       (4, '2020-12-19', 'Суббота', '15:30:00', 1),
       (4, '2020-12-19', 'Суббота', '18:11:00', 2),
       (3, '2020-12-19', 'Суббота', '09:16:00', 1);

insert into ctrl(emp, sdate, week_day, stime, typ)
values (1, '2020-12-19', 'Суббота', '12:58:59', 2),
       (1, '2020-12-19', 'Суббота', '12:59:59', 1),
       (1, '2020-12-19', 'Суббота', '15:30:59', 2),
       (1, '2020-12-19', 'Суббота', '16:00:59', 1),
       (1, '2020-12-19', 'Суббота', '18:58:59', 2),
       (4, '2020-12-19', 'Суббота', '18:13:00', 1),
       (4, '2020-12-19', 'Суббота', '18:15:00', 2);

select * from ctrl;

create or replace function getMinAgeLateFor10Mins(time)
returns interval as
$$
    select min(age(birthday))
    from
    (
        select row_number() over (partition by emps.id) as rn, fio, birthday
        from emps join ctrl
        on emps.id = ctrl.emp and ctrl.typ = 1 and stime - $1 > '00:10:00'
    ) nest;
$$ language sql;

select * from getMinAgeLateFor10Mins('10:00:00');