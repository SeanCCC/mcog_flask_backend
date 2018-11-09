from flask import Flask, request
from flask_pymongo import PyMongo
import time, json, datetime

app = Flask(__name__)

# MongoDB collections: 
#   For Garmin API: dailies, activities, manually_updated_activities, epochs, sleeps, body_compositions, 
#                   third_party_dailies, stress, user_metrics, moveIQ, pulse_ox
#   For DMS APP: tracking, lastpos, tripdump, devicedump, surveydump, servicecheck
app.config["MONGO_URI"] = "mongodb://localhost:27017/mcog"
mongo = PyMongo(app)

# APP dump new device information
@app.route('/devicedump', methods=['POST'])
def devicedump():
    dumpdata = request.get_json(force=True, silent=True)
    try:
        dumpdata['servertime'] = int(time.time())
        mongo.db.devicedump.insert(dumpdata)
    except Exception as e:
        print ('/devicedump', e, dumpdata)
    endtime = {'lastinsert':int(dumpdata['endtime'])}
    return json.dumps(endtime)

# APP dump new trip record
@app.route('/tripdump', methods=['POST'])
def tripdump():
    dumpdata = request.get_json(force=True, silent=True)
    try:
        dumpdata['servertime'] = int(time.time())
        mongo.db.tripdump.insert(dumpdata)
    except Exception as e:
        print ('/tripdump', e, dumpdata)
    endtime = {'lastinsert':int(dumpdata['endtime'])}
    return json.dumps(endtime)

# APP dump new survey status
@app.route('/surveydump', methods=['POST'])
def surveydump():
    dumpdata = request.get_json(force=True, silent=True)
    try:
        dumpdata['servertime'] = int(time.time())
        mongo.db.surveydump.insert(dumpdata)
    except Exception as e:
        print ('/surveydump', e, dumpdata)
    endtime = {'lastinsert':dumpdata['triggerTime']}
    return json.dumps(endtime)

# Get last service's information and total count for the requested "deviceid", "email", and "userid"
@app.route('/servicerec', methods=['POST'])
def servicerec():
    dumpdata = request.get_json(force=True, silent=True)
    try:
        deviceidnum = int(dumpdata['deviceid']) if dumpdata['deviceid'] else 9999
        email = dumpdata['email'] if dumpdata['email'] else "NO EMAIL PROVIDED"
        userid = dumpdata['userid'] if dumpdata['userid'] else "NOT PROVIDED"
    except Exception as e:
        print ('/servicerec', e, dumpdata)
    # Calculate midnight epoch time
    midnight = int(time.mktime(datetime.date.today().timetuple()))+86400
    midnightstr = str(datetime.datetime.fromtimestamp(midnight))
    
    # Check last service
    idcheck = mongo.db.servicecheck.find({"userid": userid}, {'_id': False}).sort("ts",1)
    firsttsdt = datetime.datetime.fromtimestamp(idcheck[0]['ts'])
    midnightfirsttsdt = datetime.datetime.fromtimestamp(idcheck[0]['startmidnight'])
    startmidnight = idcheck[0]['startmidnight']
    nowtime = int(time.time())
    nowtssdt = datetime.datetime.fromtimestamp(nowtime)
    numofdays = (nowtssdt - midnightfirsttsdt).days
    hourssincesurveystart = (nowtime - startmidnight)/3600
    midnightstr = idcheck[0]['startmidnightstr']
    
    hourssincesurveystart = float("{:.2f}".format(hourssincesurveystart))

    # Check if they have recorded any checkins already
    isfirstrec = mongo.db.servicecheck.find({"email":email})
    sreccount = isfirstrec.count()

    servicedictout = {
        "deviceid":deviceidnum, "email":email, 'userid':userid, 'currentcheckin':nowtime,
        'firstcheckin':str(firsttsdt), 'currentcheckinstr':str(nowtssdt), 'daysinsurvey':numofdays,'midnightstart':startmidnight, 'surveyrunninghours': hourssincesurveystart,
        'startmidnightstr':midnightstr, 'numrecs':sreccount
    }

    return json.dumps(servicedictout)

# Get "not_checked_in" and "checked_in" for the requested "userid".
@app.route('/servicecheck', methods=['POST'])
def servicecheck():
    ts = int(time.time())
    dumpdata = request.get_json(force=True, silent=True)

    try:
        starttime = int(dumpdata['starttime'])*3600 if dumpdata['starttime'] else ts-86400
        hours1 = 86400 if dumpdata['last'] else int(starttime)*3600
        hours2 = 0 if dumpdata['last'] else int(dumpdata['endtime'])*3600
    except Exception as e:
        print ('/servicecheck', e, dumpdata)

    # Get notcheckedin
    hours1ts = ts - hours1
    hours2ts = ts - hours2
    hours1query = mongo.db.servicecheck.find({"ts": {"$gte": hours1ts}}, {'_id': False})
    hours2query = mongo.db.servicecheck.find({"ts": {"$gte": hours2ts}}, {'_id': False})
    templist = list()
    for i in set(hours1query) - set(hours2query):
        templist.append({'userid':i})	
    notcheckedin = {'last_'+str(int(hours2/3600))+"_hours": templist if templist else "All Checked In"}
    
    # Get checkedinlist
    if dumpdata['deviceid']:
        checkedinlist = servicecheck.aggregate([ 
            { '$match': {'$and': [{'userid':int(dumpdata['deviceid'])}, {'ts': {'$gte': hours1ts  }}]}},  
            {"$group": { 
                "_id": '$deviceid', 
                "email":{"$first": "$email"},
                'timestamps': { '$push':  '$ts'},
                'count': { "$sum": 1}
            }}
        ])
    else: 
        checkedinlist = servicecheck.aggregate([ 
            { '$match': {'ts': {'$gte': hours1ts  }}},  
            {"$group": { 
                "_id": '$userid', 
                'deviceid': {"$first":"$deviceid"},
                'timestamps': { '$push':  '$ts'},
                'count': { "$sum": 1}
            }}
        ])
    for i in checkedinlist:
        i['datetimes'] = [ str(datetime.datetime.fromtimestamp(j)) for j in i['timestamps'] ]
    
    return json.dumps( {'not_checked_in': notcheckedin,'checked_in': checkedinlist} )

# Get the last "trip" and "device" information for the requested "userid".
@app.route('/trip_device', methods=['POST'])
def gettripdevice():
    dumpdata = request.get_json(force=True, silent=True)
    if dumpdata['userid']: 
        userid = dumpdata['userid']
        # tripdict
        tripdict = mongo.db.tripdump.find({"userid":userid},{'_id': False})
        tdcount = tripdict.count()
        td = tripdict[tdcount-1] if tdcount > 0 else {"Warning":"NOTICE - no trips have been dumped by userid "+str(userid)}
        # devicedict
        devicedict = mongo.db.devicedump.find({"userid":userid},{'_id': False})
        ddcount = devicedict.count() 
        dd = devicedict[ddcount-1] if ddcount > 0 else {"Warning":"NOTICE - no device information has been dumped by userid "+str(userid)}
    else:   
        td = {"WARNING": "No user provided"}
        dd = {"WARNING": "No user provided"}
    outlist = [{'trip_last_doc': td,'device_last_doc':dd}]

    return json.dumps(outlist)

# Show all of the last insert "survey" and "trip" from each devices.
@app.route('/lastinsert', methods=['GET'])
def lastinsert2():
    devices = mongo.db.devicedump.aggregate([ 
        {"$sort":  {"EndTime":1}} , 
        {"$group": { "_id": "$userid","email":{"$last": "$email"},"ddcount": {"$sum":1}, "lastdevice": {"$last": "$EndTime"}}}
    ])
    surveys = mongo.db.surveydump.aggregate([ 
        {"$sort":  {"clickedtime":1}} , 
        {"$group": { "_id": "$userid", "lastsurvey": {"$last": "$clickedtime"}}}
    ])
    trips = mongo.db.tripdump.aggregate([ 
        {"$sort":  {"EndTime":1}} , 
        {"$group": { "_id": "$userid", "lasttrip": {"$last": "$EndTime"}}}
    ])
    nowtime = int(time.time())

    for i in devices:
        # Set ddcount and lastdevicestr
        i['ddpercent'] = float("{:.2f}".format((i["ddcount"]/336))) if i['lastdevice'] and i['ddcount'] else "NA"
        i['lastdevicestr'] = str(datetime.datetime.fromtimestamp(i['lastdevice'])) if i['ddpercent'] else None
        i['ddhours'] = int((nowtime-i['lastdevice'])/3600)
        # Update with surveys
        for j in surveys:
            if i['_id'] == j['_id']:
                if j['lastsurvey']:
                    lastsurvey = int(j['lastsurvey'])  
                    i['lastsd'] = int(lastsurvey/1000)
                    i['sdhours'] = int(int(nowtime-(lastsurvey/1000))/3600)
                else:
                    lastsurvey = "NA"
                    i['lastsd'] = "NA"
                    i['sdhours'] = "NA"
                break
        for k in trips:
            if i['_id'] == k['_id']:
                i['lasttrip'] = k['lasttrip']
                i['tdhours'] = int((nowtime - int(k['lasttrip']))/3600)
                break
    return json.dumps(devices)

# Show all surveys (?)
@app.route('/surveycompletion', methods=['GET'])
def surveycompletion():
    surveys = mongo.db.surveydump.aggregate([
        { "$group": { 
            "_id": {"user":"$userid","day":"$d"},
            "ct": {"$sum": 1},
            'clicked': {"$sum": { "$cond": [{ "$eq":["$completeType",'complete']},1,0]}},
            "notclicked": {"$sum": { "$cond": [ {"$eq" : ["$completeType",'incomplete']},1,0]}},
            "error":{"$sum": { "$cond": [ {"$eq" : ["$completeType",'error']},1,0]}}
        }}, 
        { "$sort": {"_id":1} }
    ])
    for i in surveys:
        i['completeper'] =  float("{:.2f}".format((i["clicked"]/i["ct"])*100)) if i["clicked"] and i["ct"] else "NA"
    return json.dumps(surveys)

# Show all trips (?)
@app.route('/tripcompletion', methods=['GET'])
def tripcompletion():
    trips = mongo.db.tripdump.aggregate([
        {"$group": {
            "_id": {"user":"$userid","day":"$d"},
            "ct": {"$sum": 1},
            'complete': {"$sum": { "$cond": [{ "$eq":["$completeOrNot",'complete']},1,0]}},
            "incomplete": {"$sum": { "$cond": [ {"$eq" : ["$completeOrNot",'incomplete']},1,0]}}
        }},
        {"$sort": {"_id":1}}
    ])
    for i in trips:
        i['completeper'] =  float("{:.2f}".format((i["clicked"]/i["ct"])*100)) if i["clicked"] and i["ct"] else "NA"
    return json.dumps(trips)

# Show the last login "email" for the requested "userid"
@app.route('/useridcheck', methods=['POST'])
def useridcheck():
    dumpdata = request.get_json(force=True, silent=True)
    userid = dumpdata['userid']
    if userid:
        services = mongo.db.servicecheck.find({'userid':userid}).sort("ts",1) 
        if services.count() > 0:
            email = services[0]['email']
            return json.dumps({'userid':userid, 'email':email})
    return json.dumps({'userid':'no userid provided','email':'NA'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
