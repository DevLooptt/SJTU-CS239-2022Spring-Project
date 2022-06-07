
import pandas as pd
import csv
import networkx as nx
import matplotlib.pyplot as plt
import time
import json
from collections import deque

Linkfile="./data/Link.csv"
Nodefile="./data/Node.csv"

def to_csv(file):
    G = nx.DiGraph()

    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        for row in read:
            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]
    with open(file,'r') as json_obj:
        data=json.load(json_obj)
    nodelist=[]
    for node_item in data['nodes']:
        nodelist.append(node_item['id'])
    subG=G.subgraph(nodelist)
    subG.edges()
    output_node_file=file.split('.')[0]+'_node.csv'
    with open(output_node_file,'w') as f:  
        for node in subG.nodes():
            f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+'\n')
    output_edge_file=file.split('.')[0]+'_edge.csv'
    start_edgefile=[]
    end_edgefile=[]
    for node_item in data['links']:
        start_edgefile.append(node_item['source'])
        end_edgefile.append(node_item['target'])
    
    with open(output_edge_file,'w')as f:
        for i in range(0,len(start_edgefile)):
            # for edges in subG.edges(start_edgefile[i]):
            for node1,node2,data in subG.edges(start_edgefile[i],data=True):
                f.write(str(data['relation'])+','+str(node1)+','+str(node2)+','+'\n')

def find_naive(start_node,output_node_file="newnode.csv",output_edge_file="newedge.csv",output_image_file="edges.png",max=400):
    start_time=time.time()
    G = nx.DiGraph()
    # i=0
    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            G.nodes[row[0]]['visited']=0
            G.nodes[row[0]]['turn']=0
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]

    end_time=time.time()
    print(time.time()-start_time)
    # max=400
    search_path=[]
    node_list=[[]for i in range(max)]
    node_list[0]=start_node
    for item in node_list[0]:
        print(item)
    maxx=max
    for node in node_list[0]:
        G.nodes[node]['visited']=-1
    for i in range(maxx):
        flag=1
        if node_list[i] is None:
            break
        for node in node_list[i]:
            if max<=0:
                flag=0
                break
            max-=1
            turn=G.nodes[node]['turn']
            search_path.append(node)
            for neighbor in G.neighbors(node):
                if(G.nodes[neighbor]['visited']==0):
                    G.nodes[neighbor]['visited']=-1
                    G.nodes[neighbor]['turn']=turn+1
                    node_list[i+1].append(neighbor)
        if flag==0:
            break
    subG=G.subgraph(search_path)
    print(time.time()-start_time)

    with open(output_node_file,'w') as f:  
        for node in subG.nodes():
            f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+','+str(subG.nodes[node]['turn'])+'\n')
    with open(output_edge_file,'w')as f:
        for node1,node2,data in subG.edges(data=True):
            f.write(str(data['relation'])+','+str(node1)+','+str(node2)+','+'\n')

    print(time.time()-start_time)
    plt.figure()
    pos = nx.spring_layout(subG)
    nx.draw(subG, pos)
    plt.savefig(output_image_file)
    print(time.time()-start_time)
def find_naive_undirect(start_node,output_node_file="newnode.csv",output_edge_file="newedge.csv",output_image_file="edges.png",max=400):
    start_time=time.time()
    G = nx.DiGraph()
    UG=nx.Graph()
    # i=0
    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            G.nodes[row[0]]['visited']=0
            G.nodes[row[0]]['turn']=0
            UG.add_node(row[0])
            UG.nodes[row[0]]['name']=row[1]
            UG.nodes[row[0]]['type']=row[2]
            UG.nodes[row[0]]['industry']=row[3]
            UG.nodes[row[0]]['visited']=0
            UG.nodes[row[0]]['turn']=0
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]
            UG.add_edge(row[1],row[2])
            UG.edges[row[1],row[2]]['relation']=row[0]

    end_time=time.time()
    print(time.time()-start_time)
    # max=400
    search_path=[]
    node_list=[[]for i in range(max)]
    node_list[0]=start_node
    for item in node_list[0]:
        print(item)
    maxx=max
    for node in node_list[0]:
        UG.nodes[node]['visited']=-1
    for i in range(maxx):
        flag=1
        if node_list[i] is None:
            break
        for node in node_list[i]:
            if max<=0:
                flag=0
                break
            max-=1
            turn=G.nodes[node]['turn']
            search_path.append(node)
            for neighbor in UG.neighbors(node):
                if(UG.nodes[neighbor]['visited']==0):
                    UG.nodes[neighbor]['visited']=-1
                    G.nodes[neighbor]['turn']=turn+1
                    node_list[i+1].append(neighbor)
        if flag==0:
            break
    subG=G.subgraph(search_path)
    print(time.time()-start_time)

    with open(output_node_file,'w') as f:  
        for node in subG.nodes():
            f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+','+str(subG.nodes[node]['turn'])+'\n')
    with open(output_edge_file,'w')as f:
        for node1,node2,data in subG.edges(data=True):
            f.write(str(data['relation'])+','+str(node1)+','+str(node2)+'\n')


    print(time.time()-start_time)

    plt.figure()
    pos = nx.spring_layout(subG)
    nx.draw(subG, pos)
    plt.savefig(output_image_file)
    # plt.show()
    print(time.time()-start_time)
def find_naive_undirect_plus(start_node,output_node_file="newnode.csv",output_edge_file="newedge.csv",output_image_file="edges.png",max=400):
    start_time=time.time()
    G = nx.DiGraph()
    UG=nx.Graph()
    # i=0
    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
    
            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            G.nodes[row[0]]['visited']=0
            G.nodes[row[0]]['turn']=0
            UG.add_node(row[0])
            UG.nodes[row[0]]['name']=row[1]
            UG.nodes[row[0]]['type']=row[2]
            UG.nodes[row[0]]['industry']=row[3]
            UG.nodes[row[0]]['visited']=0
            UG.nodes[row[0]]['turn']=0
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]
            UG.add_edge(row[1],row[2])
            UG.edges[row[1],row[2]]['relation']=row[0]
           
    end_time=time.time()
    print(time.time()-start_time)
    # max=400
    search_path=[]
    node_list=[[]for i in range(max)]
    node_list[0]=start_node
    for item in node_list[0]:
        print(item)
    maxx=max
    for node in node_list[0]:
        UG.nodes[node]['visited']=-1
    for i in range(maxx):
        flag=1
        if node_list[i] is None:
            break
        for node in node_list[i]:
            if max<=0:
                flag=0
                break
            max-=1
            turn=G.nodes[node]['turn']
            search_path.append(node)
            for neighbor in UG.neighbors(node):
                if(UG.nodes[neighbor]['visited']==0):
                    UG.nodes[neighbor]['visited']=-1
                    G.nodes[neighbor]['turn']=turn+1
                    node_list[i+1].append(neighbor)
        if flag==0:
            break
    subG=G.subgraph(search_path)
    print(time.time()-start_time)

    with open(output_node_file,'w') as f:  
        for node in subG.nodes():
            f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+','+str(subG.nodes[node]['turn'])+','+str(subG.degree(node))+'\n')
    with open(output_edge_file,'w')as f:
        for node1,node2,data in subG.edges(data=True):
            f.write(str(data['relation'])+','+str(node1)+','+str(node2)+','+'\n')
    print(time.time()-start_time)
def find_naive_undirect_plus_p(start_node,output_node_file="newnode.csv",output_edge_file="newedge.csv",output_image_file="edges.png",max=400):
    start_time=time.time()
    G = nx.DiGraph()
    UG=nx.Graph()
    # i=0
    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:

            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            G.nodes[row[0]]['visited']=0
            G.nodes[row[0]]['turn']=0
            UG.add_node(row[0])
            UG.nodes[row[0]]['name']=row[1]
            UG.nodes[row[0]]['type']=row[2]
            UG.nodes[row[0]]['industry']=row[3]
            UG.nodes[row[0]]['visited']=0
            UG.nodes[row[0]]['turn']=0
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]
            UG.add_edge(row[1],row[2])
            UG.edges[row[1],row[2]]['relation']=row[0]

    end_time=time.time()
    print(time.time()-start_time)
    # max=400
    search_path=[]
    node_list=[[]for i in range(max)]
    
    node_list[0]=start_node
    for item in node_list[0]:
        print(item)
    maxx=4
    for node in node_list[0]:
        UG.nodes[node]['visited']=-1
    for i in range(maxx):
        flag=1
        if node_list[i] is None:
            break
        for node in node_list[i]:
            # if max<=0:
            #     flag=0
            #     break
            # max-=1
            turn=G.nodes[node]['turn']
            search_path.append(node)
            for neighbor in UG.neighbors(node):
                if(UG.nodes[neighbor]['visited']==0):
                    UG.nodes[neighbor]['visited']=-1
                    G.nodes[neighbor]['turn']=turn+1
                    node_list[i+1].append(neighbor)
        # if flag==0:
        #     break
    node_path=[]
    subtmpG=G.subgraph(search_path)
    for node in search_path:
        if int(subtmpG.degree(node))>=5:
            node_path.append(node)
            
    subG=G.subgraph(node_path)
    print(time.time()-start_time)

    with open(output_node_file,'w') as f:  
        for node in subG.nodes():
            f.write(str(node)+','+str(subG.nodes[node]['name'])+','+str(subG.nodes[node]['type'])+','+str(subG.nodes[node]['industry'])+','+str(subG.nodes[node]['turn'])+','+str(subG.degree(node))+'\n')
    with open(output_edge_file,'w')as f:
        for node1,node2,data in subG.edges(data=True):
            f.write(str(data['relation'])+','+str(node1)+','+str(node2)+','+'\n')
    
    print(time.time()-start_time)
def find_useful_node():
    start_time=time.time()
    G = nx.DiGraph()
    UG=nx.Graph()
    # i=0
    with open(Nodefile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
       
            G.add_node(row[0])
            G.nodes[row[0]]['name']=row[1]
            G.nodes[row[0]]['type']=row[2]
            G.nodes[row[0]]['industry']=row[3]
            G.nodes[row[0]]['visited']=0
            G.nodes[row[0]]['turn']=0
            UG.add_node(row[0])
            UG.nodes[row[0]]['name']=row[1]
            UG.nodes[row[0]]['type']=row[2]
            UG.nodes[row[0]]['industry']=row[3]
            UG.nodes[row[0]]['visited']=0
            UG.nodes[row[0]]['turn']=0
            
    with open(Linkfile,"r") as f:
        read=csv.reader(f)
        # read=next(read)
        for row in read:
            G.add_edge(row[1],row[2])
            G.edges[row[1],row[2]]['relation']=row[0]
            UG.add_edge(row[1],row[2])
            UG.edges[row[1],row[2]]['relation']=row[0]
    with open('mynode','w') as f:
        for node in UG.nodes():
            if UG.degree(node)>100:
                f.write(str(node)+','+str(UG.degree(node))+'\n')

if __name__ == "__main__":
    
    start=[[]for i in range(5)]
    start[0]=['Domain_c58c149eec59bb14b0c102a0f303d4c20366926b5c3206555d2937474124beb9','Domain_f3554b666038baffa5814c319d3053ee2c2eb30d31d0ef509a1a463386b69845']
    start[1]=['IP_400c19e584976ff2a35950659d4d148a3d146f1b71692468132b849b0eb8702c','Domain_b10f98a9b53806ccd3a5ee45676c7c09366545c5b12aa96955cde3953e7ad058']
    start[2]=['Domain_24acfd52f9ceb424d4a2643a832638ce1673b8689fa952d9010dd44949e6b1d9','Domain_9c72287c3f9bb38cb0186acf37b7054442b75ac32324dfd245aed46a03026de1','Domain_717aa5778731a1f4d6f0218dd3a27b114c839213b4af781427ac1e22dc9a7dea','Domain_8748687a61811032f0ed1dcdb57e01efef9983a6d9c236b82997b07477e66177','Whois_Phone_f4a84443fb72da27731660695dd00877e8ce25b264ec418504fface62cdcbbd7']
    start[3]=['IP_7e730b193c2496fc908086e8c44fc2dbbf7766e599fabde86a4bcb6afdaad66e','Cert_6724539e5c0851f37dcf91b7ac85cb35fcd9f8ba4df0107332c308aa53d63bdb']
    start[4]=['Whois_Phone_fd0a3f6712ff520edae7e554cb6dfb4bdd2af1e4a97a39ed9357b31b6888b4af','IP_21ce145cae6730a99300bf677b83bbe430cc0ec957047172e73659372f0031b8','Domain_7939d01c5b99c39d2a0f2b418f6060b917804e60c15309811ef4059257c0818a','Domain_587da0bac152713947db682a5443ef639e35f77a3b59e246e8a07c5eccae67e5']
    max=[400,800,800,3000,3000]
    
    for i in range(5):
        out_put_nodefile='./naive_undirect_plus/node'+str(i)+'.csv'
        out_put_edgefile='./naive_undirect_plus/edge'+str(i)+'.csv'
        out_put_imagefile='./naive_undirect_plus/image'+str(i)+'.png'
        find_naive_undirect_plus(start_node=start[i],output_node_file=out_put_nodefile,output_edge_file=out_put_edgefile,output_image_file=out_put_imagefile,max=max[i])

    
