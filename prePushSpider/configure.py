# coding=utf-8
import json
import os

max_page = 3

# 权威网站
site_search_flag = False            # 是否启用权威媒体网站高级搜索
site_file = 'prePushSpider/url.txt'               # 权威网站列表文件
media_file = 'prePushSpider/media.txt'            # 权威网站中文列表文件
site_filter_flag = True             # 是否启用权威媒体网站过滤
threshold = 0.5
site_set = set()


# 看点文章list
KanDianListFile = 'prePushSpider/科技.txt'

# 看点文章存储中间文件
KanDianItemFile = 'prePushSpider/KanDianArticle.json'

# score本地文件
ScoreDir = 'prePushSpider/score'

# Url文章本地文件
DownloadDir = 'prePushSpider/download'

for site in open(site_file):
    tmp = json.loads(site)
    site_set.add(tmp['url'])
print('添加'+str(len(site_set))+'个权威网站')

if not os.path.exists(ScoreDir):
     os.mkdir(ScoreDir)
if not os.path.exists(DownloadDir):
    os.mkdir(DownloadDir)
