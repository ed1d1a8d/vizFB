
import facebook
import json
import tulip_facebook
import time
import sys
#import mutuality
from tulip import *


#fql_query="SELECT post_id FROM stream WHERE source_id = me()"
#query=[{"method":"GET", "relative_url":"me"},{"method":"GET", "relative_url":"me/friends?limit=50"}]
#payload = {"batch": query, "access_token": token}
#r = requests.post("https://graph.facebook.com/", params=payload)
#print r.url

start=time.clock()
global noN
global noE
global name
global picSquare


def gen_graph(graph, token, complete=False):                            #This gets all the info needed
    global noN
    global noE
    global name
    global picSquare

    noN=0
    noE=0
    fbGraph = facebook.GraphAPI(token)
    
    alist={}
    
    viewColor = graph.getColorProperty("viewColor")
    viewBorderColor = graph.getColorProperty("viewBorderColor")
    viewShape = graph.getIntegerProperty("viewShape")
    viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
    viewLayout = graph.getLayoutProperty("viewLayout")
    viewSize = graph.getSizeProperty("viewSize")
    viewMetric = graph.getDoubleProperty("viewMetric")
    picSquare={}
    
    name={}
    comMap={}

    userId="100000186340290"
    mutualFriendEdges=[]
    ans=0
    fMap={}
    
    #----------Get Node Info---------------------------#
    uInf=fbGraph.fql("SELECT uid, pic_square, name FROM user WHERE uid=me() OR uid IN (SELECT uid2 FROM friend WHERE uid1 = me())" )
    #print len(uInf)
    for i in uInf:
        uid=str(i["uid"])
        comMap[uid]={}
        #print uid, i["name"]
        alist[uid]={}
        curN=graph.addNode()
        fMap[uid]=curN
        name[curN.id] = i["name"].encode("UTF-8", "replace")
        #print curN.id, name[1]
        #print name[uid]
        picSquare[curN.id]=i["pic_square"]

    #-----------Get Mutual Friends------------------------#
    for i in range(0, 5):
        fqlQuery={}
        for j in range(i*50, min((i+1)*50, len(uInf))):
            fqlQuery[str(uInf[j]["uid"])]=("select uid1,uid2 from friend where uid1=\"" + str(uInf[j]["uid"]) +
                                               "\" and uid2 in (select uid2 from friend where uid1=me())")
        t=fbGraph.fql(fqlQuery)
        #print t[2]
        for j in t:
            #print j
            for k in j["fql_result_set"]:
                uid1=str(k["uid1"])
                uid2=str(k["uid2"])
                comMap[uid1][uid2]=0
                comMap[uid2][uid1]=0
                node1=fMap[k["uid1"].encode("UTF-8", "replace")]
                node2=fMap[k["uid2"].encode("UTF-8", "replace")]
                if not graph.existEdge(node1, node2, False).isValid():
                    #print "hi"
                    graph.addEdge(node1, node2)
    #----Get Likes/Comments/Tags----------------------------------------#
    """if(complete):
        for i in range(0, 5):
            fqlQuery={}
            for j in range(i*50, min((i+1)*50, len(uInf))):
                fqlQuery[str(uInf[j]["uid"])]=("SELECT fromid FROM comment WHERE object_id "+
                                              "IN (SELECT status_id FROM status WHERE uid="+str(uInf[j]["uid"])+")")
            t=fbGraph.fql(fqlQuery)
            #print t[2]
            for j in t:
                for k in j["fql_result_set"]:
                    print k["fromid"], str(t[j]["name"])
                    try:
                        comMap[str(k["fromid"])][str(j["name"])]+=1
                        print k["fromid"], str(j["name"])
                    except:
                        continue
            print len(t)"""


    
    cnt={}
    viewMutualFriends=graph.getDoubleProperty("viewMutualFriends")
    for n in graph.getNodes():
        noN+=1
        for m in graph.getInOutEdges(n):
            #print graph.source(m)
            if n.id in cnt.keys():
                cnt[n.id].add(graph.source(m).id)
                cnt[n.id].add(graph.target(m).id)
            else:
                cnt[n.id]=set([graph.source(m).id])
                cnt[n.id].add(graph.target(m).id)               

    def geometric_mean(n1, n2):
        #print len(cnt[n1]&cnt[n2]), len(cnt[n1]), len(cnt[n2])
        return 10-10.0*(float(len(cnt[n1]&cnt[n2])/float(len(cnt[n1]))*(float(len(cnt[n1]&cnt[n2]))/float(len(cnt[n2]))))**(1.0/2.0))
    
    for m in graph.getEdges():
        noE+=1
        viewMutualFriends[m]=geometric_mean(graph.source(m).id, graph.target(m).id)
        #print viewMutualFriends[m]
        
    dataSet=tlp.DataSet()
    dataSet["viewMutualFriends"]=viewMutualFriends
    graph.applyLayoutAlgorithm("GEM (Frick)", viewLayout, dataSet)
    graph.applyDoubleAlgorithm("Louvain", viewMetric, dataSet)
    dataSet=tlp.getDefaultPluginParameters("Color Mapping")
    graph.applyColorAlgorithm("Color Mapping", viewColor, dataSet)
    #tlp.exportGraph("TLP Export", graph, "C:/Moving/workspace_C++/tlp2svg/input.in")
    return graph
    

def process_graph(graph):              #This converts the graph into json
    nodes=[{} for x in range(noN)]
    alist = [[] for x in range(noN)]
    edges=[{} for x in range(noE)]

    #t=graph.getIntProperty("start")
    pos=graph.getLayoutProperty("viewLayout")
    clr=graph.getColorProperty("viewColor")
    mfriends=graph.getDoubleProperty("viewMutualFriends")
    #name=graph.getStringProperty("viewLabel")


    for i in graph.getNodes():
        nodes[i.id]["x"]=pos[i].getX()
        nodes[i.id]["y"]=pos[i].getY()
        #nodes[i.id]["color"]=[clr[i].getR(), clr[i].getG(), clr[i].getB()]
        nodes[i.id]["name"]=name[i.id]
        nodes[i.id]["pic"]=picSquare[i.id]
        nodes[i.id]["color"]="rgb("+str(clr[i].getR())+","+str(clr[i].getG())+","+str(clr[i].getB())+")"


    for i in graph.getEdges():
        t=graph.ends(i)
        edges[i.id]["start"]=t[0].id
        edges[i.id]["target"]=t[1].id
        edges[i.id]["mfriends"]=mfriends[i]


    for i in graph.getNodes():
        for j in graph.getInOutEdges(i):
            t=graph.ends(j)
            n1=t[0]
            n2=t[1]
            alist[n1.id].append((n2.id, j.id))
            alist[n2.id].append((n1.id, j.id))
    f = ["var nodes="+json.dumps(nodes)+";\n", "var edges="+json.dumps(edges)+";\n","var alist="+json.dumps(alist)+";\n"]
    f=''.join([`num` for num in f])
    #print len(f)
    return f
    
