#!/usr/bin/python  
# -*- coding: utf-8 -*-  

'''
Created on 2013-4-1

@author: ghy459

@my blog: http://hack0nair.me
'''

from urllib import request
from urllib import parse
import configparser,codecs,re,json,time,Login,sys,time


class Tieba_Sign(object):
	"""docstring for Sign"""
	def __init__(self):
		super(Tieba_Sign, self).__init__()
		self._LOGIN = Login.Baidu_Login()
		self._IS_LOGIN()
		self._HEADERS = self._LOGIN._HEADERS
		self._OPENER = self._LOGIN._OPENER
		self._INI_FILE = self._LOGIN._INI_FILE
		self._TIEBA_NAME = []
		self._TIEBA_TBS = []

		#self.load_ini_file()
		#self.get_tieba_tbs()
		#self.sign(self._TIEBA_NAME[1],self._TIEBA_TBS[1])

	def _IS_LOGIN(self) :

		if self._LOGIN.login() != '0' :
			print ("\n登录失败！请检查config.ini文件中用户名和密码是否正确！\n")
			sys.exit(1)
		else :
			print ("\n登录成功！\n")

	def load_ini_file(self) :
		
		filename = self._INI_FILE
		config = configparser.ConfigParser()
		config.read(filename,encoding = 'utf-8-sig')
		section = 'TIEBA'
		for option in config.options(section):
			t = config.get(section,option)
		self._TIEBA_NAME.extend(t.split(','))

	def load_input_name(self,t) :

		self._TIEBA_NAME.extend(t.split(','))

	def trans_to_gbk(self,name) :

		return parse.quote(name.encode('gbk'))

	def get_tieba_tbs(self) :

		for tieba in self._TIEBA_NAME :
			url = 'http://tieba.baidu.com/f?kw='+self.trans_to_gbk(tieba)
			resp = self._OPENER.open(url).read().decode('gb18030')
			s = r'PageData.tbs = \"(\w+)\"'
			t = re.findall(s,resp)[0]
			self._TIEBA_TBS.append(t)
			
	def sign(self,name,tbs) :

		url = 'http://tieba.baidu.com/sign/add'
		data = {}
		data.update(kw=name,tbs=tbs,ie='utf-8')
		postdata = parse.urlencode(data)
		postdata = postdata.encode('utf-8')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req).read().decode('utf-8')

		result = json.loads(resp)
		no = result['no']
		error = result['error']
		print ("====================")
		if no == 0 :
			result = result['data']['uinfo']
			print ("贴吧 : %s" % name)
			print ("签到状态 : 签到成功！")
			print ("个人签到排名 : %s" % result['user_sign_rank'])
			print ("连续签到天数 : %s" % result['cont_sign_num'])
			print ("本月累计签到天数 : %s" % result['cout_total_sing_num'])
			print ("====================")
		else :
			print ("贴吧 : %s" % name)
			print ("签到失败 : %s" % error)
			print ("错误代码 : %d" % no)
			print ("====================")

	def get_tieba_list(self) :

		url='http://tieba.baidu.com/i/sys/enter?ie=utf-8&kw=' + self.trans_to_gbk(self._LOGIN._LOGIN_DATA['username'])
		r=r'\$_likeForum=(.*?);'
		resp = self._OPENER.open(url).read().decode('gbk')
		t = re.findall(r,resp)[0]
		j = json.loads(t)
		print ("%s 喜欢的贴吧 :" % self._LOGIN._LOGIN_DATA['username'])
		for i in j :
			self._TIEBA_NAME.append(i['name'])
			print (i['name'])

	def sign_all(self) :
		
		self.get_tieba_tbs()
		for i in range(len(self._TIEBA_NAME)) :
			self.sign(self._TIEBA_NAME[i],self._TIEBA_TBS[i])
			time.sleep(2)
		
