* `graphdata`
  * `problem_0.json`：第一个团伙的图数据；
  * `distribution.json`：某一团伙的 domain 节点分布数据；
  * `core.json`：某一团伙的核心资产和关键链路数据；
  * `legend.json`：图例
* `src`
  * `utils.js`：绘制部分代码
  * `css`
    * `page.css`：页面 CSS
  * `Picture`：背景图片
* `index.html`：需要 open with live server 运行

* `problem.json` 和`core.json`数据说明：
  * "group": 节点类型，参见`legend.json`
  *  "weight"：节点权重，30的画出来已经很大了
* `distribution.json`数据说明：
  * 参考示例即可，"value"为该类型的节点数目
  * "totalnodes"：为某子图的全部节点数
  * "totaldomain"：某子图的全部domain类型的节点数