import requests
from bs4 import BeautifulSoup
import re

# import traceback
url = "https://www.bilibili.com/video/BV1Cf4y1y7KX"
r = requests.get(url)
r.encoding = r.apparent_encoding
r.status_code
soup = BeautifulSoup(r.text, 'html.parser')


# 1) get total comments amount

initial_state = soup.find_all('script')[5]	# <class 'bs4.element.Tag'>
content = initial_state.string				# <class 'bs4.element.Script'>
# re.search('"reply":[0-9]+',initial_state.string)	# <re.Match object; span=(1003, 1016), match='"reply":21223'>
reply = re.search('"reply":[0-9]+',initial_state.string).group()	#'"reply":21223'
count = int(re.search('[0-9]+', reply).group())						# 21223




# 2) get comments
url = "https://api.bilibili.com/x/v2/reply?pn=1&type=1&oid=286054084&sort=2"
html = getHTMLText(url)			# <class 'str'>
html_dict = json.loads(html)	# <class 'dict'>


with open(html, encoding='utf-8') as fh:
    comments = json.load(fh)