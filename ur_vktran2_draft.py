#!/usr/bin/env python3
'''
OPS435 Assignment 2 - Fall 2020
Program: ur_vktran2.py
Author: Victor Tran
The python code in this file ur_vktran2.py is original work written by
Victor Tran. No code in this file is copied from any other source 
including any person, textbook, or on-line resource except those provided
by the course instructor. I have not shared this python file with anyone
or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and violators 
will be reported and appropriate action will be taken.
'''

import os
import sys
import time
import argparse
 
def form_dict(file_name):
	''' docstring for this function
	open the file from cli
	read each file from the file
	format the lines into a dictionary to be called on'''
	f = open(file_name, 'r')
	lists = list(f)
	f.close

	n_list = []
	p_list = []
	h_list = []
	f_logon = []
	l_logon = []
	length = []
	dictionary = {}

	for line in lists:
		lis = line.split()
		n_list.append(lis[0])
		p_list.append(lis[1])
		h_list.append(lis[2])
		f_logon.append(lis[3] + ' ' + lis[4] + ' ' + lis[5] + ' ' + lis[6] + ' ' + lis[7])
		l_logon.append(lis[9] + ' ' + lis[10] + ' ' + lis[11] + ' ' + lis[12] + ' ' + lis[13])
		length.append(lis[14])
	dictionary['name'] = n_list
	dictionary['points'] = p_list
	dictionary['hosts'] = h_list
	dictionary['first logon'] = f_logon
	dictionary['last logon'] = l_logon
	dictionary['length'] = length
	return dictionary

def user_list():
	''' docstring for this function
	get the dictionary from the last command
	filter out unwanted records
	format the output '''

	return u_list

def host_list():
	'''docstring for this function
	get the dictionary from the last command
	filter out unwanted records
	format the output'''


if __name__ == '__main__':

	parser = argparse.ArgumentParser(description="Retrieve specified information from files")
	parser.add_argument("-l", "--listing", type=str, choices=['user','host'], help="generate user name or remote host IP from the given files")
	parser.add_argument("-r", "--rhost", help="usage report for the given remote host IP")
	parser.add_argument("-t","--type", type=str, choices=['daily','weekly'], help="type of report: daily or weekly")
	parser.add_argument("-u", "--user", help="usage report for the given user name")
	parser.add_argument("-v","--verbose", action="store_true",help="turn on output verbosity")
	parser.add_argument("files",metavar='F', type=str, nargs='+',help="list of files to be processed")
	args=parser.parse_args()

	file_list = args.files

	if args.verbose:
		print('Files to be processed:',file_list)
		print('Type of args for files',type(file_list))
	if (args.listing == "host"):
		for file_name in file_list:
			x = form_dict(file_name)
			print(x['name'])
	if args.user:
		print('usage report for user:',args.user)
	if args.rhost:
		print('usage report for remote host:',args.rhost)
	if args.type:
		print('usage report type:',args.type)

