# coding=utf-8
import json

max_page = 3

# 权威网站
site_search_flag = False            # 是否启用权威媒体网站高级搜索
site_file = 'url.txt'               # 权威网站列表文件
media_file = 'media.txt'            # 权威网站中文列表文件
site_filter_flag = True             # 是否启用权威媒体网站过滤
site_set = set()

# 看点文章list
KanDianListFile = 'select_test.csv'

# 看点文章存储中间文件
KanDianItemFile = 'KanDianArticle.json'

for site in open(site_file):
    tmp = json.loads(site)
    site_set.add(tmp['url'])
print '添加'+str(len(site_set))+'个权威网站'



