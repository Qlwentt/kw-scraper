from __future__ import unicode_literals
import unidecode
# _*_ coding:utf-8 _*_
# encoding=utf8  

import mechanize
from BeautifulSoup import BeautifulSoup
import urllib2 
import cookielib
import requests
import random
import time
import os
import csv

import sys
reload(sys)  
sys.setdefaultencoding('utf8')

class KeywordScraper(object):

	@staticmethod
	def login_jobscan():
		cj = cookielib.CookieJar()
		br = mechanize.Browser()

		br.set_cookiejar(cj)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
		br.set_handle_equiv(True)
		br.set_handle_redirect(True)
		br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

		user_agents=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
					'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3',
					'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201',
					'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko'
					]

		#pick a random user-agent to try to pretend not to be a bot
		br.addheaders = [('user-agent',  random.choice(user_agents)),
		('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

		#log in
		br.open('https://www.jobscan.co/login')
		br.select_form(name='reg')
		br.form['email']= os.environ["JOB_SCAN_EMAIL"]
		br.form['password']= os.environ["JOB_SCAN_PW"]
		br.submit()
		return br

	@staticmethod
	def perform_jobscan(br,job_desc):
		resume = """EXPERIENCE

		Software Development Student, Ada Developers Academy (August 2016 - August 2017)

		Intensive training in full stack software development, with exposure to and implementation of a wide variety of languages, frameworks, and methodologies.
		Emphasis on collaboration, leadership, Agile practices, and computer science fundamentals.
		PAST EXPERIENCE

		Assisted in database management
		Wrote an Excel VBA macro that extracts patient data from a database and outputs a personalized report

		Edited internal documents for proper format, legal statements, and language mechanics according to style guide
		Edited engineering white papers for content, structure, and spelling/grammar
		Distinguished performance at internship; (Read recommendation on LinkedIn)

		Wrote marketing copy, website content, and white papers
		Edited academic papers in various writing styles (APA, MLA, Chicago, AMA) for submission to peer-reviewed journals

		Ensured unit preparation for a chemical, biological, or nuclear attack by:
		planning and executing training exercises
		ordering and ensuring maintenance of $40K worth of equipment
		inspecting lower level units and assisting them with meeting standards
		giving biweekly presentations regarding status of program
		Rebuilt a failing program into the most improved program in the organization in a matter of months

		Managed of a platoon of 25 soldiers in preparation for overseas deployment
		EDUCATION

		United States Military Academy at West Point (2012)
		Bachelor of Science in Psychology, with a concentration in Computer Science (GPA: 3.4)

		SKILLS

		Experience with and affinity for learning programming languages
		Ruby on Rails, DJango/Python, Java
		Exposure to tools/languages for front-end development
		HTML/CSS, Javascript, Backbone JS
		Familiarity with database design/implementation
		Access, MS SQL Server, MySQL, SQLite, Postgres
		ACCOMPLISHMENTS

		Qualcomm Coin of Distinguished Achievement for performance during internship in 2014
		Basic Parachutist (Certified to safely exit an airplane at 1250ft by static line parachute)"""

		br.open('https://www.jobscan.co/')
		br.select_form(name='form')
		br.form['cv']= resume
		br.form['jd']= job_desc
		# for f in br.forms():
		# 	print f
		br.submit()
		return BeautifulSoup(br.response())

	@staticmethod
	def get_keywords(soup):
		# get skills
		skills=soup.findAll("span", attrs={"data-skillkey":True})
		# get categories
		categories = soup.findAll(attrs={"data-skill":True})
		keywords =[]
		
		# get text from html
		for skill in skills:
			keywords.append(skill.getText())
		for cat in categories:
			keywords.append(cat.getText())
			
		# get unique values by chaging it to a set
		keywords = set(keywords)
		print keywords
		return keywords

	@staticmethod
	def write_kws_to_csv(keywords, cat):
		output = open("keywords.csv", "a")
		writer = csv.writer(output)
		for kyword in keywords:
			writer.writerow([kyword, cat])



