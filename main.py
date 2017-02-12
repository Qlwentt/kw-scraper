from api_wrapper import QuallyApiWrapper
from job_ad import JobAd
from kw_scraper import KeywordScraper

import random


job_ads=[]
num_records = 100
job_titles = ["software engineer", "backend developer", "frontend developer", "software developer"]
city_state = [{"city": "San Francisco", "state": "CA"}, {"city": "Palo Alto", "state":"CA"}, 
			  {"city": "Seattle", "state": "WA"}, {"city":"Raliegh", "state": "NC"}, {"city": "Portland","state":"OR"}]

user_input={'search_term': data['job_title'],
				'city': data['city'],
				'state': data['state'],
				'ip': get_client_ip(request),
				'user_agent': request.META['HTTP_USER_AGENT'],
				}
for i in range(num_records/25):
	job_ads.extend(QuallyApiWrapper.get_job_ads(user_input, i*25))

