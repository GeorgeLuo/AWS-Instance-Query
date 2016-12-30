from flask import Flask,render_template,jsonify,json,request,Response
import boto3
import boto.ec2
import pymongo
from pymongo import MongoClient

application = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.aws_search
query_results = db.query_results

ec2 = boto3.client('ec2', region_name='us-west-2')
regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]

def saveQuery(query):
    query_results.delete_many({})
    query_results.insert_one(query)

@application.route("/makeQuery",methods=['POST'])
def makeQuery():
    try:
        print("query made...")
        regions = request.json['regions']
        secret_id = request.json['secret_id']
        access_key = request.json['access_key']
        region_to_instance = {}
        for region in regions:
            if regions[region]:
                ec2conn = boto.ec2.connect_to_region(region, aws_access_key_id=secret_id, aws_secret_access_key=access_key)
                query_res = ec2conn.get_all_instances()
                instances = [i for r in query_res for i in r.instances]
                instance_data = {}
                for i in instances:
                    instance_data[i.id] = {'public_dns_name':i.public_dns_name, 'image_id':i.image_id, 'key_name':i.key_name, '_state':str(i._state)}
                if len(instance_data) != 0:
                    region_to_instance[region] = instance_data
        response_pack = {}
        response_pack['message'] = 'Success: results added to table'
        response_pack['results'] = region_to_instance
        saveQuery(region_to_instance)
        region_to_instance.pop('_id')
        return Response(response=json.dumps(response_pack), status='201',mimetype="application/json")

    except Exception,e:
        print (e)
        return jsonify(status='ERROR',message="Error: check credentials")

@application.route('/')
def genTables():
    return render_template('list.html')

@application.route("/getRegions",methods=['POST'])
def getRegions():
    regions = [region['RegionName'] for region in ec2.describe_regions()['Regions']]
    return json.dumps(regions)

@application.route("/initializeQuery",methods=['POST'])
def initializeQuery():
    print ('generating persisted data...')
    query = query_results.find_one()
    query.pop('_id')
    return jsonify(results=query)

if __name__ == "__main__":
    application.run(host='0.0.0.0')

