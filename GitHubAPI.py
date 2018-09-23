# -*- coding: utf-8 -*-
import requests
import argparse

def printUserRepos(userID):
  """printUserRepos prints out the user's repos with the number of commits
  Format: "Repo: <name> Number of commits: <total commits>"""
  if not isinstance(userID, str):
    print('Input must be a string')
    return
  r = requests.get('https://api.github.com/users/' + userID + '/repos')
  repos = r.json()
  # if nothing returned then we probably cannot contact github
  if repos is None:
    print('Cannot contact github')
    return
  # handle error responses from github with are always objects with a message property
  if not isinstance(repos, list):
    if 'API rate limit exceeded' in repos['message']:
      print('Unable to contact github due to rate limitation')
      return
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
