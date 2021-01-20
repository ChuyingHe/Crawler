import bilibili_api as bi
import json

def getComment(bvid):
	try:
		comments = bi.video.get_comments_g(bvid)	
		print(type(comments))	# comments is a generator(dict)
		saveComment(comments)
		return comments
	except:
		return "Exception"

def saveComment(comments):
	print("start writing")
	with open("/Users/chuyinghe/Documents/Crawler/data.json", "w", encoding='utf-8-sig') as jsonfile:
		# writer = csv.DictWriter(jsonfile, delimiter = ',', fieldnames = next(comments).keys())
		output = []
		for i in comments:
			print('.', end='')
			output.append(i)
		json.dump(output, jsonfile)		
	print("done writing.")

def main():
	getComment("BV1Cf4y1y7KX")

# Entrance
main()