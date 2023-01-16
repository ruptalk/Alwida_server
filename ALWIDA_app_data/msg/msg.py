import datetime
from flask import Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import terminal_table, container_table, reservation_table, chatting_table, message_table, db

blue_msg = Blueprint("msg", __name__, url_prefix="/msg")

@blue_msg.route("/info", methods=["POST"])
def info():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                container_num = reservation_table.query.filter(reservation_table.id==id).first().container_num
                container = container_table.query.filter(container_table.container_num == container_num).first()
                terminal = terminal_table.query.filter(terminal_table.tn==container.tn).first()
                
                data = {
                    "terminalName":terminal.name,
                    "terminalAbb":container.tn,
                    "scale":container.scale,
                    "deviceLocation":container.position,
                    "containerNum":container.container_num
                }
                
                return data
            except:
                return jsonify({'result':False}) 
        else:
            return jsonify({'result':'error'})

@blue_msg.route("/congestion", methods=["POST"])
def congestion():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                now = datetime.datetime.now()
                new_msg = message_table(id=id, message="목적지 혼잡도를 알려주세요.", time=now, sender=True)
                db.session.add(new_msg)
                db.session.commit()
                
                tn = reservation_table.query.filter(reservation_table.id==id).first().tn
                terminal = terminal_table.query.filter(terminal_table.tn==tn).first()
                            
                if(terminal.car_amount < terminal.easy):
                    state = "원활"
                elif(terminal.car_amount < terminal.normal):
                    state = "보통"
                else:
                    state = "혼잡"

                time = now.strftime('%Y-%m-%d %H:%M')

                msg = f"목적지 혼잡도\n{tn} 터미널\n혼잡도: {state}\n{time} 기준"
                new_msg = message_table(id=id, message=msg, time=now, sender=False)
                db.session.add(new_msg)
                db.session.commit()
                    
                data = {
                    "description":msg,
                    "hour":now.hour,
                    "min":now.minute
                }
                return data
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 

@blue_msg.route("/numOfCar", methods=["POST"])
def numOfCar():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                now = datetime.datetime.now()
                new_msg = message_table(id=id, message="부두 내 차량 현황을알려주세요.", time=now, sender=True)
                db.session.add(new_msg)
                db.session.commit()
                            
                tn = reservation_table.query.filter(reservation_table.id==id).first().tn
                terminal = terminal_table.query.filter(terminal_table.tn==tn).first()
                        
                time = now.strftime('%Y-%m-%d %H:%M')
                msg = f"부두 내 차량 현황\n{terminal.car_amount}\n{time}"
                new_msg = message_table(id=id, message=msg, time=now, sender=False)
                db.session.add(new_msg)
                db.session.commit()
                        
                data = {
                    "description":msg,
                    "hour":now.hour,
                    "min":now.minute
                }
                return data
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 

@blue_msg.route("/resChange", methods=["POST"])
def resChange():
    if(request.method == "POST"):
        id = request.form.get("id","")
        hour = request.form.get("hour","")
        min = request.form.get("min","")
        if(id != "" and hour != ""and min != ""):
            try:
                now = datetime.datetime.now()
                reservation = reservation_table.query.filter(reservation_table.id==id).first()
                time = datetime.datetime(now.year,now.month,now.day,int(hour),int(min),0)
                reservation.accept_time = time
                msg = f"예약 변경 요청 완료"
                new_msg = message_table(id=id, message=msg, time=now, sender=False)
                new_chat = chatting_table(id=id, state=3)
                db.session.add(new_msg)
                db.session.add(new_chat)
                db.session.commit()
                            
                data = {
                    "description":msg,
                    "hour":now.hour,
                    "min":now.minute
                }
                return data
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 

@blue_msg.route("/departCancle", methods=["POST"])
def departCancle():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                now = datetime.datetime.now()
                msg = "출발 취소 요청"
                new_msg = message_table(id=id, message=msg, time=now, sender=True)
                new_chat = chatting_table(id=id, state=4)
                db.session.add(new_msg)
                db.session.add(new_chat)
                db.session.commit()
                
                return jsonify({'result':True})
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 

@blue_msg.route("/entryRequest", methods=["POST"])
def entryRequest():
    if(request.method == "POST"):
        id = request.form.get("id","")
        try:
            now = datetime.datetime.now()
            msg = "게이트 진입요청"
            new_msg = message_table(id=id, message=msg, time=now, sender=True)
            new_chat = chatting_table(id=id, state=5)
            db.session.add(new_msg)
            db.session.add(new_chat)
            db.session.commit()
            
            return jsonify({'result':True})
        except:
            return jsonify({'result':False})
    else:
        return jsonify({'result':'error'}) 

@blue_msg.route("/coordinate", methods=["POST"])
def coordinate():
    if(request.method == "POST"):
        id = request.form.get("id","")
        if(id != ""):
            try:
                tn = reservation_table.query.filter(reservation_table.id==id).first().tn
                terminal = terminal_table.query.filter(terminal_table.tn==tn).first()
                
                data = {
                    'longitude':terminal.longitude,
                    'latitude':terminal.latitude
                }
                
                return data
            except:
                return jsonify({'result':False})
        else:
            return jsonify({'result':'error'}) 