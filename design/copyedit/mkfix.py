import re,json,subprocess,sys
out=subprocess.run(["python3","/home/user/Books/design/validate-codex-final.py","--all","--complete"],capture_output=True,text=True,cwd="/home/user/Books").stdout
d={e["name"]:e for e in json.load(open("/home/user/Books/content/playbook-data.json"))["codex_completed"]}
items={}; cur=None
for line in out.splitlines():
    m=re.match(r"== (.*?) \[[^\]]+\]",line)
    if m: cur=m.group(1); continue
    m=re.match(r"\s+ERROR ([a-z_.]+): (.*)",line)
    if m and cur:
        f,msg=m.groups(); sub="-"
        if "." in f: f,sub=f.split(".",1)
        e=d[cur]; v=e.get(f); t=v if sub=="-" else (v or {}).get(sub)
        if not isinstance(t,str): print("skip",cur,f,msg[:60]); continue
        items.setdefault(cur,[]).append({"id":"|".join([cur,f,"-",sub]),"field":f,"why":msg,"text":t})
w=[{"entry":n,"about":d[n].get("short_definition",""),"items":i} for n,i in items.items()]
json.dump(w,open(sys.argv[1],"w"),ensure_ascii=False,indent=1)
print(len(w),"entries",sum(len(x["items"]) for x in w),"items")
for x in w:
    for i in x["items"]: print("-",i["id"].split("|")[0],"/",i["field"],"::",i["why"][:110])
