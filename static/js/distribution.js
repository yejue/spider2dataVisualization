const heat_map_data = document.getElementById('heatmap-data');

const heat_map_data_obj = JSON.parse(heat_map_data.innerText); // 以上两步是获取后端渲染来的数据，并将其转换为 json 格式数据。

var heat_map_data_json = [];

heat_map_data_json.push(heat_map_data_obj); // heatmap 需要的数据格式是 [ json ] 因此在这里创建了一个列表

const top10_data = document.getElementById('top10-data');

const top10_data_json = JSON.parse(top10_data.innerText); // 参考上面的例子，获取总价/单价前十的 json 数据。

const dom = document.getElementById('container');

var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
}); // 初始化一个 echarts 实例，准备绘制热力图.

var option; // 设置项变量

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
] // 房价总价前十的小区的定位。

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
]; // 房价总价前十的房子的价格。

// 将从后端渲染来的数据进行格式转换，为后续在 bmap 上绘制散点图做准备。
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

// 将从后端渲染来的数据进行格式转换，为后续在 bmap 上绘制热力图做准备。
var clearData = function (data) { // 参考了 echarts 官网的热力图示例中的功能函数。
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

var t_data = clearData(heat_map_data_json);// 数据转换

myChart.setOption( // echarts 设置选项
    (option = {
        tooltip: {
            trigger: 'item',
            formatter: function (val) {
                let val_str = "房屋名字: " + val['data']['value'][2]['house_name'] +
                    "<br/>户型: " + val['data']['value'][2]['house_type'] + "<br/>" +
                    "总面积: " + val['data']['value'][2]['house_area'] + " 平方米<br/>" +
                    "总价: " + val['data']['value'][2]['total_price'] + " 万";
                return val_str; // 只支持 h5 形式的显示
            }, // 自定义提示框内容。
        },
        animation: false, // 关闭动画效果
        bmap: {
            center: [114.063836, 22.543884],  // 设置百度地图的中心，位于福田站
            zoom: 12, // 地图初始化缩放等级为 12
            roam: true // 允许地图使用滚轮进行缩放
        },
        visualMap: {
            show: false, // 是否显示 visualMap-continuous 组件。如果设置为 false，不会显示，但是数据映射的功能还存在
            top: 'top', //组件离容器上侧的距离,'top', 'middle', 'bottom','20%
            min: 0, // 指定 visualMapContinuous 组件的允许的最小值
            max: 5, // 指定 visualMapContinuous 组件的允许的最大值
            seriesIndex: 2, // 指定取哪个系列的数据，即哪个系列的 series.data ,这里指定的是 heatmap
            calculable: true, // 是否显示拖拽用的手柄（手柄能拖拽调整选中范围）
            inRange: { // 定义在选中范围中的视觉元素的颜色
                color: ['blue', 'blue', 'green', 'yellow', 'red']
            }
        },
        series: [
            {
                type: 'scatter', // 散点图
                coordinateSystem: 'bmap', // 坐标系为百度地图坐标系
                data: convertData(total_price, top10_data_json),
                pointSize: 5,
                symbolSize: function (val) {
                    return (val[2]['total_price'] / 30) / 10;
                },
                label: {
                    normal: {   // 默认
                        formatter: '{b}',
                        position: 'right',
                        show: false
                    },
                    emphasis: {  // 悬浮
                        show: true
                    }
                },
                itemStyle: {
                    normal: {
                        color: 'rgba(255,0,0,0.6)',   // 小圆点的颜色
                    }
                }
            },// 上面是固定大小远点，往下是涟漪点
            {
                name: 'Top 10',
                type: 'effectScatter',  // 带有涟漪特效动画的散点（气泡）
                coordinateSystem: 'bmap',  // 坐标系统
                data: convertData(total_price.sort(function (a, b) {  //数据排序，截取前10个
                    return b.value - a.value;
                }).slice(0, 10), top10_data_json),
                symbolSize: function (val) {   // 标志图形大小
                    return (val[2]['total_price'] / 30) / 10;// 涟漪圈大小
                },
                showEffectOn: 'render',   // 绘制完成后显示特效。
                rippleEffect: {           // 涟漪特效相关配置。
                    brushType: 'stroke'    // 波纹的绘制方式
                },
                hoverAnimation: true, // 鼠标移入到图上不放大但会将内容显示在中心.
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
                        shadowBlur: 0.8,     // 模糊度

                        // shadowColor: '#333'  // 阴影颜色
                    }
                },
                zlevel: 1      // 一级层叠控制
            },
            {
                type: 'heatmap', // 热力图
                coordinateSystem: 'bmap', // 坐标系 百度地图
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


let bmap = myChart.getModel().getComponent('bmap').getBMap(); // 百度地图实例初始化

bmap.addControl(new BMap.MapTypeControl()); // 添加百度地图插件

if (option && typeof option === 'object') {
    myChart.setOption(option); // 如果还没绘图就开始绘图，如果已经绘图就不再绘图，避免重复加载。
    // myBarChart.setOption(Bar_option);
}

window.addEventListener('resize', myChart.resize); // 让echarts图表随着浏览器窗口的大小变化而变化
