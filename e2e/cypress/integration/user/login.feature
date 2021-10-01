Feature: Test Flash User Login
	Scenario: verify login using valid credentials with user not connected to bank account
		Given there is a registered user without connecting his bank account
		When user visits login page
		And user logs in to system
        Then user will be redirected to "/bank/connect" that verifies he didnt connect his bank account


    Scenario: verify login using valid credentials with user connected to bank account
		Given there is a registered user without connecting his bank account
		And that user has connected his bank account
		When user visits login page
		And user logs in to system
        Then user will be redirected to "/bank/connected" that verifies he has connected his bank account


#TODO: invalid login scenario