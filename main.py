import time

from api_wrapper import QuallyApiWrapper
from job_ad import JobAd
from kw_scraper import KeywordScraper



job_ads=[]
job_titles = ["software engineer", "backend developer", "frontend developer", "software developer"]
city_states = [{"city": "San Francisco", "state": "CA"}, {"city": "Palo Alto", "state":"CA"}, 
			  {"city": "Seattle", "state": "WA"}, {"city":"Raliegh", "state": "NC"}, {"city": "Portland","state":"OR"}]



for job_title in job_titles:
	for city_state in city_states:
		print city_state
		print type(city_state)
		user_input={'search_term': job_title,
			'city': city_state['city'],
			'state': city_state['state'],
			'ip': '98.247.242.40',
			'user_agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36",
			}
		job_ads=QuallyApiWrapper.get_job_ads(user_input, 0)

		br = KeywordScraper.login_jobscan()
		for job_ad in job_ads:
			soup = KeywordScraper.perform_jobscan(br, job_ad.content)
			keywords=KeywordScraper.get_keywords(soup)
			KeywordScraper.write_kws_to_csv(keywords, job_title)
			time.sleep(4)