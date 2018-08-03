import requests
from datetime import datetime
import json
import re
import pytz

intz = pytz.timezone('Asia/Kolkata')
nowdt = datetime.now(intz)

d={}
f1=open('output.txt','w+')
f= open("data.txt","a+")
data=f.read()
if len(data)!=0:
    for line in data.split('\n'):
        if len(line)>0 : (key,value)=line.split()
        d[key]=datetime.strptime(value,'%Y%m%d%H%M%S')
f.close()
d1=d.copy()

url = 'https://www.site24x7.com/api/monitors'
headers = {'Authorization': 'Zoho-authtoken 5c9642a1a4b6f93a3fb8c3827211b481' , 'Accept':'application/json; version=2.0'}
r = requests.get(url, headers=headers)

for item in r.json()['data']:
    if item['state']==0:
        url = 'https://www.site24x7.com/api/reports/log_reports/'+item['monitor_id']+'?date='+str(nowdt.date())
        r1 = requests.get(url, headers=headers)
        a = json.dumps(r1.json()['data']['report']).replace('}]','').replace('[{','').split('}, {')
        if a[0]!='[]':
            b = []
            if d.has_key(item['monitor_id'])==False:
                d[item['monitor_id']]= datetime.strptime(datetime.now().date().strftime('%Y%m%d000000'),'%Y%m%d%H%M%S')
            for x in a:
                collection_time=datetime.strptime(''.join(re.search('collection_time\": \"(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)',x).groups()),'%Y%m%d%H%M%S')
                if d[item['monitor_id']] < collection_time:
                    b.append(x)
                    if d1.has_key(item['monitor_id'])==False or d1[item['monitor_id']]<collection_time:
                        d1[item['monitor_id']]=collection_time
            b = [x+', "smartID": "'+item['monitor_id']+'#'+item['display_name']+'"' for x in b]
            if len(b)>0 : f1.write('\n'.join(b).encode('ascii','ignore')+'\n')

if len(d1)==0: d1=d.copy()
f=open('data.txt','w+')
for k,v in d1.items():
    f.write(k+' '+v.strftime('%Y%m%d%H%M%S')+'\n')
f.close()
f1.close()
