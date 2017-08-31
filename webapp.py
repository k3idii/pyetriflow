import libs.saucepan.saucepan as saucepan 
import sqlalchemy as sqla
from sqlalchemy.orm import sessionmaker
import model

ADMIN_TOKEN="so_so_secret"


engine = sqla.create_engine('sqlite:///db/database.sqlite', echo=True)
Session = sessionmaker(bind=engine)

model.BaseClass.metadata.create_all(engine)

sql_session = Session()


@saucepan.route("/admin/<method>/<op>")
class AdminHandler(saucepan.RoutableClass):
 
  def always(self, ctx, *a, **kw):
  	token = ctx.request.get.get('token')
  	if token != ADMIN_TOKEN:
  		raise saucepan.Http4xx(403,"Acces deny !")

  def default(self, ctx, *a):
    return " Nope !"
  
  def do_users(self, ctx, op=None):
  	if op == "add":
  		sql_session.add(model.XUser(name=ctx.request.get['username'], attributes={}))
  		sql_session.commit()
  		return "DONE"
  	if op == "del":
  		uid = ctx.request.get['uid']
  		usr = sql_session.query(model.XUser).filter_by(id=uid).first()
  		sql_session.delete(usr)
  		sql_session.commit()
  		return "DONE"

  	return "LIST USERS"


@saucepan.route("/api/<method>/")
class ApiHandler(saucepan.RoutableClass):
	pass


@saucepan.route('/<name>')
def handle_hello(ctx, name=None):
  ctx.response.status_message = "ACK!"
  return "Hello {0:s} !".format(name)


saucepan.run(port=8081)
