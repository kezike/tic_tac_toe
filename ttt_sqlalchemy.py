from sqlalchemy import Table, Column, Integer, String, Unicode, Boolean, MetaData, ForeignKey
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)
metadata = MetaData()

games = Table('games', metadata,
             Column('id', Integer, primary_key=True), 
             Column('channel_id', String),
             Column('board_id', String),
             Column('player1_uname', String),
             Column('player2_uname', String),
             Column('turn', String(1)),
             Column('is_over', Boolean)
)

boards = Table('boards', metadata,
              Column('id', Integer, primary_key=True), 
              Column('turn', String(1))
)

players = Table('players', metadata,
               Column('id', Integer, primary_key=True), 
               Column('piece', String(1))
)
