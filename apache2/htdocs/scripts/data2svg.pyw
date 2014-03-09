#! /usr/bin/env python2.7-32

import facebook
import json
import tulip_facebook
import time
import sys
#import mutuality
from tulip import *


token="CAACEdEose0cBAC8wEINz4x9qpfDdvsZAdx6OjBbYloWZBXoFFDosPZAYtRHNrGgevnKFmbsgW3OwSEZBDKQE0kmOWzcwkws1SlVOnt5wNmmuSwafR7jIURRECyGfj32E4uQlJtsnAe5sktC6NmVOYZAnu60C0Mly5ulDOrS56LZBc21tCMBn8FSfbAKyqAnZCgZD"

graph=tlp.newGraph()
#fql_query="SELECT post_id FROM stream WHERE source_id = me()"
#query=[{"method":"GET", "relative_url":"me"},{"method":"GET", "relative_url":"me/friends?limit=50"}]
#payload = {"batch": query, "access_token": token}
#r = requests.post("https://graph.facebook.com/", params=payload)
#print r.url

start=time.clock()


def gen_graph():                            #This gets all the info needed
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

    userId="100000186340290"
    mutualFriendEdges=[]
    ans=0
    fMap={}

    #----------Get Node Info---------------------------#
    uInf=fbGraph.fql("SELECT uid, pic_square, name FROM user WHERE uid=me() OR uid IN (SELECT uid2 FROM friend WHERE uid1 = me())" )
    #print len(uInf)
    meNode=graph.addNode()

    for i in uInf:
        uid=str(i["uid"])
        #print uid, i["name"]
        alist[uid]={}
        curN=graph.addNode()
        fMap[uid]=curN
        name[uid] = i["name"].encode("UTF-8", "replace")
        picSquare[uid]=i["pic_square"]

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
                #print k
                node1=fMap[k["uid1"].encode("UTF-8", "replace")]
                node2=fMap[k["uid2"].encode("UTF-8", "replace")]
                if not graph.existEdge(node1, node2, False).isValid():
                    #print "hi"
                    graph.addEdge(node1, node2)
    #----Get Likes/Comments/Tags----------------------------------------#
    cnt={}
    viewMutualFriends=graph.getDoubleProperty("viewMutualFriends")
    for n in graph.getNodes():
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
        viewMutualFriends[m]=geometric_mean(graph.source(m).id, graph.target(m).id)
        #print viewMutualFriends[m]
        
    dataSet=tlp.DataSet()
    dataSet["viewMutualFriends"]=viewMutualFriends
    graph.applyLayoutAlgorithm("GEM (Frick)", viewLayout, dataSet)
                              
    
    
gen_graph()

def process_graph(graph):              #This converts the graph into json
    nodes=[{} for x in range(300)]
    alist = [{} for x in range(300)]
    edges=[{} for x in range(400000)]

    #t=graph.getIntProperty("start")
    pos=graph.getLayoutProperty("viewLayout")
    clr=graph.getColorProperty("viewColor")
    mfriends=graph.getDoubleProperty("viewMutualFriends")
    name=graph.getStringProperty("viewLabel")


    for i in graph.getNodes():
        nodes[i.id]["pos"]=[pos[i].getX(), pos[i].getY()]
        #nodes[i.id]["color"]=[clr[i].getR(), clr[i].getG(), clr[i].getB()]
        nodes[i.id]["name"]=name[i]
        
    for i in graph.getEdges():
        t=graph.ends(i)
        edges[i.id]["start"]=t[0]
        edges[i.id]["target"]=t[1]


    for i in graph.getNodes():
        for j in graph.getInOutEdges(i):
            alist[i.id][j.id]= {}
            alist[i.id][j.id]["to"]=graph.opposite(j, i).id
            alist[i.id][j.id]["mfriends"]=mfriends[j]
    #json.dump(nodes)

#heh=tlp.loadGraph("C:/Users/Horace/AppData/Local/Tulip 4.4/plugins/graph.tlp")
process_graph(graph)
print time.clock()-start
