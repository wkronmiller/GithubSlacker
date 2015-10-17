from github import Github
from datetime import datetime

class GithubMonitor(object):
  
  def __init__(self, username, password):
    self._gh_handle = Github(username, password)

  def get_open_milestones(self):
    import settings
    # Make sure settings are fresh
    settings = reload(settings)
    # Initialize array
    open_milestones = {}
    # Get data from GitHub
    for repo in settings.monitored_repos:
      open_milestones[repo] = []
      for milestone in self._gh_handle.get_organization(settings.monitored_org).get_repo(repo).get_milestones():
        if milestone.state == "open":
          open_milestones[repo].append(milestone)
    return open_milestones

  def get_late_list(self):
    import settings
    settings = reload(settings)
    late_list = {}
    open_milestones = self.get_open_milestones()
    for repo in open_milestones:
      # Iterate over late milestones
      for milestone in open_milestones[repo]:
        if (milestone.due_on != None) and (milestone.due_on < datetime.now()):
          late_issues = self._gh_handle.get_organization(settings.monitored_org).get_repo(repo).get_issues(milestone=milestone, state="open")
          for issue in late_issues:
            assignee = issue.assignee.login
            if assignee in late_list:
              late_list[assignee].append(issue)
            else:
              late_list[assignee] = [issue]
    return late_list

