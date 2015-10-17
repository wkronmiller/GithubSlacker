#!/usr/bin/python
import github_credentials, re
from github_monitor import GithubMonitor

monitor = GithubMonitor(github_credentials.username, github_credentials.password)

from slackbot.bot import Bot, respond_to, listen_to

bot = Bot()

@respond_to("List milestones", re.IGNORECASE)
def milestones(message):
  milestones = monitor.get_open_milestones()
  milestones_message = "Here are the open milestones:\n"
  for repo in milestones:
    for milestone in milestones[repo]:
      print milestone
      milestones_message += "*" + str(milestone.title) + "*"
      milestones_message += "\n> Due: " + milestone.due_on.strftime("%m-%d")
      milestones_message += "\n> Open Issues: " + str(milestone.open_issues) + "\n"
  message.reply(milestones_message)

@respond_to("What's late?", re.IGNORECASE)
def late(message):
  late_list = monitor.get_late_list()
  late_message = "I have compiled a list of todo's:\n"
  for assignee in late_list:
    late_message += "*" + assignee + "* hasn't closed:"
    for issue in late_list[assignee]:
      late_message += "\n> - "  + issue.title
    late_message += "\n"
  message.reply(late_message)

bot.run()
