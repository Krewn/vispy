class drawable:
    def __init__(self,name,anID):
        self.name = name
        self.data = []
        self.type = "line"
        self.id = anID
    def addData(self,x,y):
        self.data.append((x,y))
    def setType(self,t):
        self.type = t
    def groupInfo(self):
        ret = """groups.add({
        id: """+str(self.id)+""",
        content: '"""+self.name+"""',
        options: {
            drawPoints: false"""+(",style:'bar'"if self.type =="bar" else "")+"""
        }});"""
        return(ret)
    def getData(self):
        return(",".join(["{x: "+str(k[0])+", y: "+str(k[1])+", group: "+str(self.id)+"}" for k in self.data]))

class chart:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.drawables = []
    def addDrawable(self,d):
        self.drawables.append(d)
    def addGroups(self):
        ret = ""
        for n,k in enumerate(self.drawables):
            ret+=k.groupInfo()+"\n"
        return(ret)
    def addGraphItems(self):
        return(",".join([k.getData() for k in self.drawables]))
    def opGraph(self,opfn):
        op = open(opfn,"w")
        op.write("""
<html>

<head>
    <script src = "http://visjs.org/dist/vis.js"></script>
    <link href="http://visjs.org/dist/vis-timeline-graph2d.min.css" rel="stylesheet" type="text/css">
</head>
<body>
  <h3>"""+self.title+"""</h3>
  <p><"""+self.description+"""</p>
  <div id="visChart"></div>
  <script>
      var groups = new vis.DataSet()
      """+self.addGroups()+"""
      var container = document.getElementById("visChart");
      var dataset = new vis.DataSet(["""+self.addGraphItems()+"""]);
      var options = {
          defaultGroup: 'ungrouped',
          legend: true
      };
      var graph2d = new vis.Graph2d(container, dataset, groups, options);
  </script>  
</body>
</html>""")
        op.close()
    
            

