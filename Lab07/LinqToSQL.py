from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, BigInteger, Date, ForeignKey
from sqlalchemy.orm import relationship
engine = create_engine('postgresql+psycopg2://postgres:1&0O#_)"d@localhost/Real_Estate', 
executemany_mode='batch')

meta = MetaData()

reobj_table = Table\
(
    're_obj',
    meta,
    Column('cad_num', BigInteger, primary_key=True),
    Column('obj_address', String),
    Column('cad_value', BigInteger),
    Column('approval_date', Date),
    Column('obj_square', Integer)
)

reownership_table = Table\
(
    're_ownership',
    meta,
    Column('id', BigInteger, primary_key=True),
    Column('cad_num', ForeignKey("re_obj.cad_num")),
    Column('ensurance_num', ForeignKey("re_owner.cad_num")),
    Column('ownership_type_id', ForeignKey("re_ownership_type.ownership_type_id"))
)

connection = engine.connect()
reobj = connection.execute(reobj_table.select())
reownership = connection.execute(reownership_table.select())

# obj_ownership = re_obj.outer_join

q = connection.execute(reownership_table.outerjoin(reobj_table).select())
print(q.fetchone())

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = engine)
session = Session()

res = session.execute('call table_size()')
print(res)
