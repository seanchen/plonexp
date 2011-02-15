-- 
-- provide following satemats as samples for create a MySQL database 
-- for Plone.  using the mysql client:
-- $ mysql -u root -p < plone-db.sql
--
drop database if exists relstoragetest;
create database relstoragetest;

-- 
drop database if exists plone;
create database plone;

grant all on relstoragetest.* to 'relstoragetest'@'localhost' identified by 'password';

grant all on plone.* to 'plone'@'localhost' identified by 'plonepassword';

flush privileges;
