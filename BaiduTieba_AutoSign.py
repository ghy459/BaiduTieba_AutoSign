#!/usr/bin/python  
# -*- coding: utf-8 -*-  

'''
Created on 2013-4-1

@author: ghy459

@my blog: http://hack0nair.me
'''

import Sign,Login
from optparse import OptionParser
import sys

def usage():
	
	usage = "%prog [options] [ -a | -c | -t tieba_name ] " 
	parser = OptionParser(usage,version="BaiduTieba_AutoSign v1.0")
	parser.add_option("-a",action="store_true", dest="a",help="签到“我喜欢的贴吧”")
	parser.add_option("-c",action="store_true", dest="c",help="签到'config.ini'中的贴吧")
	parser.add_option("-t",type="string",dest="tieba_name",help="签到指定的贴吧，多个贴吧用逗号隔开,如: -t dota,dota2")

	(options, args) = parser.parse_args()

	d = {'a':'0','c':'0','t':'0'}

	if options.a == True :
		d['a'] = '1'
	if options.c == True :
		d['c'] = '1'
	if options.tieba_name != '' :
		d['t'] = options.tieba_name

	return d


if __name__ == '__main__':
	
	op = usage()
	print ("\n欢迎使用百度贴吧签到器，程序正在启动中...")
	AutoSign = Sign.Tieba_Sign()
	print ("\n正在签到中，请耐心等待...\n")

	if op['a'] == '1' :
		AutoSign.get_tieba_list()
		AutoSign.sign_all()
		print ("\n签到完毕！\n")
		sys.exit(0)

	if op['c'] == '1' :
		AutoSign.load_ini_file()
		AutoSign.sign_all()
		print ("\n签到完毕！\n")
		sys.exit(0)

	if op['t'] != '' :
		AutoSign.load_input_name(op['t'])
		AutoSign.sign_all()
		print ("\n签到完毕！\n")
		sys.exit(0)


