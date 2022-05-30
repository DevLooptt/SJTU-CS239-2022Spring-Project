function drawStatic() {
  var data_url;
  var core_url;
  var distribution_url;
  
  var group_index = document.getElementById("select-list-static").value;

  data_url = "../../graphdata/Static_data/problem_" + group_index + ".json";
  core_url = "../../graphdata/Static_data/core_" + group_index + ".json";
  distribution_url = "../../graphdata/Static_data/dis_" + group_index + ".json";
  
  drawPic(data_url, core_url, distribution_url);
  
}

function drawFree() {
  var data_url;
  var core_url;
  var distribution_url;
  var group_index = document.getElementById("select-list-free").value;

  data_url = "../../graphdata/Free_data/problem_" + group_index + ".json";
  core_url = "../../graphdata/Free_data/core_" + group_index + ".json";
  distribution_url = "../../graphdata/Free_data/dis_" + group_index + ".json";

  drawPic(data_url, core_url, distribution_url);
}

function drawPic(data_url, core_url, distribution_url) {
  // Color array
  var group_color = ["#FF0000", "#1685a9", "#eaff56", "#8d4bbb", "#00e500"];

  $.ajax({
    url: data_url,
    type: "GET",
    dataType: "json",
    cache: true,
    success: 
    function (data) {
        displayData(data);
    }
});

var displayData= function(data){
    var map = new Map();
    for(let i=0; i<data.nodes.length; i++){
        map.set(data.nodes[i].id,i);
    }
    const gData = {
        nodes: data.nodes,
        links: data.links
    };

    // cross-link node objects
    gData.links.forEach(link => {
        const a = gData.nodes[map.get(link.source)];
        const b = gData.nodes[map.get(link.target)];
        !a.neighbors && (a.neighbors = []);
        !b.neighbors && (b.neighbors = []);
        a.neighbors.push(b);
        b.neighbors.push(a);

        !a.links && (a.links = []);
        !b.links && (b.links = []);
        a.links.push(link);
        b.links.push(link);
    });

    const highlightNodes = new Set();
    const highlightLinks = new Set();
    let hoverNode = null;

    const Graph = ForceGraph3D()
        (document.getElementById('graph'))
    .graphData(gData)
    .width($(window).width()*0.5)
    .height($(window).height() * 0.9)
    .backgroundColor("#000000")
    .nodeLabel((node)=>{	// Node label
      return "id: " + node.id;	
    })
    .linkLabel((link)=>{ // Link label
      return "Source: "+ link.source.id + " Target: "+ link.target.id;
    })
    .nodeColor((node) => {
      return group_color[node.group];
    })
    .nodeVal(node => highlightNodes.has(node)? node.value*2: node.value)
    //.nodeColor(node => highlightNodes.has(node) ? node === hoverNode ? 'rgb(255,0,0,1)' : 'rgba(255,160,0,0.8)' : 'rgba(0,255,255,0.6)')
    .linkWidth(link => highlightLinks.has(link) ? link.value*2 : link.value)
    .linkDirectionalParticles(link => highlightLinks.has(link) ? 1 : 0)
    .linkDirectionalParticleWidth(4)
    .linkDirectionalParticleSpeed(0.02)
    .onNodeHover(node => {
      // no state change
      // if ((!node && !highlightNodes.size) || (node && hoverNode === node)) return;

      if ((!node ) || (node && hoverNode === node)) return;

      highlightNodes.clear();
      highlightLinks.clear();
      if (node) {
        highlightNodes.add(node);
        node.neighbors.forEach(neighbor => highlightNodes.add(neighbor));
        node.links.forEach(link => highlightLinks.add(link));
      }

      hoverNode = node || null;

      updateHighlight();
    })
    .onNodeClick(node => {
      handleCamera(node);        
    })
    .onLinkHover(link => {
      highlightNodes.clear();
      highlightLinks.clear();

      if (link) {
        highlightLinks.add(link);
        highlightNodes.add(link.source);
        highlightNodes.add(link.target);
      }

      updateHighlight();
    });
  
  // Change camera pos to focus on clicked node
  function handleCamera(node){
    const distance = 600;
    const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
    Graph.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio },
        node, 
        3000  
    );
  }

  function updateHighlight() {
    // trigger update of highlighted objects in scene
    Graph
      .nodeVal(Graph.nodeVal())
      .nodeColor(Graph.nodeColor())
      .linkWidth(Graph.linkWidth())
      .linkDirectionalParticles(Graph.linkDirectionalParticles());
  } 
  
  // Core graph camera distance
  const core_distance = 150;
  // Create core graph

  // Stick nodeLable to nodes
  // const coreGraph = ForceGraph3D({
  //   extraRenderers: [new THREE.CSS2DRenderer()]
  // })
  const coreGraph= ForceGraph3D()
    (document.getElementById('threeobjects'))
    .jsonUrl(core_url)
    .width($(window).width() * 0.3)
    .height($(window).height() * 0.35)
    .backgroundColor("#000000")
    .nodeVal((node) => {
      if (node.group == 5) return 1;
      else return 30;
    })
    .linkWidth('value')
    .nodeColor((node) => {
      if(node.group==5) return "#fff2df"
      return group_color[node.group];
    })
    .nodeThreeObject(node => {
      const nodeEl = document.createElement('div');
      nodeEl.textContent = node.id;
      nodeEl.className = 'node-label';
      return new THREE.CSS2DObject(nodeEl);
    })
    .onNodeHover(node => {
      // no state change
      if (!node || (node && hoverNode === node)) return;

      highlightNodes.clear();
      highlightLinks.clear();
      if (node) {
        var id_to_find = node.id;
        var node_to_find = gData.nodes.find(node => {
          if (node.id == id_to_find) return node;
        })
        highlightNodes.add(node_to_find);
        node_to_find.neighbors.forEach(neighbor => highlightNodes.add(neighbor));
        node_to_find.links.forEach(link => highlightLinks.add(link));
      }
      // console.log(highlightNodes.size);
      hoverNode = node || null;

      updateHighlight();
    })
    .onNodeClick(node => {
      var id_to_find = node.id;
      var node_to_find = gData.nodes.find(curnode => {
        if (curnode.id == id_to_find) return curnode;
      })
      handleCamera(node_to_find);        
    })
    .nodeThreeObjectExtend(true)
    // .enableNodeDrag(false)
    // .enableNavigationControls(false)
    .showNavInfo(false)
    .cameraPosition({ z: core_distance })
    .nodeLabel((node) => {	// Node label
      return "id: " + node.id;
    });
  
  // Auto Rotate for core
  // let angle = 0;
  // setInterval(() => {
  //   coreGraph.cameraPosition({
  //     x: core_distance * Math.sin(angle),
  //     z: core_distance * Math.cos(angle)
  //   });
  //   angle += Math.PI / 300;
  // }, 15);
  
  
  // Create Pie chart
  var chartDom = document.getElementById('pie');
  var myChart = echarts.init(chartDom);
  var option;
  // Init chart data
  $.ajax({
    url: distribution_url,
    type: "GET",
    dataType: "json",
    cache: true,
    success: 
    function (data) {
        pieChart(data);
    }
  });

  var pieChart = function (json_data) {
    
    option = {
      title: {
              text: 'Total Nodes: ' + json_data.totalnodes + '    Domain Nodes: ' + json_data.totaldomain,
              left: 'center',
              top: 0,
              textStyle: {
                color: '#FFFFFF',
                fontSize: 16
              }
          },
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      series: [
        {
          name: 'Node Type',
          type: 'pie',
          center: ['50%', '55%'],
          selectedMode: 'single',
          radius: [0, '30%'],
          label: {
            position: 'inner',
            fontSize: 12
          },
          labelLine: {
            show: true
          },
          data: json_data.all
        },
        {
          name: 'Domain Type',
          type: 'pie',
          center: ['50%', '55%'],
          radius: ['45%', '60%'],
          avoidLabelOverlap: false,
          labelLine: {
            length: 25
          },
          label: {
            formatter: '{abg|} {b|{b}} \n   {c|{c}}  {per|{d}%}  ',
            backgroundColor: '#3d3b4f',
            borderColor: '#8C8D8E',
            borderWidth: 1,
            borderRadius: 4,
            rich: {
              a: {
                color: '#ffffff',
                lineHeight: 22,
                align: 'center'
              },
              hr: {
                borderColor: '#ffffff',
                width: '100%',
                borderWidth: 1,
                height: 0,
              },
              c: {
                color:'#ffffff',
              },
              b: {
                color: '#ffffff',
                fontSize: 14,
                fontWeight: 'bold',
                lineHeight: 33,
                align: 'center'
              },
              per: {
                color: '#fff',
                backgroundColor: '#4C5058',
                padding: [3, 4],
                borderRadius: 4
              }
            }
          },
          data: json_data.nodes
        }
      ]
    };
    option && myChart.setOption(option);
  }


}
}

function drawLegend() {
  const highlightLegend = new Set();
  // Create legend graph
  const legend_distance = 165;
  const legendGraph = ForceGraph3D({
    extraRenderers: [new THREE.CSS2DRenderer()]
  })
    (document.getElementById('legend'))
    .jsonUrl("../../graphdata/legend.json")
    .width($(window).width() * 0.2)
    .height($(window).height() * 0.45)
    .backgroundColor("#000000")
    .showNavInfo(false)
    .enableNodeDrag(false)
    .enableNavigationControls(false)
    //.nodeVal('weight')
    .nodeVal(node => highlightLegend.has(node)? node.weight*2: node.weight)
    .nodeColor((node) => {
      return group_color[node.group];
    })
    .nodeThreeObject(node => {
      const nodeEl = document.createElement('div');
      nodeEl.textContent = node.id;
      nodeEl.className = 'node-label';
      return new THREE.CSS2DObject(nodeEl);
    })
    .nodeThreeObjectExtend(true)
    .cameraPosition({ z: legend_distance });
    
  // Auto rotate
    let angle = 0;
    setInterval(() => {
      legendGraph.cameraPosition({
        x: legend_distance * Math.sin(angle),
        z: legend_distance * Math.cos(angle)
      });
      angle += Math.PI / 300;
    }, 15);
}
