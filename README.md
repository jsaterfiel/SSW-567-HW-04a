[![build status of master](https://travis-ci.org/jsaterfiel/SSW-567-HW-04a.svg?branch=HW05a_Mocking)](https://travis-ci.org/jsaterfiel/SSW-567-HW-04a)

# SSW-567-HW-04a
SSW 567 Homework 04a

The unit tests use cached data in the test-data/ folder.

This allows for consistent testing without having to worry about changes in the api making the test cases more brittle or less able to test the results.

Also there is no worry about the api rate limit using cached data.

Best practice is refresh the cached data when any major work occurs on the api or have a specific test case run less frequently that just checks if a static api call remains the same as a way of being alerted to api changes.