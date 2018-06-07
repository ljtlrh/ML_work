新闻涉及经营异常


主体公司:

input data:  ["重庆誉存大数据科技有限公司"]


output data:

```
{
     'time': '2017-08-09 10:00:00.124322',
     'source': 'news',
     'name': '风险新闻',
     'count': 3,  #命中多少次
     'scId':[],
     'content':[
                 {'dateKey': '2017',
                  'cnt': 2,
                  'contentPart': [{
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2017-06-06"   //新闻发生时间
                                                 },
                                            "companyName": "重庆誉存大数据科技有限公司"
                                        },
                                    {
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2017-05-06"   //新闻发生时间
                                                 },
                                            "companyName": "重庆誉存大数据科技有限公司"

                                    }]
                 },
                 {'dateKey': '2016',
                  'cnt': 1,
                  'contentPart':[{
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2016-06-06"   //新闻发生时间
                                                 },
                                            "companyName": "重庆誉存大数据科技有限公司"

                                    }]
                 }

               ]
}

```




关联公司:

input data:  input data:

```
[{companyName:'companyName1', connectType: '对外投资'}, {companyName:'companyName2', connectType: '企业股东'},{companyName:'companyName3', connectType: '法人对外投资'}]
```

output data:

```
{
     'time': '2017-08-09 10:00:00.124322',
     'source': 'connectNews',
     'name': '关联公司-风险新闻',     #所有关联公司的风险新闻
     'count': 2,  #命中多少家
     'scId':[],
     'content':[
                 {'companyName': '关联公司一名字',
                  'connectType': '对外投资',
                  'cnt': 2,
                  'contentPart': [{
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2017-06-06"   //新闻发生时间
                                                 }
                                     },
                                    {
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2017-06-06"   //新闻发生时间
                                                 }

                                    }]
                 },
                 {'companyName': '关联公司二名字',
                 'connectType': '企业股东',
                  'cnt': 1,
                  'contentPart':[{
                                            "type": "风险新闻",
                                            "detail": {
                                                "newsTital": "长安汽车江北发动机工厂大石坝基地全部关停并完成设备搬迁",      //新闻标题
                                                "newsYime": "2017-06-06"   //新闻发生时间
                                                 }
                                   }]
                 }]
}

```