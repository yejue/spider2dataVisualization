// 图表容器初始化

// 线性表初始化 深圳市房价热力图与散点图
const dom = document.getElementById('container');
let myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
let option;

const heat_map_data_obj = JSON.parse($("#heatmap-data").text()); // 从 script 标签中获取用于绘制热力图的数据。
let heat_map_data_json = new Array();
heat_map_data_json.push(heat_map_data_obj); // echarts 官方的示例，数据处理函数需要的格式是 [ json ] 因此在此新建一个列表

const top10_convert_json = JSON.parse($("#top10_convert").text());// 从 script 标签中获取用于绘制散点图的数据。


// 热力图数据处理函数
let clearData = function (data) {
    let points = [].concat.apply(
        [],
        data.map(function (track) {
            return track.map(function (seg) {
                return seg.coord.concat([1]);
            });
        })
    );
    return points;
};

myChart.setOption(
    (option = {
        tooltip: {
            trigger: 'item',
            formatter: function (top10_data_json) {
                let tooltip_str = top10_data_json['name'] +
                    "<br/>户型: " + top10_data_json['data']['value'][4] + "<br/>" +
                    "总面积: " + top10_data_json['data']['value'][5] + " 平方米<br/>" +
                    "总价: " + top10_data_json['data']['value'][2] + " 万";
                return tooltip_str;//只支持h5形式的显示
            },
        },
        title: {
            left: "200px",
            top: "20px",
            text: "深圳市房价分布态势",
            textStyle: {
                fontSize: 30,
            },
        },
        animation: false,
        bmap: {
            center: [114.123611,22.537961],  // 深圳站坐标
            zoom: 12,
            roam: true
        },
        visualMap: {
            show: false,
            top: 'top',
            min: 0,
            max: 5,
            seriesIndex: 2,
            calculable: true,
            inRange: {
                color: ['blue', 'blue', 'green', 'yellow', 'red']
            }
        },
        series: [
            {
                type: 'scatter',
                coordinateSystem: 'bmap',
                data: top10_convert_json,
                pointSize: 5,
                symbolSize: function (top10_data_json) {
                    return (top10_data_json[2]/ 30) / 10;
                },
                label: {
                    normal: {   //默认
                        formatter: '{b}',
                        position: 'right',
                        show: false
                    },
                    emphasis: {  //悬浮
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(255,0,0,0.6)',   //小圆点的颜色
                    }
                }
            },//上面是固定大小远点，往下是涟漪点
            {
                name: 'Top 10',
                type: 'effectScatter',  //带有涟漪特效动画的散点（气泡）
                coordinateSystem: 'bmap',  //坐标系统
                data:top10_convert_json.sort(function (a, b) {  //数据排序，截取前10个
                    return b.value[2] - a.value[2];
                }).slice(0, 10),
                symbolSize: function (top10_data_json) {   //标志图形大小
                    return (top10_data_json[2]/ 30) / 10;//涟漪圈大小
                },
                showEffectOn: 'render',   //绘制完成后显示特效。
                rippleEffect: {           //涟漪特效相关配置。
                    brushType: 'stroke'    //波纹的绘制方式
                },
                hoverAnimation: true,
                label: {
                    normal: {
                        formatter: '{b}',
                        position: 'right',
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(255,0,0,0.6)',
                        shadowBlur: 0.8,     //模糊度

                        // shadowColor: '#333'  //阴影颜色
                    }
                },
                zlevel: 1      // 一级层叠控制
            },
            {
                type: 'heatmap',
                coordinateSystem: 'bmap',
                data: clearData(heat_map_data_json),
                pointSize: 5,
                blurSize: 6,
            },
        ]
    })
);


// 添加百度地图插件
let bmap = myChart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.MapTypeControl());

// 如果已经存在那么不再再次绘制，节省资源。
if (option && typeof option === 'object') {
    myChart.setOption(option);
}

window.addEventListener('resize', myChart.resize); // 支持浏览器缩放时,图表自适应。
