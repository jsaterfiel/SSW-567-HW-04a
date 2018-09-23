# -*- coding: utf-8 -*-
import requests
import argparse

def printUserRepos(userID):
  """printUserRepos prints out the user's repos with the number of commits
  Format: "Repo: <name> Number of commits: <total commits>"""
  r = requests.get('https://api.github.com/users/' + userID + '/repos')
  repos = r.json()
  if not isinstance(repos, list):
    print('UserID not found')
    return
  for repo in repos:
    r = requests.get(repo['commits_url'].replace('{/sha}',''))
    commits = r.json()
    if not isinstance(commits, list):
      continue
    print('Repo: {0} Number of commits: {1}'.format(repo['name'], len(commits)))

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("userID", help="displays the repos for the given userID")
  args = parser.parse_args()
  printUserRepos(args.userID)
