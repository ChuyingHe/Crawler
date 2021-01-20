import bilibili_api as bi
import csv

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
	with open("/Users/chuyinghe/Documents/Crawler/data.csv", "w", encoding="utf-8-sig") as csvfile:
		writer = csv.DictWriter(csvfile, delimiter = ",", fieldnames = next(comments).keys())
		for i in comments:
			print(".", end="")
			writer.writerow(i)			
	print("done writing.")

def main():
	getComment("BV1Cf4y1y7KX")

# Entrance
main()