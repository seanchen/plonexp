-- 
-- sample statments to create database for Workpress 
-- on MySQL database.
-- $ mysql -u root -p < wordpress-db.sql
--

-- create a database calle CeShi
drop database if exists ceshi;
create database ceshi;

-- create wordpress user and grant privileges.
grant all on ceshi.* to 'ceshiyuan'@'localhost' identified by 'ceshipassword';

flush privileges;