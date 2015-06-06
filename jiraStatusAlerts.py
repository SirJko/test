#!/usr/bin/python

# INSTALL PACKAGES

# PIP, PYTHON, BOTO

import sys
import requests
import json
import boto.ses
import datetime
import cStringIO

# VARIABLES

assignee = "Jassef Torres"
usr = 'jtorres'
pwd = 'Jassef1!'
host = 'https://koupon.atlassian.net/rest/api/2/search?jql='

# URLS AND JQLS

#test_url = host+'assignee in ("'+assignee+'")&fields=key"'
tickets_ready_for_merge = host+'project = KPN AND status = "Ready for Merge" AND fixVersion != Backlog and updatedDate > 2015-06-01 ORDER BY fixVersion DESC, key ASC'
tickets_resolved = host+'project = KPN AND status = Resolved AND fixVersion != Backlog AND updatedDate > 2015-06-02 ORDER BY fixVersion DESC'
tickets_qa = host+'project = KPN AND status = "Pending Certification" AND fixVersion != Backlog ORDER BY fixVersion DESC'

urls_list = [tickets_ready_for_merge,tickets_resolved, tickets_qa]

# DICT

tickets = { 'ready': [], 'resolved' : [], 'qa' : [] }

# METHODS

def make_request (url):
	response = requests.get(url, auth=(usr,pwd))
	return response.json()["issues"]

def create_email_body (jresponse):
	output = cStringIO.StringIO()
	output.write("Summary of Jira Tickets as of now "+datetime.datetime.now().strftime("%m/%d/%Y-%I:%M%p")+"\n")
	for key,values in jresponse.items():
		if len(values) != 0:
			output.write("\nThe ticket is in state: " + key)
			for i in range (len(values)):
				output.write("\n"+values[i]["key"])
	message = output.getvalue()
	output.close()
	return message

# MAIN

tickets['ready'] = make_request(tickets_ready_for_merge)
tickets['resolved'] = make_request(tickets_resolved)
tickets['qa'] = make_request(tickets_qa)

if not (len(tickets['ready']) == 0 and len(tickets['resolved']) == 0 and len(tickets['qa']) == 0):

	# CONNECTION TO AWS SES
	conn = boto.ses.connect_to_region('us-east-1')

	# SEND EMAIL
	try:
		conn.send_email(
	        'operations@kou.pn',
	        'Jira Tickets on '+datetime.datetime.now().strftime("%m/%d/%Y-%I:%M%p"),
	        create_email_body(tickets),
	        ['jtorres@kou.pn'])
	except:
		print "Unexpected error:", sys.exc_info()[0]
		raise
