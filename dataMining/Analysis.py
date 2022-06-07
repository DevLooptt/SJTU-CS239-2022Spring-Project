import json
for i in range(10):
    openfile='graphdata/problem_'+str(i)+'.json'
    with open(openfile)as f:
        data=json.load(f)
    out_core_file='graphdata/core_'+str(i)+'.json'
    cout_dis_file='graphdata/dis_'+str(i)+'.json'
    # with open(out_core_file,'w') as f:
    with open(cout_dis_file, 'w', encoding="utf-8") as f:
        f.write('{\n')
        f.write('"nodes": [\n')
        number=[0 for k in range(9)]
        for k in range(0,len(data['nodes'])):
            # print(data['nodes'][k]["domain"])
            if data['nodes'][k]["domain"]!='' and data['nodes'][k]["domain"]!='hoi':
                # print(data['nodes'][k]["domain"])
                number[int(ord(data['nodes'][k]["domain"][1])-ord('A'))]+=1
        # f.write()
        f.write('{"name": "涉黄","value":'+str(number[0])+'},\n')

        f.write('{"name": "涉赌","value":'+str(number[1])+'},\n')


        f.write('{"name": "涉骗","value":'+str(number[2])+'},\n')
        f.write('{"name": "涉毒","value":'+str(number[3])+'},\n')
        f.write('{"name": "涉枪","value":'+str(number[4])+'},\n')
        f.write('{"name": "黑客","value":' +str(number[5])+'},\n')
        f.write('{"name": "非法交易平台","value":'+str(number[6])+'},\n')
        f.write('{"name": "非法支付平台","value":' +str(number[7])+'},\n')
        f.write('{"name": "其它","value":' +str(number[8])+'}\n')
        f.write('],\n')
        totaldomain=0
        for item in number:
            totaldomain+=item
        f.write('"totalnodes":'+str(len(data['nodes']))+',\n')
        f.write('"totaldomain":'+str(totaldomain)+',\n')
        f.write('"all":['+'\n')
        name_number=[0 for i in range(6)]
        for k in range(0,len(data['nodes'])):
            # print(data['nodes'][k]["domain"])
            if data['nodes'][k]["id"][0:6]=='Domain':
                # print(data['nodes'][k]["domain"])
                name_number[2]+=1
            elif data['nodes'][k]["id"][0:4]=='Cert':
                name_number[1]+=1
            elif data['nodes'][k]["id"][0:5]=='Whois':
                name_number[3]+=1
            elif data['nodes'][k]["id"][0:4]=='IP_C':
                name_number[4]+=1
            elif data['nodes'][k]["id"][0:3]=='ASN':
                name_number[5]+=1
            else:
                name_number[0]+=1
        f.write('{"name": "IP","value": '+str(name_number[0])+'},\n')
        f.write('{"name": "Cert","value":'+str(name_number[1])+'},\n')
        f.write('{"name": "Domain","value": '+str(name_number[2])+'},\n')
        f.write('{"name": "Whois","value": '+str(name_number[3])+'},\n')
        f.write('{"name": "IP_C","value":'+str(name_number[4])+'},\n')
        f.write('{"name": "ASN","value": '+str(name_number[5])+'}\n')
        f.write(']\n')
        f.write('}')
