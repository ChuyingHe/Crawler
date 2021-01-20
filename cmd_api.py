import requests
from bs4 import BeautifulSoup
import re
import json
from fake_useragent import UserAgent

# time_order:
# 	- 按时间排序：type=1&sort=0
# 	- 按热度排序：type=1&sort=2
def __init__(self):
	self.content = []   # 评论列表


def getHTMLText(url):
	useragent = UserAgent()
	headers = {
	'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'user-agent': useragent.random
	}

	try:
		r = requests.get(url, headers=headers)
		# r.encoding = r.apparent_encoding <-- deleted, otherwise cause problem for chinese
		r.raise_for_status()
		# r.status_code
		return r.text
	except:
		return "Exceptions in getHTMLText()"
	
# get total comments amount
def getVideoInfo(bvid):
	dict = {}

	url = f'https://www.bilibili.com/video/{bvid}'
	html = getHTMLText(url)
	soup = BeautifulSoup(html, 'html.parser')
	# initial_state
	initial_state = soup.find_all('script')[5].string	# <class 'bs4.element.Script'>
	# videoData":{ ...,"upData
	video_data = re.search('"videoData":{.*?upData', initial_state).group()

	count = int(re.search('[0-9]+', re.search('reply":[0-9]+',video_data).group()).group())	# 21223
	avid = int(re.search('[0-9]+', re.search('aid":[0-9]+',video_data).group()).group())	# 286054084
	# title = re.search('[0-9]+', re.search('title":.*,',video_data).group()).group()
	dict["count"] = count
	dict["avid"] = avid

	print(f'视频 {bvid} 的AV号是 {avid} ，元数据中显示本视频共有 {count} 条评论（包括评论的评论）。')
	return dict


# get direct comments (1st layer)
# https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=286054084&sort=2
# 11394（up主自己的定制评论不算）
def getRootComments(video_info, time_order):

	#test: root_comment_url = 'https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=286054084&sort=2'
	#test: html = getHTMLText(root_comment_url)
	# All the pages have the "count" attribute which gives us the amount of first-layer-comment
	root_comment_url = 'https://api.bilibili.com/x/v2/reply?pn={}&type=1&oid=' + str(video_info["avid"]) + '&sort=' + str(time_order)
	html = getHTMLText(root_comment_url.format(0))
	comment_amount = json.loads(html)['data']['page']['count']
	page_amount = comment_amount//20 + 1		# root-comment 每一页有20个，计算总页数

	# Iteration: all pages
	for page in range(1, page_amount + 1):		
		page_url = root_comment_url.format(page)
		page_html = getHTMLText(page_url)
		page_json = json.loads(page_html)
		page_comment_amount = len(page_json['data']['replies'])
		print(page_comment_amount)

		# Iteration: all root comments in one page
		for i in range(page_comment_amount):		
			# self.content.append(page_json['data']['replies'][i]['content']['message'])
			getSubComment(video_info, page_json['data']['replies'][i])

	# return json.loads(html)['data']['page']['count']


# get comments of comment (1st layer) - including folded comments

def getSubComment(video_info, root_comment):	# root_comment = page_json['data']['replies'][i]

	sub_comment_url = 'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={}&type=1&oid='+ str(video_info["avid"]) +'&ps=10&root={}'
	
	if root_comment['replies']!= None:
		# amount of sub-comments for 1 root-comment	/
		sub_comment_amount = root_comment['rcount']				#【397】
		sub_comment_visible = len(root_comment['replies'])		#【3】

		if sub_comment_visible == sub_comment_amount:	 		# 相等的话不需要进行另一个api的调用了，比如只有3条评论，也显示了三条
			for i in range(sub_comment_visible):
				self.content.append(root_comment['replies'][i]['content']['message'])
		else:	 												# 不相等：实际有的sub-comment比显示的多（其他的被折叠了）
			root_comment_id = root_comment['rpid']
			sub_comment_page_amount = sub_comment_amount//10 + 1	# sub-comment 每一页有10个，计算总页数
			for page in range(1, sub_comment_page_amount + 1):
				pass


def main():
	bvid = "BV1Cf4y1y7KX"
	video_info = getVideoInfo(bvid)
	getRootComments(video_info, 2)
	

main()