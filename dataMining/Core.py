
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
for i in range(10):
    openfile='pro2/problem_'+str(i)+'.json'
    with open(openfile)as f:
        data=json.load(f)
    out_core_file='pro2/core_'+str(i)+'.json'
    cout_dis_file='pro2/dis_'+str(i)+'.json'
    # with open(out_core_file,'w') as f:
    threshold=50
    ls=[]
    name=[ "id","group","value","domain"]
    for j in range(0,len(data['nodes'])):
        if int(data['nodes'][j]['value'])>threshold:
            newline=[]
            for item in name:
                newline.append(data['nodes'][j][item])
            ls.append(newline)
    fw=open(out_core_file,"w",encoding='utf-8')
    for i in range(0,len(ls)):
        ls[i]=dict(zip(name,ls[i]))
    a = json.dumps(ls[0:],sort_keys=True,indent=4,ensure_ascii=False)
    # print(a)
    fw.write(a)
    fw.close()
def find_center(item):
    openfile='pro2/problem_'+str(item)+'.json'
    with open(openfile)as f:
        wholedata=json.load(f)
    start_time=time.time()
    G = nx.DiGraph()
    UG=nx.Graph()
    # i=0
    for i in range(0,len(wholedata['nodes'])):
        G.add_node(wholedata['nodes'][i]['id'])
        G.nodes[wholedata['nodes'][i]['id']]['value']=wholedata['nodes'][i]['value']
        UG.add_node(wholedata['nodes'][i]['id'])
        UG.nodes[wholedata['nodes'][i]['id']]['value']=wholedata['nodes'][i]['value']
    for i in range(0,len(wholedata['links'])):
        G.add_edge(wholedata['links'][i]['source'],wholedata['links'][i]['target'])
        UG.add_edge(wholedata['links'][i]['source'],wholedata['links'][i]['target'])
        # G.edges[data['links'][i]['source'],data['links'][i]['target']]['value']
    domainlist,valuelist,grouplist,nodelist=[],[],[],[]

    openfile='pro2/data/core'+str(item)+'.json'
    with open(openfile)as f:
        data=json.load(f)
    for i in range(0,len(data['nodes'])):
        nodelist.append(data['nodes'][i]['id'])
        domainlist.append(data['nodes'][i]['domain'])
        grouplist.append(data['nodes'][i]['group'])
        valuelist.append(data['nodes'][i]['value'])
    # for node in G.nodes:
    #     if int(G.nodes[node]['value'])>50 :
    #         # print(str(node))
    #         nodelist.append(node)
            # print(node)
    # print(len(nodelist))
    ls=[]
    newnode=[]
    name=['source','target']
    for i in range(0,len(nodelist)-1):
        for j in range(i+1,len(nodelist)):
            paths_ij=(nx.shortest_path(UG,nodelist[i],nodelist[j]))
            try:
                paths_ij=list(paths_ij)
            except nx.exception.NetworkXNoPath:
                # print("None")
                # continue
                a=1
            else:
                path=paths_ij
                print(path)
                for k in range(0,len(path)-1):
                    if G.has_edge(path[k],path[k+1]):
                        newls=[]
                        newls.append(path[k])
                        newls.append(path[k+1])
                        if newls not in ls: 
                            ls.append(newls)
                    else:
                        newls=[]
                        newls.append(path[k+1])
                        newls.append(path[k])
                        if newls not in ls: 
                            ls.append(newls)
                    if path[k] not in newnode:
                        newnode.append(path[k])

            paths_ij=(nx.shortest_path(UG,nodelist[j],nodelist[i]))
            try:
                paths_ij=list(paths_ij)
            except nx.exception.NetworkXNoPath:
                # print("None")
                # continue
                a=1
            else:
                path=paths_ij
                print(path)
                for k in range(0,len(path)-1):
                    if G.has_edge(path[k],path[k+1]):
                        newls=[]
                        newls.append(path[k])
                        newls.append(path[k+1])
                        if newls not in ls: 
                            ls.append(newls)
                    else:
                        newls=[]
                        newls.append(path[k+1])
                        newls.append(path[k])
                        if newls not in ls: 
                            ls.append(newls)
                    if path[k] not in newnode:
                        newnode.append(path[k])
    allfilename='./pro2_result/core_'+str(item)+'.json'
    with open(allfilename,'w') as f:
        f.write('{\n"links":\n')
        filename='link'+str(item)+'.json'
        fw=open(filename,"w",encoding='utf-8')
        for j in range(0,len(ls)):
            ls[j]=dict(zip(name,ls[j]))
        jsonj = json.dumps(ls[0:],sort_keys=True,indent=4,ensure_ascii=False)
        # print(a)
        fw.write(jsonj)
        fw.close()
        f.write(jsonj)
        f.write(',\n"nodes":')
        newname=['id','group']
        ls=[]
        for k in newnode:
            if k not in nodelist:
                newls=[]
                newls.append(k)
                newls.append(5)
                ls.append(newls)
        for i in range(0,len(data['nodes'])):
            newls=[]
            newls.append(data['nodes'][i]['id'])
            newls.append(data['nodes'][i]['group'])
            ls.append(newls)
            # nodelist.append(data['nodes'][i]['id'])
            # domainlist.append(data['nodes'][i]['domain'])

        nodefilename='node'+str(item)+'.json'
        fw=open(nodefilename,"w",encoding='utf-8')
        for j in range(0,len(ls)):
            ls[j]=dict(zip(newname,ls[j]))
        jsonj = json.dumps(ls[0:],sort_keys=True,indent=4,ensure_ascii=False)
        # print(a)
        fw.write(jsonj)
        f.write(jsonj)
        f.write('\n}')
        fw.close()


            # paths_ij=list(paths_ij)
            # if paths_ij is not None:
            #     for path in paths_ij:
            #         print(path)
            # print

    # with open(Nodefile,"r") as f:
    #     read=csv.reader(f)
    #     # read=next(read)
    #     for row in read:
    #         # print(row)
    #         # if i==0:
    #         #     for j in range(4):
    #         #         print(row[j])
    #         #     i+=1            
    #         # for j in range(4):
    #         #     print(row[j])
    #         #     i+=1
    #         G.add_node(row[0])
    #         G.nodes[row[0]]['name']=row[1]
    #         G.nodes[row[0]]['type']=row[2]
    #         G.nodes[row[0]]['industry']=row[3]
    #         G.nodes[row[0]]['visited']=0
    #         G.nodes[row[0]]['turn']=0
    #         UG.add_node(row[0])
    #         UG.nodes[row[0]]['name']=row[1]
    #         UG.nodes[row[0]]['type']=row[2]
    #         UG.nodes[row[0]]['industry']=row[3]
    #         UG.nodes[row[0]]['visited']=0
    #         UG.nodes[row[0]]['turn']=0
            
    # with open(Linkfile,"r") as f:
    #     read=csv.reader(f)
    #     # read=next(read)
    #     for row in read:
    #         G.add_edge(row[1],row[2])
    #         G.edges[row[1],row[2]]['relation']=row[0]
    #         UG.add_edge(row[1],row[2])
    #         UG.edges[row[1],row[2]]['relation']=row[0]
    #         # if i==1:
    #         #     for j in range(3):
    #         #         print(row[j])
    #         #     i+=1
    # # G.nodes()
    # # print(G.nodes['Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9']['name'])
    # # print(G.nodes['Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9']['type'])
    # # print(G.nodes['Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9']['industry'])
    # # print(G.degree('Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9'))
    # end_time=time.time()
    # print(time.time()-start_time)
    # # max=400
    # search_path=[]
    # node_list=[[]for i in range(max)]
    # # node_list[0]=['Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9','Domain_f3554b666038baffa5814c319d3053ee2c2eb30d31d0ef509a1a463386b69845']
    # node_list[0]=start_node
    # for item in node_list[0]:
    #     print(item)
    # maxx=max
    # for node in node_list[0]:
    #     UG.nodes[node]['visited']=-1
    # for i in range(maxx):
    #     flag=1
    #     if node_list[i] is None:
    #         break
    #     for node in node_list[i]:
    #         if max<=0:
    #             flag=0
    #             break
    #         max-=1
    #         turn=G.nodes[node]['turn']
    #         search_path.append(node)
    #         for neighbor in UG.neighbors(node):
    #             if(UG.nodes[neighbor]['visited']==0):
    #                 UG.nodes[neighbor]['visited']=-1
    #                 G.nodes[neighbor]['turn']=turn+1
    #                 node_list[i+1].append(neighbor)
    #     if flag==0:
    #         break
    # subG=G.subgraph(search_path)
    # print(time.time()-start_time)

    # with open(output_node_file,'w') as f:  
    #     for node in subG.nodes():
    #         f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+','+str(subG.nodes[node]['turn'])+','+str(subG.degree(node))+'\n')
    # with open(output_edge_file,'w')as f:
    #     for node1,node2,data in subG.edges(data=True):
    #         f.write(str(data['relation'])+','+str(node1)+','+str(node2)+','+'\n')
    #         # G.nodes[row[0]]['name']=row[1]
    #         # G.nodes[row[0]]['type']=row[2]
    #         # G.nodes[row[0]]['industry']=row[3]
    # # q=deque()
    # # q.append
    # # print(time.time()-start_time)
    # # strnumber=out_put_nodefile.split('.')[1].split('/')[-1][-1]
    # # with open('')
    # # with open()







    # print(time.time()-start_time)
    # G.add_node('hello')
    # G.add_node('hwerf')
    # G.add_edge('hello','hwerf')
    # plt.figure()
    # pos = nx.spring_layout(subG)
    # nx.draw(subG, pos)
    # plt.savefig(output_image_file)
    # plt.show()
    # print(time.time()-start_time)
    print(item)
if __name__ == "__main__":
    for item in range(10):
        # openfile='graphdata/problem_'+str(i)+'.json'
        find_center(item)