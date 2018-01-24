import flask
from gevent import  monkey
from gevent import pywsgi
import os

monkey.patch_all()


app = flask.Flask(__name__)

#...................................................................................
#所有行应函数必须放在handlers下面,而且Blueprint的名称必须为flask_view,而且flask_view不能被替换,而且handlers目录下面新建的文件名不能以'_'开头
handlers=[i[:-3] for i in os.listdir('handlers') if i[0]!='_']
for i in handlers:
    exec('from handlers.%s import flask_view\rapp.register_blueprint(flask_view)'%(i))
#...................................................................................

if __name__ == '__main__':
    # run our standalone gevent server
    # server = pywsgi.WSGIServer(('127.0.0.1', 6679), app)
    # server.serve_forever()
    app.run(port=6679,debug=True)