##  一、开发环境

python3.10、ubuntu2204

（python 最低需要 python3.8）

**附注：本项目使用数据库为MySQL，详细配置见：spider2dataVisualization/settings.py**

## 二、快速启动

1. 克隆本项目
2. 安装所有的依赖包,  ` pip install -r requirements.txt `
3. 创建数据库 “spider2dataVisualization”，并配置 spider2dataVisualization/settings.py 的 DATABASES
4. 创建迁移 ` python manage.py makemigrations `
5. 执行迁移 ` python manage.py migrate `
6. 可以选择将示例 .sql 数据导入到数据库中，也可以选择依次执行城市、辖区、小区、房子、辖区坐标，小区坐标这六个功能接口
7. 按照 global.env 内提示配置两个百度地图 access key
8. 使用命令启动 ` python manage.py runserver 0:8000 `，在任意浏览器访问  ip 地址:8000 即可

## 三、信息接口

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

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 1,
            "create_time": "2022-07-08T12:56:22.128571+08:00",
            "update_time": "2022-07-08T12:56:22.128617+08:00",
            "city_name": "安庆",
            "subdomain": "https://aq.lianjia.com/",
            "created_by": 1
        },
    ],
    "total_count": 154
}
```

#### 3.2 城市信息详情接口
接口地址：/api/city_list/:id

返回格式：json

请求方式：get

请求示例：/api/city_list/?city_name=安庆

接口备注： 城市信息详情接口。支持使用对应模型库字段参数过滤。

------

参数说明：

| 名称      | 必须性 | 类型     | 描述                 | 默认值 |
| --------- | ------ | -------- | -------------------- | ------ |
| city_name | 是     | string   | 数据库中的城市名字段 | 无     |
| id        | 否     | interger | 数据库中的 id        | 无     |
| subdomain | 否     | string   | 城市链家网址         | 无     |
|           |        |          |                      |        |

返回参数说明：

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 1,
            "create_time": "2022-07-08T12:56:22.128571+08:00",
            "update_time": "2022-07-08T12:56:22.128617+08:00",
            "city_name": "安庆",
            "subdomain": "https://aq.lianjia.com/",
            "created_by": 1
        }
    ],
    "total_count": 1
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

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 106,
            "create_time": "2022-07-08T17:25:17.501857+08:00",
            "update_time": "2022-07-08T17:25:17.501913+08:00",
            "district_name": "罗湖区",
            "lon": null,
            "lat": null,
            "city": 19,
            "parent": null,
        }
    ],
    "total_count": 99
}
```

#### 3.4 辖区信息详情接口
接口地址：/api/district_list/:id

返回格式：json

请求方式：get

请求示例：/api/district_list/?district_name=罗湖区

接口备注： 辖区信息详情接口。支持使用对应模型库字段参数过滤。

------

参数说明：

| 名称          | 必须性 | 类型     | 描述                   | 默认值 |
| ------------- | ------ | -------- | ---------------------- | ------ |
| district_name | 是     | string   | 数据库中的辖区名字段   | 无     |
| city          | 否     | interger | 数据库中对应的城市编号 | 无     |
| id            | 否     | interger | 数据库中的 id          | 无     |

返回参数说明：

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |
|             |         |                              |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 106,
            "create_time": "2022-07-08T17:25:17.501857+08:00",
            "update_time": "2022-07-08T17:25:17.501913+08:00",
            "district_name": "罗湖区",
            "lon": null,
            "lat": null,
            "city": 19,
            "parent": null,
        }
    ],
    "total_count": 5148
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

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 5774,
            "district_id": 107,
            "estate_name": "阳光绿地家园",
            "lon": 114.14319731616294,
            "lat": 22.569812821078028,
            "avg_price": 59700.0,
            "house_code": "2411048928212"
        }
    ],
    "total_count": 5148
}
```


#### 3.6 小区信息详情接口
接口地址：/api/estate_list/:id

返回格式：json

请求方式：get

请求示例：/api/estate_list/1/

接口备注： 城市信息详情接口。支持使用对应模型库字段参数过滤。

------

参数说明：

| 名称        | 必须性 | 类型    | 描述                 | 默认值 |
| ----------- | ------ | ------- | -------------------- | ------ |
| estate_name | 是     | string  | 数据库中的小区名字段 | 无     |
| id          | 否     | integer | 数据库中的 id        | 无     |
| house_code  | 否     | string  | 数据库中的小区id字段 | 无     |

返回参数说明：

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
        {
            "id": 5774,
            "district_id": 107,
            "estate_name": "阳光绿地家园",
            "lon": 114.14319731616294,
            "lat": 22.569812821078028,
            "avg_price": 59700.0,
            "house_code": "2411048928212"
        }
    ],
    "total_count": 1
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

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 results 内的字段介绍参考**6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
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
    ],
    "total_count": 23311
}
```


#### 3.8 房子信息详情接口
接口地址：/api/house_info_list/:id

返回格式：json

请求方式：get

请求示例：/api/house_info_list/?house_code=105110791655

接口备注： 房子信息详情接口。支持使用对应模型库字段参数过滤。

------

参数说明：

| 名称       | 必须性 | 类型    | 描述                         | 默认值 |
| ---------- | ------ | ------- | ---------------------------- | ------ |
| house_code | 是     | string  | 数据库中对应的房子id编号     | 无     |
| id         | 否     | integer | 数据库中的 id                | 无     |
| title      | 否     | string  | 数据库中对应的二手房售卖标题 | 无     |
| house_type | 否     | string  | 数据库中对应的房子户型       | 无     |
| location   | 否     | string  | 数据库中对应房子的位置       | 无     |

返回参数说明：

| 名称        | 类型    | 说明                         |
| ----------- | ------- | ---------------------------- |
| result_code | string  | 返回状态码                   |
| message     | string  | 状态码对应信息，或自定义信息 |
| data        | list    | 搜索结果数据列表             |
| total_count | integer | 总的结果数量                 |

返回参数示例:

关于 data 内的字段介绍参照 **6.1数据表模型**

```python
{
    "result_code": "200",
    "message": "成功",
    "data": [
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
    ],
    "total_count": 1
}
```

## 四、功能接口

**注意，四个功能接口请按照顺序使用，才可正确集成数据录入对应的数据表。**

### 4.1 集成添加城市数据功能接口
使用方法：使用命令 ` python manage.py runserver 0:8000 ` 启动本项目之后，在任意浏览器中访问
ip:8000/visualization/add_city/ ,然后等待录入结束，页面弹出以下信息即可。

```python
{
    "result_code": "200",
    "message": "成功",
    "data": null
}
```
### 4.2 集成添加辖区数据功能接口
使用方法：使用命令 ` python manage.py runserver 0:8000 ` 启动本项目和上述城市数据录入完毕之后，在任意浏览器中访问 ip:8000/visualization/add_district/ ,然后等待录入结束，页面弹出以下信息即可。

```python
{
    "result_code": "200",
    "message": "成功",
    "data": null
}
```
### 4.3 集成添加小区数据功能接口
使用方法：使用命令 ` python manage.py runserver 0:8000 ` 启动本项目和上述辖区数据录入完毕之后，在任意浏览器中访问 ip:8000/visualization/add_estate/ ,然后等待录入结束，页面弹出以下信息即可。

```python
{
    "result_code": "200",
    "message": "成功",
    "data": null
}
```
### 4.4 集成添加房屋信息数据功能接口
使用方法：使用命令 ` python manage.py runserver 0:8000 `启动本项目和上述小区数据录入完毕之后，在任意浏览器中访问 ip:8000/visualization/add_data/ ,然后等待录入结束，页面弹出以下信息即可。

```python
{
    "result_code": "200",
    "message": "成功",
    "data": null
}
```


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

| 字段名      | 类型       | 描述                                   | 默认  |
| ----------- | ---------- | -------------------------------------- |-----|
| title       | string     | 链家二手房商品的描述                   | 无   |
| house_code  | string     | 房子编号                               | 无   |
| location    | string     | 大概的位置，最低层次的位置信息         | 无   |
| house_type  | string     | 户型，二手房的户型，例如xx室xx厅。     | 无   |
| house_area  | float      | 房子面积                               | 无   |
| total_price | float      | 房子总价，单位是万                     | 无   |
| unit_price  | 单价       | 每单位价格                             | 无   |
| estate      | ForeignKey | 外键约束，房子信息表是小区表的一个从表 | 无   |

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

## 七、暂定错误码

| 错误码 | 描述                                           |
| ------ | ---------------------------------------------- |
| 200    | OK                                             |
| 4001   | PARAM_ERR 传入的参数值错误，多出现于值类型错误 |
| -1     | UNKNOWN_ERR 未知错误                           |
| 5001   | CONNECT_ERR 连接错误，多出现为代理连接异常     |
