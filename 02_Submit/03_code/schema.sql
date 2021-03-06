drop table if exists Devices cascade;
drop table if exists Suppliers cascade;
drop table if exists Produce cascade;
drop table if exists Companies cascade;
drop table if exists Collaborate cascade;
drop table if exists Retailers cascade;
drop table if exists Sales cascade;
drop table if exists Retailers_Sale cascade;
drop table if exists Stores cascade;
drop table if exists Users cascade;
drop table if exists Reviews cascade;

create table Companies(
    name varchar(32) primary key,
    country varchar(32),
    founder varchar(32),
    found_date varchar(16),
    website varchar(128)
);

create table Devices(
    name varchar(32) primary key,
    launch_date date,
    type varchar(32),
    price decimal,
    capacity integer,
    chip varchar(32),
    camera decimal,
    battery integer,
    dimension varchar(32),
    screen_size decimal,
    weight decimal,
    os varchar(32),
    C_name varchar(32) not null,
    foreign key (C_name) references Companies(name),
    check (type in ('Phone', 'Laptop', 'Desktop', 'Pad', 'Watch', 'Other'))
);

create table Suppliers(
    name varchar(32) primary key,
    country varchar(32)
);

create table Produce(
    M_name varchar(32),
    D_name varchar(32),
    primary key (M_name, D_name),
    foreign key (M_name) references Suppliers(name),
    foreign key (D_name) references Devices(name)
);

create table Collaborate(
    M_name varchar(32),
    C_name varchar(32),
    primary key (M_name, C_name),
    foreign key (M_name) references Suppliers(name),
    foreign key (C_name) references Companies(name)
);

create table Retailers(
    name varchar(32) primary key,
    type varchar(32),
    check(type in ('Comprehensive', 'Electronic', 'Carrier', 'Official', 'Other'))
);

create table Sales(
    id serial primary key,
    year integer,
    season char(2),
    quantity integer not null,
    check(season in ('Q1', 'Q2', 'Q3', 'Q4'))
);

create table Retailers_Sale(
    D_name varchar(32),
    R_name varchar(32),
    sid integer,
    primary key (D_name, R_name, sid),
    foreign key (D_name) references Devices(name),
    foreign key (R_name) references Retailers(name),
    foreign key (sid) references Sales(id)
);

create table Stores(
    id integer,
    R_name varchar(32),
    address varchar(128),
    operation_time varchar(128),
    contact_number varchar(32),
    primary key (id, R_name),
    foreign key (R_name) references Retailers(name) on delete cascade
);

create table Users(
    username varchar(32) primary key,
    age integer,
    gender char(1),
    password char(64) not null,
    email varchar(32),
    check (gender in ('M', 'F', '')),
    check (age > 0)
);

create table Reviews(
    id serial primary key,
    content text,
    rating integer,
    time date,
    D_name varchar(32) not null,
    U_name varchar(32) not null,
    foreign key (D_name) references Devices(name),
    foreign key (U_name) references Users(username),
    check (rating in (0, 1, 2, 3, 4, 5))
);
