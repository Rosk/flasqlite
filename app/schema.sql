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

drop table if exists messages;
create table messages (
  msg_id integer primary key autoincrement,
  msg_from integer not null,
  msg_to integer not null,
  msg_title text not null,
  msg_body text not null,
  msg_isread integer default 0 not null
);