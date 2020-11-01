--drop table if exists Entry;
--drop table if exists Patients;
--drop table if exists Journal;
--drop table if exists Doctors;
--drop table if exists Clinic;

create table if not exists Clinic
(
    Cli_Id bigint not null primary key,
	Cli_Address varchar(100),
    Rating smallint
);
create table if not exists Doctors
(
    Doc_Id bigint not null primary key,
    Doc_Name varchar(80),
	Spec varchar(80),
	Cli_Id bigint references Clinic(Cli_Id)
);
create table if not exists Patients
(
    Pat_Id bigint not null primary key,
	Pat_Name varchar(80),
	Desease varchar(100),
	Doc_Id bigint references Doctors(Doc_Id)
);
create table if not exists Journal
(
	J_Id smallint not null primary key,
	Pat_Id bigint references Patients(Pat_Id),
    Entry_Id bigint references Entry(Entry_Id),
	J_Date date
);
create table if not exists Entry
(
    Entry_Id bigint not null primary key,
	Entry_Text varchar(100),
);

