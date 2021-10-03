Feature: Test Flash User Login
	Scenario: verify that user can exchange currency rate using base currency
		Given there is a registered user
		When user visits login page
		And user logs in to system
		And user visits currency exchange rate page
		And user selects base currency 'USD'
        Then exchanged rate for currency "EUR" should be "0.8"
		And exchanged rate for currency "EGP" should be "15"
		When user change baes currency to "GBP"
		Then exchanged rate for currency "EUR" should be "1"
		And exchanged rate for currency "EGP" should be "21"