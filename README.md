# prePushSpider
KanDian source score

# 一些说明：

## 网页结构化策略

### newspaper

1.简单测试，python3与python2差别不大。一般情况下，都无法提取到date，author。可以考虑从百度搜索结果页面取。

2.如需要添加代理，具体在network.get_request_kwargs中添加。参考

    `return {
        'headers': {'User-Agent': useragent},
        'cookies': cj(),
        'timeout': timeout,
        'allow_redirects': True,
        'proxies': {'http':'dev-proxy.oa.com:8080'}
    }`
线上环境经测试不需要配置代理


3.如需不下载图片，可进行配置configuration.py

    `self.fetch_images = False`
或者通过传递参数的方式。

    `article = Article(url='', language='zh',fetch_images=False)`
    

### 日期提取策略

1.都是用正则表达式，一个是直接在网页中提取，另外一个是在百度搜索结果摘要中提取。各有优略。

### 文本相似度

1.初期，考虑到实际情况，预要选取的是相同的文章，而非一些同类型，同新闻等文章，没有必要nlp中一些比较复杂的方法，先采用比较简单的算法，这里预研后选用jaro算法。统计4篇文章，85个对比，选取阈值为0.6。分析其同的bad case，主要原因有两点：a.文章爬去不完全（如分页问题，这里没有爬取下一页文章）b.newspaper分析正文出错，提取的正文内容和实际相差较大。


## 权威媒体爬虫说明

### 功能

根据权威媒体中文网站转换为url。示例：

    {"url": "cri.cn", "name": "国际在线"}
	{"url": "people.com.cn", "name": "人民网"}
	{"url": "cntv.cn", "name": "央视国际网络"}
	{"url": "chinadaily.com.cn", "name": "中国日报网"}
	{"url": "ce.cn", "name": "中国经济网"}
	{"url": "youth.cn", "name": "中国青年网（中青网）"}
	{"url": "china.com.cn", "name": "中国网"}

### 说明

在权威媒体列表中，存在中文名称不同，url相同的情况，因此可能出现结果数量，数输入中文网站数量对不上的情况。

