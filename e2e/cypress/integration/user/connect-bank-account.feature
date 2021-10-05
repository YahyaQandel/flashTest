Feature: Test Flash User Can Connect His Bank Account
	Scenario: verify unauthorized user cannot access connect bank page
		Given there is no registered users
		When user visits connect bank page
        Then user will be redirected to "/login"

	Scenario: verify registered user can connect his bank
		Given there is a registered user has no bank account connected
		When user visits login page
		And user logs in to system
		And user visits connect bank page
		And fill bank field "random" and branch name "Maadi" and account number "random" and account holder name "flashTestUser"
		Then user will be redirected to "/bank/connected"
		Then bank name should be "random" and account number should be "random"

	Scenario: verify connect bank form validation
		Given there is a registered user has no bank account connected
		When user visits login page
		And user logs in to system
		And user visits connect bank page
		And user leaves fields empty and presses connect
		Then user will be redirected to "/bank/connect"
		Then form validation spans will be visible

#TODO: required fields validatio