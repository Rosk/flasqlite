drop table if exists user;
create table user (
  user_id integer primary key autoincrement,
  user_name text not null,
  user_email text not null,
  user_pw_hash text not null,
  user_land text not null,
  user_points integer not null,
  user_status integer not null
);

drop table if exists comment;
create table comment (
  comment_id integer primary key autoincrement,
  comment_uid integer not null,
  comment_title text not null,
  comment_text text not null,
  comment_time text not null
);