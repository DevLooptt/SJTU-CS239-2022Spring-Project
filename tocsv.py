import pandas as pd
import os
import csv
import json
import networkx as nx

# Filepath
Linkfile="Data/Link.csv"
Nodefile="Data/Node.csv"
path='Data'

G = nx.DiGraph()
with open(Nodefile,"r",encoding='utf-8') as f:
    read=csv.reader(f)
    for row in read:
        G.add_node(row[0])
        G.nodes[row[0]]['name']=row[1]
        G.nodes[row[0]]['type']=row[2]
        G.nodes[row[0]]['industry']=row[3]
with open(Linkfile,"r",encoding='utf-8') as f:
    read=csv.reader(f)
    for row in read:
        G.add_edge(row[1],row[2])
        G.edges[row[1],row[2]]['relation']=row[0]
print('1')
def to_csv(file):
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
                if str(node2)==str(end_edgefile[i]):
                    f.write(str(data['relation'])+','+str(node1)+','+str(node2)+'\n')
                    break



files=os.listdir(path)
for file in files:
    if file.split('.')[-1]=='json':
        print(path+'/'+file)
        to_csv(path+'/'+file)
