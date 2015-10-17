#!/usr/bin/python
import github_credentials
from github_monitor import GithubMonitor

monitor = GithubMonitor(github_credentials.username, github_credentials.password)

late_list = monitor.get_late_list()

for assignee in late_list:
  blame = assignee + " hasn't closed:"
  for issue in late_list[assignee]:
    blame += "\n\t"  + issue.title
  print blame
