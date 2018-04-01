# amazon_in_stock

### 介绍

一个简单的监控amazon.cn是否到货和是否低于预期价格的Python脚本，如果符合条件就给目标发送微信。

**只支持海外购商品**，测试了几个商品，其他商品不保证正确性。不过理论上遇到问题，稍微改改好了。我目前这个就是根据[Amazon com商品解析](https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python/)魔改的，只是对比了有货跟没货两个商品的html diff，其实我对html一无所知。

### 依赖

安装requests、itchat库。

```shell
pip install requests
pip install itchat
```

### 引用
1. [How To Scrape Amazon Product Details and Pricing using Python](https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python/)
2. [python使用itchat发送微信消息提醒](http://www.cnblogs.com/chenbei-blog/p/7799352.html)
3. [itchat文档](http://itchat.readthedocs.io/zh/latest/)
