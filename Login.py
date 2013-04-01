#!/usr/bin/python  
# -*- coding: utf-8 -*-  

'''
Created on 2013-3-31

@author: ghy459

@my blog: http://hack0nair.me
'''

from urllib import request
from urllib import parse
from http import cookiejar
import configparser
import re,codecs


class Baidu_Login(object):
	"""docstring for Baidu_Login"""
	def __init__(self):
		super(Baidu_Login, self).__init__()
		self._LOGIN_DATA = {}
		self._HEADERS = {
						"Accept": "Accept:text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
						"Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
						"Accept-Language": "zh-CN,zh;q=0.8",
						"Content-Type": "application/x-www-form-urlencoded",
						'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.94 Safari/537.4',
						"Connection": "Keep-Alive",
						"Cache-Control": "no-cache",
						}
		self._INI_FILE = 'config.ini'
		self._CJ=cookiejar.CookieJar()
		self._OPENER = request.build_opener(request.HTTPCookieProcessor(self._CJ))
		request.install_opener(self._OPENER)
		self.load_ini_file()
		self.get_login_token()

	def load_ini_file(self) :

		filename = self._INI_FILE
		config = configparser.ConfigParser()
		config.read(filename,encoding = 'utf-8-sig')
		section = 'LOGIN'
		for option in config.options(section):
			self._LOGIN_DATA[option] = config.get(section,option)

	def get_login_token(self) :

		req1 = request.Request('https://passport.baidu.com/v2/?login')
		req2 = request.Request('https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=false')
		resp1 = self._OPENER.open(req1)
		resp2 = self._OPENER.open(req2).read().decode('utf-8')
		s=r'login_token=\'(\w+)\''
		t = re.findall(s,resp2)[0]
		self._LOGIN_DATA.update(token=t)

	def login(self) :

		url = 'https://passport.baidu.com/v2/api/?login'
		postdata = parse.urlencode(self._LOGIN_DATA)
		postdata = postdata.encode('utf-8')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req).read().decode('utf-8')
		s=r'error=(\w+)'
		t = re.findall(s,resp)[0]
		return t


