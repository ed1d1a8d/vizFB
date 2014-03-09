var names=paper.set();
var dNode=paper.set();
var prev={id: 0};
var cur={};



var start=null;

function makeInvis(){
	if(prev.box!=null) prev.box.attr({opacity: .5});
	if(prev.boxpic!=null) prev.boxpic.attr({opacity: .5});
}

function revealInvis(){
	console.log("hm")
	prev.box.attr({opacity: 1})
	if(prev.boxpic!=null) prev.boxpic.attr({opacity: 1})
}

function nodeClick(id){
	return function(){
		if(prev.paths!=null){
			//console.log(prev.paths.length)
			for(var i=0; i<prev.paths.length; i++){
				prev.paths[i].remove();
			}
		}
		prev.paths=paper.set();
		//console.log(alist[id])
		//console.log(alist[id][875])
		var cnt=0;
		for(var i=0; i < alist[id].length; i++){
			prev.paths.push(paper.path("M "+ (nodes[edges[alist[id][i][1]].start].x) +" "+(nodes[edges[alist[id][i][1]].start].y)+" L "+nodes[edges[alist[id][i][1]].target].x+" "+(nodes[edges[alist[id][i][1]].target].y)));
			t=edges[alist[id][i][1]].mfriends;
			prev.paths[i].attr({stroke: "rgb("+(t/8.0)*255+","+(t/8.0)*255+","+(t/8.0)*255+")"});
		}
		if(prev.box!=null) prev.box.remove()
		prev.box=paper.rect(nodes[id].x-200, nodes[id].y-150, 200, 150)
		prev.box.attr({fill: "rgb(225, 225, 225)", stroke: "rgb(100, 100, 100)"})
		if(prev.boxname!=null) prev.boxname.remove();
		prev.boxname=paper.print(nodes[id].x-200+20, nodes[id].y-150+20, nodes[id].name, paper.getFont("Cabin"))
		
		prev.box.hover(function(){
		prev.box.attr({opacity: .2});
		if(prev.boxpic!=null) prev.boxpic.attr({opacity: .2});
		}, function(){
		prev.box.attr({opacity: 1});
		prev.boxpic.attr({opacity: 1});})
		
		if(prev.boxpic!=null) prev.boxpic.remove();
		prev.boxpic=paper.image(nodes[id].pic, nodes[id].x-200+40, nodes[id].y-150+40, 75, 75)
		
		prev.boxpic.hover(function(){
		prev.box.attr({opacity: .2});
		if(prev.boxpic!=null) prev.boxpic.attr({opacity: .2});
		}, function(){
		prev.box.attr({opacity: 1});
		prev.boxpic.attr({opacity: 1});});
	}
}

function nodeHover(id){
	//console.log(id);
	return function(){
		
		var timestamp=Date.now();
		if(prev.id==id) return 0;
		var tEdge=paper.set();
		
		//console.log(prev.id, id)
		dNode[prev.id].attr({fill : nodes[prev.id].viewColor, transform: "s1"}); 
		if(prev.name!=null) prev.name.remove();
		if(prev.pic!=null) prev.pic.remove();
		
		//console.log(nodes[id].name)
		cur.name=paper.print(100, 100, nodes[id].name, paper.getFont("Cabin"));
		cur.pic=paper.image(nodes[id].pic, 200, 150, 25, 25);
		
		prev.name=cur.name;
		//console.log(prev.name);
		prev.pic=cur.pic;
		prev.id = id;

		
		dNode[id].toFront();
		
		
		dNode[id].attr({fill: "rgba(255,102,0,255)"});
		dNode[id].attr({transform: "s2"});   												

	}
}

function sq(num){
	return num*num;
}

window.onload = function() {
	var maxX, maxY, minX, minY;
	maxX=-10000, maxY=-10000, minX=10000, minY=10000
	for(var i=0; i<nodes.length; i++){
		maxX=Math.max(maxX, nodes[i].x);
		minX=Math.min(minX, nodes[i].x);
		maxY=Math.max(maxX, nodes[i].y);
		minY=Math.min(minY, nodes[i].y);
	}
	console.log(minX, maxX, minY, maxY)
	var xOff, yOff, mult;
	xOff=Math.abs(minX)+50;
	yOff=Math.abs(minY)+50;
	mult=Math.min(900.0/(maxX+xOff), 900.0/(maxY+yOff));
	//mult=1
	for(var i=0; i<nodes.length; i++){
		nodes[i].x+=xOff;
		nodes[i].x*=mult;
		nodes[i].y+=yOff;
		nodes[i].y*=mult;
		//console.log(nodes[i].x, nodes[i].y)
	}
	for(var i=0; i<edges.length; i++){
		//if(sq(Math.abs(nodes[edges[i].start].x-nodes[edges[i].target].x))+sq(Math.abs(nodes[edges[i].start].y-nodes[edges[i].target].y))<sq(160)){
			var t=paper.path("M "+ (nodes[edges[i].start].x) +" "+((nodes[edges[i].start].y))+" L "+nodes[edges[i].target].x+" "+(nodes[edges[i].target].y));
			t.attr({"stroke": "rgb(225,225,225)"})
		//}
		
	}
	var svg = paper.toSVG();
	canvg(document.getElementById("myCanvas"), svg);
	paper.clear();
	
    setTimeout(function() {
		var dataURL = document.getElementById('myCanvas').toDataURL("image/png");
		var edgeImg= new Image();
		edgeImg.src=dataURL;
		var width = edgeImg.width;
		var height = edgeImg.height;
		edgeImg=paper.image(dataURL, 0, 0, width, height);
		edgeImg.toBack();
       }, 100);
	 
	
	for(var i=0; i<nodes.length; i++){
		//var t=paper.text(nodes[i].x*2, nodes[i].y*2, nodes[i].viewLabel);
		/*var t =paper.print(100, 100, nodes[i].viewLabel, paper.getFont("Cabin", 800), 30);
		t.attr({size: 40});
		t.hover(dispName);
		t.hide();
		names.push(t);*/
		//console.log(names.length);
		nodes[i].viewColor="rgb(0,51,102,255)";
		
		dNode.push(paper.circle(nodes[i].x, nodes[i].y, 3));
		dNode[i].attr({fill: nodes[i].viewColor, "stroke-width": .1});
		dNode[i].hover(nodeHover(i));
		dNode[i].click(nodeClick(i));

	}
}





