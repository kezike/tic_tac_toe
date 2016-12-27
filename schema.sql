drop table if exists player
create table player (
  id integer primary key autoincrement,
  game_piece text,
  has_won boolean
);

drop table if exists game;
create table game (
  id integer primary key autoincrement,
  board text,
  player1 player,
  player2 player,
  winner player
);
