##  一、开发环境

python3.10、ubuntu2204

（python 最低需要 python3.8）

**附注：本项目使用数据库为MySQL，详细配置见：spider2dataVisualization/settings.py**

## 二、快速启动

1. 克隆本项目
2. 安装所有的依赖包,  $ pip install -r requirements.txt $
3. 创建数据库 ”spider2dataVisualization“
4. 配置 spider2dataVisualization/settings.py 的 DATABASES
5. 根据 model.py 创建新的迁移 $ python manage.py makemigrations $
6. 执行迁移 $ python manage.py migrate $
7. 在根目录路径下放入 global.env 和示例.sql ,将示例.sql 导入数据库 spider2dataVisualization
8. 启动Django $ python manage.py runserver 0:8000 $
9. 在浏览器访问  ip 地址:8000 即可运行本项目。

## 三、接口设计

####  3.1 城市信息列表

接口地址：/api/city_list/

返回格式：json

请求方式：get

请求示例： /api/city_list/?page=1

接口备注： 城市信息展示接口。可使用 page 进行结果过滤。（支持使用表字段进行结果过滤）

------

参数说明:

| 名称 | 必须性 | 类型    | 描述                     | 默认值 |
| ---- | ------ | ------- | ------------------------ | ------ |
| page | 否     | integer | 请求结果的页数，缺省为 1 | 1      |

返回参数说明:

| 名称     | 类型    | 说明               |
| -------- | ------- | ------------------ |
| previous | string  | 上一页的结果的 url |
| next     | string  | 下一页结果的 url   |
| results  | list    | 搜索结果数据列表   |
| count    | integer | 总的结果数量       |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "count": 154,
    "next": "http://192.168.15.132:8000/api/city_list/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "create_time": "2022-07-08T12:56:22.128571+08:00",
            "update_time": "2022-07-08T12:56:22.128617+08:00",
            "city_name": "安庆",
            "subdomain": "https://aq.lianjia.com/",
            "created_by": 1
        }
    ],
}
```

#### 3.2 城市信息详情接口
接口地址：/api/city_list/:id

返回格式：json

请求方式：get

请求示例：/api/city_list/1/

接口备注： 城市信息详情接口。可使用 id 查询某一条目详情。暂无过滤参数。

------

参数说明：

| 名称 | 必须性 | 类型    | 描述          | 默认值 |
| ---- | ------ | ------- | ------------- | ------ |
| id   | 是     | integer | 数据库中的 id | 1      |

返回参数说明：

| 名称    | 类型 | 说明             |
| ------- | ---- | ---------------- |
| results | list | 搜索结果数据列表 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "id": 1,
    "create_time": "2022-07-08T12:56:22.128571+08:00",
    "update_time": "2022-07-08T12:56:22.128617+08:00",
    "city_name": "安庆",
    "subdomain": "https://aq.lianjia.com/",
    "created_by": 1
}
```

####  3.3 辖区信息列表

接口地址：/api/district_list/

返回格式：json

请求方式：get

请求示例： /api/district_list/?page=1

接口备注： 辖区信息展示接口。可使用 page 进行结果过滤。（支持使用表字段进行结果过滤）

------

参数说明:

| 名称 | 必须性 | 类型    | 描述                     | 默认值 |
| ---- | ------ | ------- | ------------------------ | ------ |
| page | 否     | integer | 请求结果的页数，缺省为 1 | 1      |

返回参数说明:

| 名称     | 类型    | 说明               |
| -------- | ------- | ------------------ |
| previous | string  | 上一页的结果的 url |
| next     | string  | 下一页结果的 url   |
| results  | list    | 搜索结果数据列表   |
| count    | integer | 总的结果数量       |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "count": 99,
    "next": "http://192.168.15.132:8000/api/district_list/?page=2",
    "previous": null,
    "results": [
        {
            "id": 106,
            "create_time": "2022-07-08T17:25:17.501857+08:00",
            "update_time": "2022-07-08T17:25:17.501913+08:00",
            "district_name": "罗湖区",
            "lon": null,
            "lat": null,
            "city": 19,
            "parent": null
        }
    ]
}
```

#### 3.4 辖区信息详情接口
接口地址：/api/district_list/:id

返回格式：json

请求方式：get

请求示例：/api/district_list/

接口备注： 辖区信息详情接口。可使用 id 查询某一条目详情。暂无过滤参数。

------

参数说明：

| 名称 | 必须性 | 类型    | 描述          | 默认值 |
| ---- | ------ | ------- | ------------- | ------ |
| id   | 是     | integer | 数据库中的 id | 无     |

返回参数说明：

| 名称    | 类型 | 说明             |
| ------- | ---- | ---------------- |
| results | list | 搜索结果数据列表 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "id": 1,
    "create_time": "2022-07-08T17:25:17.501857+08:00",
    "update_time": "2022-07-08T17:25:17.501913+08:00",
    "district_name": "罗湖区",
    "lon": null,
    "lat": null,
    "city": 19,
    "parent": null
}
```


####  3.5 小区信息列表

接口地址：/api/estate_list/

返回格式：json

请求方式：get

请求示例： /api/estate_list/?page=1

接口备注： 辖区信息展示接口。可使用 page 进行结果过滤。（支持使用表字段进行结果过滤）

------

参数说明:

| 名称 | 必须性 | 类型    | 描述                     | 默认值 |
| ---- | ------ | ------- | ------------------------ | ------ |
| page | 否     | integer | 请求结果的页数，缺省为 1 | 1      |

返回参数说明:

| 名称     | 类型    | 说明               |
| -------- | ------- | ------------------ |
| previous | string  | 上一页的结果的 url |
| next     | string  | 下一页结果的 url   |
| results  | list    | 搜索结果数据列表   |
| count    | integer | 总的结果数量       |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "count": 5148,
    "next": "http://192.168.15.132:8000/api/estate_list/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5774,
            "create_time": "2022-07-08T20:48:16.473009+08:00",
            "update_time": "2022-07-18T17:09:40.611120+08:00",
            "estate_name": "阳光绿地家园",
            "lon": 114.14319731616294,
            "lat": 22.569812821078028,
            "avg_price": 59700.0,
            "house_code": "2411048928212",
            "district": 107
        }
    ]
 }
```


#### 3.6 小区信息详情接口
接口地址：/api/estate_list/:id

返回格式：json

请求方式：get

请求示例：/api/estate_list/1/

接口备注： 城市信息详情接口。可使用 id 查询某一条目详情。暂无过滤参数。

------

参数说明：

| 名称 | 必须性 | 类型    | 描述          | 默认值 |
| ---- | ------ | ------- | ------------- | ------ |
| id   | 是     | integer | 数据库中的 id | 无     |

返回参数说明：

| 名称    | 类型 | 说明             |
| ------- | ---- | ---------------- |
| results | list | 搜索结果数据列表 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "id": 1,
    "create_time": "2022-07-08T20:48:16.473009+08:00",
    "update_time": "2022-07-18T17:09:40.611120+08:00",
    "estate_name": "阳光绿地家园",
    "lon": 114.14319731616294,
    "lat": 22.569812821078028,
    "avg_price": 59700.0,
    "house_code": "2411048928212",
    "district": 107
}
```

####  3.7 房子信息列表

接口地址：/api/house_info_list/

返回格式：json

请求方式：get

请求示例： /api/house_info_list/?page=1

接口备注： 房子信息展示接口。可使用 page 进行结果过滤。（支持使用表字段进行结果过滤）

------

参数说明:

| 名称 | 必须性 | 类型    | 描述                     | 默认值 |
| ---- | ------ | ------- | ------------------------ | ------ |
| page | 否     | integer | 请求结果的页数，缺省为 1 | 1      |

返回参数说明:

| 名称     | 类型    | 说明               |
| -------- | ------- | ------------------ |
| previous | string  | 上一页的结果的 url |
| next     | string  | 下一页结果的 url   |
| results  | list    | 搜索结果数据列表   |
| count    | integer | 总的结果数量       |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "count": 23311,
    "next": "http://192.168.15.132:8000/api/house_info_list/?page=2",
    "previous": null,
    "results": [
        {
            "id": 2874,
            "create_time": "2022-07-08T23:00:27.767926+08:00",
            "update_time": "2022-07-08T23:00:27.768010+08:00",
            "title": "此房满五唯一，税费少，阳光充足，东南向，诚心出售",
            "house_code": "105110791655",
            "location": "百仕达",
            "house_type": "2室1厅",
            "house_area": 72.16,
            "total_price": 433.0,
            "unit_price": 59900.0,
            "estate": 5778,
            "created_by": 1
        }
    ]
}
```


#### 3.8 房子信息详情接口
接口地址：/api/house_info_list/:id

返回格式：json

请求方式：get

请求示例：/api/house_info_list/1/

接口备注： 房子信息详情接口。可使用 id 查询某一条目详情。暂无过滤参数。

------

参数说明：

| 名称 | 必须性 | 类型    | 描述          | 默认值 |
| ---- | ------ | ------- | ------------- | ------ |
| id   | 是     | integer | 数据库中的 id | 无     |

返回参数说明：

| 名称    | 类型 | 说明             |
| ------- | ---- | ---------------- |
| results | list | 搜索结果数据列表 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "id": 2874,
    "create_time": "2022-07-08T23:00:27.767926+08:00",
    "update_time": "2022-07-08T23:00:27.768010+08:00",
    "title": "此房满五唯一，税费少，阳光充足，东南向，诚心出售",
    "house_code": "105110791655",
    "location": "百仕达",
    "house_type": "2室1厅",
    "house_area": 72.16,
    "total_price": 433.0,
    "unit_price": 59900.0,
    "estate": 5778,
    "created_by": 1
}
```

## 四、暂定错误码

| 错误码 | 描述                                           |
| ------ | ---------------------------------------------- |
| 200    | OK                                             |
| 4001   | PARAM_ERR 传入的参数值错误，多出现于值类型错误 |
| -1     | UNKNOWN_ERR 未知错误                           |
| 5001   | CONNECT_ERR 连接错误，多出现为代理连接异常     |

##  五、数据集成任务

1. 集成小区坐标数据

   `python manage.py getEstateCoords` 

2. 集成链家小区数据

   `python manage.py getLianjiaEstate`

3. 集成链家二手房数据

   `python manage.py getLianjiaSecondHand`

## 六、链家二手房爬虫描述

### 6.1 数据表模型
#### 6.1.1 城市表

| 字段名     | 类型   | 描述                           | 默认 |
| ---------- | ------ | ------------------------------ | ---- |
| city_name  | string | 城市名, unique 约束。          | 无   |
| subdomain  | url    | 子域名链接,通向某城市链家网站. | 无   |
| created_by | string | 创建者                         | 无   |

```python
class CityModel(BaseModel):
    """城市表"""
    city_name = models.CharField("城市名字", max_length=32, unique=True, help_text="城市名字")
    subdomain = models.URLField("子域名链接", max_length=128, help_text="子域名链接")
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"<id: {self.id} city_name: {self.city_name}>"

    class Meta:
        db_table = "city"
        ordering = ["id"]
        verbose_name = "城市表"
        verbose_name_plural = verbose_name
```



#### 6.1.2 辖区表

| 字段名        | 类型       | 描述                                     | 默认 |
| ------------- | ---------- | ---------------------------------------- | ---- |
| city          | ForeignKey | 外键约束，辖区表是城市表的一个从表       | 无   |
| parent        | ForeignKey |                                          | 无   |
| district_name | string     | 辖区名，辖区或者是某区域， unique 约束。 | 无   |
| lon           | float      | 经度                                     | 无   |
| lat           | float      | 纬度                                     | 无   |
|               |            |                                          |      |

```python
class DistrictModel(BaseModel):
    """辖区表"""
    city = models.ForeignKey(CityModel, null=True, on_delete=models.SET_NULL)
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    district_name = models.CharField("辖区名", max_length=128, help_text="辖区或者是某区域", unique=True)
    lon = models.FloatField("经度", null=True, help_text="经度")
    lat = models.FloatField("纬度", null=True, help_text="纬度")

    def __str__(self):
        return f"<id: {self.id} district_id: {self.district_name}>"

    class Meta:
        db_table = "district"
        ordering = ["id"]
        verbose_name = "辖区表"
        verbose_name_plural = verbose_name
```
#### 6.1.3 小区表

| 字段名      | 类型       | 描述                               | 默认 |
| ----------- | ---------- | ---------------------------------- | ---- |
| district    | ForeignKey | 外键约束，小区表是辖区表的一个从表 | 无   |
| estate_name | string     | 小区名                             | 无   |
| lon         | float      | 经度                               | 无   |
| lat         | float      | 纬度                               | 无   |
| avg_price   | float      | 参考均价                           | 无   |
| house_code  | string     | 房子编号                           | 无   |

```python
class EstateModel(BaseModel):
    """小区表"""
    district = models.ForeignKey(DistrictModel, null=True, on_delete=models.SET_NULL)
    estate_name = models.CharField("小区名", max_length=128, help_text="小区名")
    lon = models.FloatField("经度", null=True, help_text="经度")
    lat = models.FloatField("纬度", null=True, help_text="纬度")
    avg_price = models.FloatField("参考均价", null=True, help_text="小区房价最近的参考均价")
    house_code = models.CharField("房子编号", max_length=32, unique=True, help_text="房子编号", null=True)

    def __str__(self):
        return f"<id: {self.id} 小区名: {self.estate_name}>"

    class Meta:
        db_table = "estate"
        ordering = ["id"]
        verbose_name = "小区表"
        verbose_name_plural = verbose_name
```
#### 6.1.4 房子信息表

| 字段名      | 类型       | 描述                                   | 默认 |
| ----------- | ---------- | -------------------------------------- | ---- |
| title       | string     | 链家二手房商品的描述                   | 无   |
| house_code  | string     | 房子编号                               | 无   |
| location    | string     | 大概的位置，最低层次的位置信息         | 无   |
| house_type  | string     | 户型，二手房的户型，例如xx室xx厅。     | 无   |
| house_area  | float      | 房子面积                               | 无   |
| total_price | float      | 房子总价，单位是万                     | 无   |
| unit_price  | 单价       | 每单位价格                             | 无   |
| estate      | ForeignKey | 外键约束，房子信息表是小区表的一个从表 |      |

```python
class HouseInfoModel(BaseModel):
    """房子信息表"""
    title = models.CharField("房子标题", max_length=256, help_text="房子标题")
    house_code = models.CharField("房子编号", max_length=32, unique=True, help_text="房子编号")
    location = models.CharField("位置", max_length=128, help_text="大概的位置，最低层次的位置信息")
    house_type = models.CharField("户型", max_length=32, help_text="户型")
    house_area = models.FloatField("房子面积", help_text="房子面积")
    total_price = models.FloatField("总价", help_text="总价")
    unit_price = models.FloatField("单价", help_text="每单位价格")

    estate = models.ForeignKey(EstateModel, null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"<{self.estate.estate_name} title: {self.title}>"

    class Meta:
        db_table = "house_info"
        ordering = ["id"]
        verbose_name = "房子信息表"
        verbose_name_plural = verbose_name
```
