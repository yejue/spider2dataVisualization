const heat_map_data = document.getElementById('heatmap-data');
const heat_map_data_obj = JSON.parse(heat_map_data.innerText);
var heat_map_data_json = new Array();
heat_map_data_json.push(heat_map_data_obj);
const dom = document.getElementById('container');
const top10_data = document.getElementById('top10-data');
const top10_data_json = JSON.parse(top10_data.innerText);

var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var option;

const address_list = [
    {
        '观澜湖': [114.07662793721526, 22.734602044976892],
        '西丽山庄': [113.98043549679703, 22.59505620892735],
        '鸿荣源·壹方中心·玖誉': [113.89413196275157, 22.558646985674],
        '波托菲诺纯水岸四期': [113.97930282337987, 22.555589310473923],
        '波托菲诺纯水岸四期': [113.97930282337987, 22.555589310473923],
        '海上世界双玺': [113.92628599999566, 22.48680051332269],
        '百仕达红树西岸': [113.97226289293106, 22.528062308733464],
        '波托菲诺纯水岸十五期': [113.97854195861318, 22.5549690058216],
        '东海花园': [114.02818824989453, 22.544343201333714],
        '鲸山觐海': [113.91373496524493, 22.48470556452431],
    },
]
const total_price = [
    {name: '观澜湖', value: 8500},
    {name: '西丽山庄', value: 6838},
    {name: '鸿荣源·壹方中心·玖誉', value: 5024.0},
    {name: '波托菲诺纯水岸四期', value: 4421.0},
    {name: '波托菲诺纯水岸四期', value: 4420.0},
    {name: '海上世界双玺', value: 4293.0},
    {name: '百仕达红树西岸', value: 4121.0},
    {name: '波托菲诺纯水岸十五期', value: 3856.0},
    {name: '东海花园', value: 3823.0},
    {name: '鲸山觐海', value: 3800},
];

const convertData = function (data, label_data) {   //转换数据
    label_data = label_data['total_price_top10'];
    let res = [];
    for (let i = 0; i < data.length; i++) {
        let geoCoord = address_list[0][data[i].name];   //地理坐标
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat(label_data[i]),
            });
        }
    }
    return res;
};

var clearData = function (data) {
    var points = [].concat.apply(
        [],
        data.map(function (track) {
            return track.map(function (seg) {
                return seg.coord.concat([1]);
            });
        })
    );
    return points;
};

var t_data = clearData(heat_map_data_json);
myChart.setOption(
    (option = {
        tooltip: {
            trigger: 'item',
            formatter: function (val) {
                let val_str = "房屋名字:" + val['data']['value'][2]['house_name'] +
                    "<br/>户型:" + val['data']['value'][2]['house_type'] + "<br/>" +
                    "总面积:" + val['data']['value'][2]['house_area'] + "平方米<br/>" +
                    "总价:" + val['data']['value'][2]['total_price'] + "万";
                return val_str;//只支持h5形式的显示
            },
        },
        animation: false,
        bmap: {
            center: [114.063836, 22.543884],  // 福田站坐标
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
                data: convertData(total_price, top10_data_json),
                pointSize: 5,
                symbolSize: function (val) {
                    return (val[2]['total_price'] / 30) / 10;
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
                data: convertData(total_price.sort(function (a, b) {  //数据排序，截取前10个
                    return b.value - a.value;
                }).slice(0, 10), top10_data_json),
                symbolSize: function (val) {   //标志图形大小
                    return (val[2]['total_price'] / 30) / 10;//涟漪圈大小
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
                data: t_data,
                pointSize: 5,
                blurSize: 6,
            },
        ]
    })
);

/*
const Bar_option = {
    tooltip: {
        formatter: function (val) {
            let val_str = "房屋名称:" + val['data']['name'] + "</br>" + "价格:" + val['data']['value'] + "万";

            return val_str;
        }
    },
    dataset: {
        dimensions: ['name', 'value'],
        source: total_price,
    },
    xAxis: {type: 'category'},
    yAxis: {},
    series: [{type: 'bar'}]
};*/

// 添加百度地图插件
let bmap = myChart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.MapTypeControl());
if (option && typeof option === 'object') {
    myChart.setOption(option);
    // myBarChart.setOption(Bar_option);
}
window.addEventListener('resize', myChart.resize);
