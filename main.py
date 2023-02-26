#!/usr/bin/env python

from lxml import objectify
from project import Project
from github import Github
import time

def read_xml_sourcefile(file_name):
    all_text = open(file_name).read()
    return objectify.fromstring(all_text)

file_name = input('Path to JIRA XML query file: ')
all_xml = read_xml_sourcefile(file_name)

jira_project = input('JIRA project name to use: ')
gh_account = input('Github account name: ')
gh_project = input('Github project name: ')
gh_token = input('Github access token: ')

project = Project(jira_project)

for item in all_xml.channel.item:
    project.add_item(item)

issues = project.get_issues()
g = Github(login_or_token=gh_token)

repo = g.get_repo(f'{gh_account}/{gh_project}')

for issue in issues:
    repo.create_issue(title=issue['title'], body=issue['body'])
    time.sleep(30)
