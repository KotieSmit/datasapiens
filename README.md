
# **QA automation homework assignment**

### Description
Pytest as the test runner and Playwright from Microsoft as the webdriver was used for this assignment. 

### Approch taken
The application under test is stateless or with no backend.  I did build state as the tests progressed, but is not something one would or should do when you have a larger application to test.  Building state make tests dependant on the previous test, and you can not implement selective or parrallel testing later.

1. Basic signup and attempted duplicate signup was covered.
2. New user can login
3. Adding of budgets and their entries
4. Deleting of budget entries and validating totals
5. Deletion of a budget with entries and validate totals

### Running the tests

Building the container:
`docker-compose up -d`

Executing tests:
*(base-url defaults to http://localhost:3567)*
`docker exec -it automation_tests pytest`

if the application under test is available on a different url or port use below. For example:
`docker exec -it automation_tests pytest --base-url http://localhost:3000`

NOTE: *url must be in a 'http://' format*


### Note to reviewer
The qa-webapp, when running in docker, had errors in the console and an iframe overlaying the entire screen.  When running directly without docker, no errors or iframe were present.  

To overcome this, you will see code like this in a few places. `self.page.eval_on_selector('iframe', 'el => el.setAttribute("hidden", "")')`.  This code hides the iframe, and make the elements accessable for interaction. This is something that normally SHOULD not be done without understanding the cause of it, as this might be an issue landing in production.

