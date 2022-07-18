// 图表容器初始化

// 线性表初始化 深圳市面积与房价折线表
let lineChartDom = document.getElementById('line-chart');
let lineChart = echarts.init(lineChartDom);
let lineChartOption;
let lineChartData = JSON.parse($("#lineChartData").text())  // 从 script 标签中获取到线性表的数据
lineChartOption = {
  title: {
    left: 'center',
    text: '深圳市房屋面积与房价'
  },
  tooltip: {
    trigger: 'axis',
    position: function (pt) {
      return [pt[0], '10%'];
    }
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    data: lineChartData["area_list"],
    boundaryGap: false,
    axisLabel: {
      formatter: '{value} 平米'
    },
  },
  yAxis: {
    type: 'value',
    boundaryGap: [0, "100%"],
    axisLabel: {
      formatter: '{value} 万'
    },
  },
  series: [
    {
      data: lineChartData["price_list"],
      type: 'line',
      smooth: true,
      itemStyle: {
        color: 'rgb(255, 70, 131)'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 158, 68)'
          },
          {
            offset: 1,
            color: 'rgb(255, 70, 131)'
          }
        ])
      },
    },
  ],
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 0.2
    },
    {
      start: 0,
      end: 0.2
    }
  ],
};

// 福田区面积与房价折线表
let ftChartDom = document.getElementById('ft');
let ftLineChart = echarts.init(ftChartDom);
let ftLineChartOption;
let ftLineChartData = JSON.parse($("#ftLineChartData").text())  // 从 script 标签中获取到线性表的数据
ftLineChartOption = {
  title: {
    left: 'center',
    text: '福田区房屋面积与房价'
  },
  tooltip: {
    trigger: 'axis',
    position: function (pt) {
      return [pt[0], '10%'];
    }
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    data: ftLineChartData["area_list"],
    boundaryGap: false,
    axisLabel: {
      formatter: '{value} 平米'
    },
  },
  yAxis: {
    type: 'value',
    boundaryGap: [0, "100%"],
    axisLabel: {
      formatter: '{value} 万'
    },
  },
  series: [
    {
      data: ftLineChartData["price_list"],
      type: 'line',
      smooth: true,
      itemStyle: {
        color: 'rgb(255, 70, 131)'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 158, 68)'
          },
          {
            offset: 1,
            color: 'rgb(255, 70, 131)'
          }
        ])
      },
    },
  ],
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 20
    },
    {
      start: 0,
      end: 20
    }
  ],
};

// 龙岗区面积与房价折现表
let lgChartDom = document.getElementById('lg');
let lgLineChart = echarts.init(lgChartDom);
let lgLineChartOption;
let lgLineChartData = JSON.parse($("#lgLineChartData").text())  // 从 script 标签中获取到线性表的数据
lgLineChartOption = {
  title: {
    left: 'center',
    text: '龙岗区房屋面积与房价'
  },
  tooltip: {
    trigger: 'axis',
    position: function (pt) {
      return [pt[0], '10%'];
    }
  },
  toolbox: {
    feature: {
      dataZoom: {
        yAxisIndex: 'none'
      },
      restore: {},
      saveAsImage: {}
    }
  },
  xAxis: {
    type: 'category',
    data: lgLineChartData["area_list"],
    boundaryGap: false,
    axisLabel: {
      formatter: '{value} 平米'
    },
  },
  yAxis: {
    type: 'value',
    boundaryGap: [0, "100%"],
    axisLabel: {
      formatter: '{value} 万'
    },
  },
  series: [
    {
      data: lgLineChartData["price_list"],
      type: 'line',
      smooth: true,
      itemStyle: {
        color: 'rgb(255, 70, 131)'
      },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          {
            offset: 0,
            color: 'rgb(255, 158, 68)'
          },
          {
            offset: 1,
            color: 'rgb(255, 70, 131)'
          }
        ])
      },
    },
  ],
  dataZoom: [
    {
      type: 'inside',
      start: 0,
      end: 20
    },
    {
      start: 0,
      end: 20
    }
  ],
};

// 饼图初始化
let pieDom = document.getElementById('pie-chart');
let pieChart = echarts.init(pieDom);
let pieData = JSON.parse($("#pieData").text())  // 从 script 标签中获取到线性表的数据
let pieOptions;

pieOptions = {
  title: {
    left: 'center',
    text: '深圳市房屋类型分布比例'
  },
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '5%',
    left: 'center'
  },
  series: [
    {
      name: 'Access From',
      type: 'pie',
      radius: ['40%', '70%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 10,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: false,
        position: 'center',
        formatter: "{b}: {c} {d}%"
      },
      emphasis: {
        label: {
          show: true,
          fontSize: '40',
          fontWeight: 'bold'
        }
      },
      labelLine: {
        show: false
      },
      data: pieData
    }
  ]
};

// 加载所有图表
lineChartOption && lineChart.setOption(lineChartOption);  // 深圳市总折线图表
ftLineChartOption && ftLineChart.setOption(ftLineChartOption);  // 福田折线图表
lgLineChartOption && lgLineChart.setOption(lgLineChartOption);  // 龙岗折线图表
pieOptions && pieChart.setOption(pieOptions);  // 房屋类型图比例
