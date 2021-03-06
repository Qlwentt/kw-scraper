# _*_ coding:utf-8 _*_
from __future__ import unicode_literals
from collections import defaultdict

import sys  
import unidecode
import re

import urllib2
from textblob import TextBlob as tb
from BeautifulSoup import BeautifulSoup
import re
import requests
import unidecode


reload(sys)  
sys.setdefaultencoding('utf8')



class JobAd(object):
	"""" A job ad from the Indeed API. It has the following properties:
	Attributes:
		# id: unique identitfier 		integer
		key: unique id for API 		string
		title: title of job ad; 	string
		snippet: short description; string
		url: url of full ad; 		string
		company: company name;		string
		content: full content of ad string 
		location: City, State;		string
		date: date posted;			datetime
	"""


	def __init__(self, properties):
		#Returns job ad object with properties
		self.key=properties['key']
		self.title=properties['title']
		self.snippet=properties['snippet']
		self.content=''
		self.url=properties['url']
		self.company=properties['company']
		self.location=properties['location']
		self.date=properties['date']

		# self.keywords = []

	@staticmethod
	def fix_spacing(text):
		  text=re.sub(r'([a-z:.)])([A-Z]|\d)', r'\1 \2', text)
		  text=re.sub(r'([A-Z])(\d)', r'\1 \2', text)
		  
		  text=text.decode("utf-8").replace(u"\u2022", " ").encode("utf-8")
		  return text

	@classmethod
	def make_job_ads_from_api(cls,api_json_resp):
		job_ads=[]
			
		for result in api_json_resp:
			# print "result: {}".format(result)
			# print "result type: {}".format(type(result[0]))
			job_ads.append(JobAd({
				'key': result['jobkey'],
				'title': result['jobtitle'],
				'snippet': result['snippet'],
				'url': result['url'],
				'company': result['company'],
				'location': result['formattedLocation'],
				'date': result['date']
				})) 
		for job_ad in job_ads: 
				job_ad.content=job_ad.set_content()
				
		return job_ads
	
	def set_content(self):	
	    # self.content=job_ad_text
	    html = urllib2.urlopen(self.url).read()
	    soup = BeautifulSoup(html)
	    job_ad_text = soup.find('span', attrs={'id': 'job_summary'}).text
	    job_ad_text= JobAd.fix_spacing(job_ad_text)
	    print job_ad_text
	    return job_ad_text


# # indeed_request_url="http://api.indeed.com/ads/apisearch?publisher=9253729351823762&q=software engineer&l=seattle%2C+wa&sort=&radius=&st=&jt=&start={}&limit=1000&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4&useragent=Mozilla/%2F4.0%28Firefox%29&v=2&format=json"
# # APIresponse = requests.get(indeed_request_url).json()['results']
# # test_job_ads=JobAd.make_job_ads_from_api(APIresponse)
# # print test_job_ads
# # print len(test_job_ads)
# # print type(test_job_ads)
# # print type(test_job_ads[0])

# # print dir(test_job_ads[0])
# # print test_job_ads[0].content


