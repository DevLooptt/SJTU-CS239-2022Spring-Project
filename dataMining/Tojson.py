import json
name=[ "id","group"]
for i in range(5):
    file='node'+str(i)+'.csv'
    f=open(file,"r",encoding='gbk') #
    ls=[]
    for line in f:
        line = line.replace("\n", "")
        newline=line.split(',')
        # newline.pop()
        line=[]
        line.append(newline[0])

        if newline[2]=='Domain' or newline[2]=='IP' or newline[2]=='Cert':
            line.append(3)
        elif newline[2]=='Whois_Name' or newline[2]=='Whois_Email' or newline[2]=='Whois_Phone':
            line.append(2)
        else:
            line.append(1)
        ls.append(line)
    f.close()
    fw=open(file.split('.')[0]+'.json',"w",encoding='utf-8')
    for i in range(0,len(ls)):
        ls[i]=dict(zip(name,ls[i]))
    a = json.dumps(ls[0:],sort_keys=True,indent=4,ensure_ascii=False)
    # print(a)
    fw.write(a)
    fw.close()
name=[ "value","source", "target"]
for i in range(5):
    file='edge'+str(i)+'.csv'
    f=open(file,"r",encoding='gbk') #
    ls=[]
    for line in f:
        line = line.replace("\n", "")
        newline=line.split(',')
        newline.pop()
        if newline[0]=='r_cert' or newline[0]=='r_subdomain' or newline[0]=='r_request_jump' or newline[0]=='r_dns_a':
            newline[0]=4
        elif newline[0]=='r_whois_name' or newline[0]=='r_whois_email' or newline[0]=='r_whois_phon':
            newline[0]=3
        elif newline[0]=='r_cert_chain' or newline[0]=='r_cname':
            newline[0]=2
        else:
            newline[0]=1
        ls.append(newline)
    f.close()
    fw=open(file.split('.')[0]+'.json',"w",encoding='utf-8')
    for i in range(0,len(ls)):
        ls[i]=dict(zip(name,ls[i]))
    a = json.dumps(ls[0:],sort_keys=True,indent=4,ensure_ascii=False)
    # print(a)
    fw.write(a)
    fw.close()
for i in range(5):
    filename='problem_'+str(i)+'.json'
    nodefile=open('node'+str(i)+'.json', 'r',encoding='utf-8')
    edgefile=open('edge'+str(i)+'.json', 'r',encoding='utf-8')
    nodecontent=nodefile.read()
    edfecontent=edgefile.read()
    with open(filename,'w') as f:
        f.write('{\n')
        f.write('"nodes":')
        f.write(nodecontent)
        f.write(',\n')
        f.write('"links":')
        f.write(edfecontent)
        f.write('\n}')
    nodefile.close()
    edgefile.close()
