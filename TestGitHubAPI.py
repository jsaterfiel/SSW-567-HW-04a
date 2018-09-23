# -*- coding: utf-8 -*-
"""
Tests for GIT HUB API file

This file uses the json data from test-data/ folder.
The files are the same as the url forward path with the slashes replaced with #
as that's the only character that's valid for windows file names.

Also the print function is being overridden so that we can capture the output from the function.
"""
import unittest
import json
from unittest import TestCase
from unittest.mock import patch, call
from GitHubAPI import printUserRepos
from os import listdir
from os.path import isfile, join

testData = dict()
for f in listdir('test-data'):
  fname = join('test-data', f)
  if isfile(fname):
    fileObj = open(fname, 'r')
    testData[fname] = json.loads(fileObj.read())
    fileObj.close()

def mocked_requests_get(*args, **kwargs):
  """mocked_requests_get is used for intercepting the requests in the function
  so that we can test them without worrying about api limitations
  """
  class MockResponse:
    def __init__(self, json_data, status_code):
      self.json_data = json_data
      self.status_code = status_code

    def json(self):
      return self.json_data
  
  if args[0] == "https://api.github.com/users/bad-request/repos":
    return MockResponse(None, 500)

  fileName = 'test-data/' + args[0].replace('https://api.github.com/','').replace('/','#') + '.json'
  if fileName in testData:
    return MockResponse(testData[fileName], 200)
  return MockResponse({"message": "Not Found", "documentation_url": "https://developer.github.com/v3/repos/#list-user-repositories"}, 404)

class TestGitHubAPI(TestCase):
    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('GitHubAPI.print')
    def testBasic(self, print_, reqs_):
      printUserRepos('richkempinski')
      self.assertEqual(print_.call_args_list, 
        [
          call('Repo: hellogitworld Number of commits: 30'),
          call('Repo: helloworld Number of commits: 2'),
          call('Repo: Project1 Number of commits: 2'),
          call('Repo: threads-of-life Number of commits: 1')
        ],
        "invalid results for userID 'richkempinski'")
      self.assertEqual(reqs_.call_args_list,
        [
          call('https://api.github.com/users/richkempinski/repos'),
          call('https://api.github.com/repos/richkempinski/hellogitworld/commits'),
          call('https://api.github.com/repos/richkempinski/helloworld/commits'),
          call('https://api.github.com/repos/richkempinski/Project1/commits'),
          call('https://api.github.com/repos/richkempinski/threads-of-life/commits')
        ], "invalid calls for requests when getting 'richkempinski'")

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('GitHubAPI.print')
    def testUnknownUserId(self, print_, reqs_):
      printUserRepos('sdflkjsdflkjsdflkjsdflkjsdflkjsdlfkjsdflkjsdlkjsdf')
      self.assertEqual(print_.call_args_list, [call('UserID not found')], "userID error check")
      self.assertEqual(reqs_.call_args_list, [call('https://api.github.com/users/sdflkjsdflkjsdflkjsdflkjsdflkjsdlfkjsdflkjsdlkjsdf/repos')])

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('GitHubAPI.print')
    def testNoReposForUser(self, print_, reqs_):
      printUserRepos('sdfsdfsdfsdfsdfsdf')
      self.assertEqual(print_.call_args_list, [], "no repos should have been found for the user")
      self.assertEqual(reqs_.call_args_list, [call('https://api.github.com/users/sdfsdfsdfsdfsdfsdf/repos')])

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('GitHubAPI.print')
    def testBadResponses(self, print_, reqs_):
      printUserRepos('bad-request')
      self.assertEqual(print_.call_args_list, [call('Cannot contact github')], "bad request so no results expected")
      self.assertEqual(reqs_.call_args_list, [call('https://api.github.com/users/bad-request/repos')])

if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()
