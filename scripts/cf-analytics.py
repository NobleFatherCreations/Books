# Cloudflare Web Analytics report. Usage: python3 scripts/cf-analytics.py [start-date YYYY-MM-DD]
# Needs the Cloudflare API token saved as a network secret for api.cloudflare.com (proxy injects it).
import json, subprocess, sys, datetime as dt
A="28e452b024f049d90e3f4550d1881f6c"; S="ff30421a26984c98853ad4ed96b293c4"
def q(query, variables):
    body=json.dumps({"query":query,"variables":variables})
    out=subprocess.run(["curl","-s","https://api.cloudflare.com/client/v4/graphql","-H","Content-Type: application/json","--data-binary","@-"],input=body,capture_output=True,text=True).stdout
    d=json.loads(out)
    if d.get("errors"): print("ERR",d["errors"]); 
    return d
today=dt.date.today()
Q="""query($a:String!,$f:AccountRumPageloadEventsAdaptiveGroupsFilter_InputObject){viewer{accounts(filter:{accountTag:$a}){
 total:rumPageloadEventsAdaptiveGroups(limit:1,filter:$f){count sum{visits}}
 daily:rumPageloadEventsAdaptiveGroups(limit:200,filter:$f,orderBy:[date_ASC]){count sum{visits} dimensions{date}}
 pages:rumPageloadEventsAdaptiveGroups(limit:12,filter:$f,orderBy:[count_DESC]){count dimensions{requestPath}}
 countries:rumPageloadEventsAdaptiveGroups(limit:8,filter:$f,orderBy:[count_DESC]){count dimensions{countryName}}
 refs:rumPageloadEventsAdaptiveGroups(limit:8,filter:$f,orderBy:[count_DESC]){count dimensions{refererHost}}
 dev:rumPageloadEventsAdaptiveGroups(limit:5,filter:$f,orderBy:[count_DESC]){count dimensions{deviceType}}
}}}"""
start=sys.argv[1] if len(sys.argv)>1 else "2026-08-14"
d=q(Q,{"a":A,"f":{"siteTag":S,"date_geq":start,"date_leq":str(today)}})
print(json.dumps(d.get("data"),indent=0)[:6000])
