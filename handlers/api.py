from flask import Blueprint
from flask import request
from utils.security import verify_quory
import json
from models.models import DB, Api, Key,Authority
import requests

view = Blueprint('api', __name__)


@view.route('/')
@view.route('/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test(**args):
    response=requests.get('http://www.baidu.com')
    return response.content,response.status_code


@view.route('/api', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api():
    if not verify_quory(request):
        return '验证不通过', 400
    dic=request.args.to_dict()
    service=dic.pop('service')
    dic.pop('timestamp')
    dic.pop('signaturenonce')
    keyid=dic.pop('keyid')
    user_id=DB.query(Key).filter(Key.keyid==keyid).first().user_id
    authority=DB.query(Authority).filter(Authority.user_id==user_id).first()
    route=DB.query(Api).filter(Api.id==service).first().route
    if authority.count<1:
        return '没有访问权限',400

    if request.method=='GET':
        requests_=requests.get
    if request.method=='PUT':
        requests_=requests.put
    if request.method=='POST':
        requests_=requests.post
    if request.method=='DELETE':
        requests_=requests.delete

    response=requests_('http://'+route,params=dic)
    print(response.text)

    if int(response.status_code)<400:
        authority.count-=1
    DB.commit()

    return response.text,response.status_code

    # data = DB.query(Templet).filter(Templet.status.in_(args['templet_status'].split(','))).all()
    # host= DB.query(Api),filter(Api.id==)
    # return str(request.json)
