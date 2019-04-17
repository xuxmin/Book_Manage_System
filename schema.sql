-- 如果bms数据库不存在，就创建bms数据库：
create database if not exists bms;

-- 切换到test数据库
use bms;

-- 删除book表,card表和borrow表（如果存在）：
drop table if exists borrow;
drop table if exists book;
drop table if exists card;
drop table if exists user;


create table user(
    id varchar(50) not null,
    email varchar(50),
    password varchar(65) not null,
    role int not null,
    username varchar(50) not null,
    created_time real not null, 
    primary key(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建book表：
create table book(
    id varchar(50) not null,
    title varchar(50) not null,
    author varchar(50) not null,
    year int not null,
    press varchar(50) not null,
    price numeric(10,2) not null,
    total int not null,
    stock int not null,
    primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建card表：
create table card(
    id varchar(50) not null,
    name varchar(50) not null,
    dept varchar(50) not null,
-- type表示借书人的类别，T为教师，S为学生
    type varchar(1) not null,
    primary key (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 创建borrow表：
create table borrow(
    id varchar(50) not null,
    card_id varchar(50) not null,
    book_id varchar(50) not null,
    admin_id varchar(50) not null,
    borrow_date real,
    return_date real,
    primary key (id),
    foreign key (card_id) references card(id),
    foreign key (book_id) references book(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- OK:
SELECT 'ok' as 'result:';