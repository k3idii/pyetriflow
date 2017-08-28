import libs.saucepan.saucepan as saucepan 
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import model

engine = sqla.create_engine('sqlite:///db/database.sqlite', echo=True)
Session = sessionmaker(bind=engine)

model.BaseClass.metadata.create_all(engine)

sql_session = Session()




@saucepan.route('/<name>')
def handle_hello(ctx, name=None):
  ctx.response.status_message = "ACK!"
  return "Hello {0:s} !".format(name)


saucepan.run(port=8081)
