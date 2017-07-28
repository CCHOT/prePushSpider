# coding=utf-8
max_page = 3

# 权威网站
site_flag = False               # 是否球启用权威网站
site_file = 'url.txt'          # 权威网站列表文件
site_set = set()

# 看点文章list
KanDianListFile = 'D:\\prePushSpider\\select_prepush2.csv'

# 看点文章存储中间文件
KanDianItemFile = 'KanDianArticle.json'

if site_flag:
    for site in open(site_file):
        site_set.add(site)
else:
    site_set.add('')