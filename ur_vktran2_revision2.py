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
import copy
import sys
import datetime, time
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
	full_time = []
	l_logon = []
	length = []
	dictionary = {}
	months = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6', 'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

	for line in lists:# iterate through each line in the list of lines
		lis = line.split() # split the lines by whitespace
		n_list.append(lis[0]) # append values that will be put into the created dictionary
		p_list.append(lis[1])
		h_list.append(lis[2])
		f_logon.append(lis[7] + ' ' + months[lis[4]] + ' ' + lis[5])
		full_time.append(lis[3] + ' ' + lis[4] + ' ' + lis[5] + ' ' + lis[6] + ' ' + lis[7] + ' - ' + lis[9] + ' ' + lis[10] + ' ' + lis[11] + ' ' + lis[12] + ' ' + lis[13])
		l_logon.append(lis[13] + ' ' + months[lis[10]] + ' ' + lis[11])
		length.append(lis[14])
	dictionary['names'] = n_list # assign the values to their respective keys
	dictionary['points'] = p_list
	dictionary['hosts'] = h_list
	dictionary['first logon'] = f_logon
	dictionary['last logon'] = l_logon
	dictionary['full time'] = full_time
	dictionary['length'] = length
	return dictionary

def norm_time(rec):
	'''docstring for this function
	Get the time record
	Check if the start and end time and in the same day, if not create another record
	Return the created records'''
	start = [rec[4:7],rec[8:10],rec[20:24]]
	end = [rec[31:34],rec[35:37],rec[47:52]]
	jday = time.strftime('%j',time.strptime(' '.join(start),'%b %d %Y'))
	jday2 = time.strftime('%j',time.strptime(' '.join(end), '%b %d %Y'))
	if jday == jday2:
		norm_rec = []
		norm_rec.append(copy.copy(rec))
		return norm_rec
	else:
		# calculate next day string in 'WoD Month Day HH:MM:SS YYYY'
		new_rec1 = copy.copy(rec)
		new_rec = copy.copy(rec)
		t_next = time.mktime(time.strptime(' '.join(new_rec1[4:6]+rec[7:8]),'%b %d %Y'))+86400
		next_day = time.strftime('%a %b %d %H:%M:%S %Y',time.strptime(time.ctime(t_next))).split()
		new_rec1[12] = '23:59:59'
		new_rec1[9] = new_rec1[3]
		new_rec1[10] = new_rec1[4]
		new_rec1[11] = new_rec1[5]
		new_rec[3] = next_day[0] # Day of week Sun, Mon, Tue...
		new_rec[4] = next_day[1] # Month Jan, Feb, Mar, ...
		new_rec[5] = next_day[2] # Day of Month 01, 02, ...
		new_rec[6] = next_day[3] # Time HH:MM:SS
		new_rec[7] = next_day[4] # Year YYYY
		norm_rec = normalized_rec(new_rec)
		normalized_recs = copy.copy(norm_rec)
		normalized_recs.insert(0,new_rec1)  # call normalized_rec function recursive
	return normalized_recs

def user_list(records, file_list):
	''' docstring for this function
	get the dictionary from the last command
	filter out unwanted records
	format and print output '''
	x = print("User list for file(s)", file_list)
	y = print('=========================================')
	newList = list(dict.fromkeys(records['names'])) #turn list into dictionary and back to remove duplicate names
	for z in newList:
		print(z)
	return x,y

def host_list(records, file_list):
	'''docstring for this function
	get the dictionary from the last command
	filter out unwanted records
	format and print output'''
	x = print("Host list for file(s)", file_list)
	y = print('=========================================')
	newList = list(dict.fromkeys(records['hosts'])) # turn list into dictionary and back to remove duplicate hosts
	for z in newList:
		print(z)
	return x, y

def daily_user(records, username):
	'''docstring for this function
	Get dictionary from the last command
	Search for the specified user
	output the date and uptime for the specified user'''
	x = print('Daily report for user ', username)
	y = print('=========================================')
	start = -1
	locations = []
	dates = []
	times = []
	new_list = []
	hms = '%H:%M:%S'

	while True: #continuously loop
		try:
			loc = records['names'].index(username,start+1) # iterate each record looking for given username
		except ValueError: #break the continuous loop  when there os a value error
			break
		else:
			locations.append(loc) #save the indexes or the username
			start = loc #resume from last location

	for inx in locations:
		dates.append(records['first logon'][inx])
		n = norm_time(str(records['full time'][inx]))
		print(n)
		for a in n:
			f = datetime.datetime.strptime(a[38:46], hms) - datetime.datetime.strptime(a[11:19], hms)
			times.append(f.total_seconds())
		
	print(dates, '     ', times)
	return x, y



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
	user = args.user

	for file_name in file_list: # create for loop to create a dictionary for all files in arg.files
		y = form_dict(file_name)

		if args.verbose:
			print('Files to be processed:',file_list)
			print('Type of args for files',type(file_list))
		if (args.listing == 'host'):
			host_list(y,file_list)
		if (args.listing == 'user'):
			user_list(y,file_list)
		if args.user:
			print('usage report for user:', user)
			daily_user(y, user)
		if args.rhost:
			print('usage report for remote host:',args.rhost)
		if args.type:
			print('usage report type:',args.type)


