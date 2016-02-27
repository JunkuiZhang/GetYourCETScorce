import requests
import re

post_url = "http://202.114.74.136/cet/Default.aspx"
img_url = "http://202.114.74.136/cet/createImg.aspx"
info_url = "http://202.114.74.136/cet/cjcx.aspx"
base_num = "20133010000"


def getImg():
	f = open("0.jpg", "wb")
	response = requests.get(img_url)
	f.write(response.content)
	f.close()
	return response


def getScorce():
	response = getImg()
	code = input("Input the strings: ")
	cook = re.findall('ASP.NET_SessionId=(.*) for 202', str(response.cookies))[0]
	for num in range(20, 50, 1):
		name = base_num + str(num)
		print("Trying %s" % name)
		post_header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
			"Cookie": "ASP.NET_SessionId=" + str(cook)
		}
		post_data = {
			"__VIEWSTATE": "/wEPDwUJNzk0Mjc1ODYxZGTA2JHtu/6dMRKjxx4BTOvIwSiodw==",
			"__EVENTVALIDATION": "/wEWBwKB463wCgLs0bLrBgLs0fbZDALs0Yq1BQLs0e58AoznisYGArursYYIRM5sLK//aqCBB6vcyOYfSaHnYlk=",
			"TextBox1": name,
			"TextBox2": "",
			"TextBox3": "张昊",
			"TextBox4": code,
			"Button1": "查询"
		}
		res = requests.post(post_url, data=post_data, cookies=response.cookies, headers=post_header)
		info = requests.get(info_url, cookies=res.cookies, headers=post_header)
		infom = str(info.text)
		index = re.findall('无成绩记录，请检查输入是否有误', infom)
		if index == []:
			print(infom)
			print(re.findall('成绩</td><td>([0-9]*)</td>', infom)[0])
			break

getScorce()