# -*- coding: utf-8 -*-
import requests
import json
from fake_useragent import UserAgent
import re

'''--------------------------------评论类---------------------------------'''
class PingLun():
    
    def __init__(self,av):
        self.av = av    # 视频av号
        self.count = 0    # 总评论数
        self.url = 'https://api.bilibili.com/x/v2/reply?&pn={}&type=1&oid='+str(self.av)
        self.content = []   # 评论列表
        self.r_url = 'https://api.bilibili.com/x/v2/reply/reply?jsonp=jsonp&pn={}&type=1&oid='+str(av)+'&ps=10&root={}'
        
    
    def fetchURL(self,url):
        '''
        功能：访问url的网页，获取网页内容并返回
        参数：
            url:目标网页的url
        返回：目标网页的html内容
        '''
        useragent = UserAgent()
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': useragent.random,
        }
        
        try:
            r = requests.get(url,headers=headers)
            r.raise_for_status()
            return r.text
        except requests.HTTPError as e:
            print(e)
            print('HTTPError')
        except requests.RequestException as e:
            print(e)
        except:
            print('Unknown Error!')
            
            
    def parserHTML(self,html):
        '''
        功能：根据参数html给定的内存型HTML文件，尝试解析其结构，获取所需内容
        参数：
            html：类似文件的内存HTML文本对象
        '''
        # 解析为json数据
        try:
            s = json.loads(html)
        except TypeError:
            # 请求失败的话就不停地请求
            i = 1
            while html == None:
                if i < 100:
                    url = self.url.format(self.page)
                    html = self.fetchURL(url)
                    i += 1
                else:
                    return None
            s = json.loads(html)
#            print(html)
#            print(type(html))
#            return None
            
        # 当前这一页的评论数
        size = len(s['data']['replies'])
    
        for i in range(size):  
            # 当前评论
            self.content.append(s['data']['replies'][i]['content']['message'])
            # 当前评论的回复 ----------------------------------------------------- root_comment = s['data']['replies'][i]
            replies = s['data']['replies'][i]['replies']
            if replies != None:
                # 总的回复数量 ----------------------------------------------------- 
                num_replies_total = s['data']['replies'][i]['count']    # 包括被折叠的         # @TODO: which one is correct? ['count'] or ['rcount']
                # 实际显示的回复总数
                num_replies_indicate = len(replies)                     # 不包括被折叠的                             
                
                if num_replies_total == num_replies_indicate:   # 相等的话不需要进行另一个api的调用了，比如只有3条评论，也显示了三条
                    for j in range(len(replies)):
                        self.content.append(replies[j]['content']['message'])
                else:
                    root = s['data']['replies'][i]['rpid']  # _id
                    # 回复每一页有10个，计算总页数
                    page_num_replies = num_replies_total//10 + 1
                    for page in range(1,page_num_replies+1):
                        useragent = UserAgent()
                        headers = {
                                'user-agent': useragent.random,
                        }
                        # 回复的api
                        r_url = self.r_url.format(page,root)
                        try:
                            # 抓取回复数据
                            r = json.loads(requests.get(r_url,headers=headers).text)
                            for k in range(len(r['data']['replies'])):
                                self.content.append(r['data']['replies'][k]['content']['message'])
                        except:
                            pass
#                            print('评论编号：'+str(i))
#                            print(s['data']['replies'][i]['content']['message'])
#                            print(r_url)
                        
            
    def writePage(self):
        import pandas as pd
        df = pd.DataFrame(self.content)
        file_name = './评论数据.csv'
        df.to_csv(file_name,index=False, sep=',', header=False,encoding="utf_8_sig")
            
        
    def run(self):
        # 总评论数
        self.count = json.loads(self.fetchURL(self.url.format(1)))['data']['page']['count']
        # 评论的页数
        num_page = self.count//20 + 1
        # print(self.count,num_page)
        
        for self.page in range(1,num_page+1):
#            print('page:'+str(page))
            url = self.url.format(self.page)
            html = self.fetchURL(url)
            self.parserHTML(html)

        # 保存数据
        self.writePage()


if __name__ == '__main__':
    av = 89971424
    
    pl = PingLun(av)
    pl.run()
