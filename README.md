# prePushSpider
KanDian filter

# 一些说明：

##newspaper

1.简单测试，python3与python2差别不大。一般情况下，都无法提取到date，author。可以考虑从百度搜索结果页面取。

2.如需要添加代理，具体在network.get_request_kwargs中添加。参考

    `return {
        'headers': {'User-Agent': useragent},
        'cookies': cj(),
        'timeout': timeout,
        'allow_redirects': True,
        'proxies': {'http':'dev-proxy.oa.com:8080'}
    }`


3.如需不下载图片，可进行配置configuration.py

    `self.fetch_images = False`
    

##日期提取策略


1.都是用正则表达式，一个是直接在网页中提取，另外一个是在百度搜索结果摘要中提取。各有优略。
