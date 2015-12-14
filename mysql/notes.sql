create database vocal_seagull;
grant all on vocal_seagull.* to 'gsc';
create user 'seagull' identified by 'bogus';
grant select,insert,update,delete on vocal_seagull.* to 'seagull';
