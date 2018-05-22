Feature: Transaction appears in Explorer
	The Block Explorer should show the previously sent transaction

Background:
	Given I am on the explorer site

@watch
Scenario: Validate explorer shows transaction
	When I browse to the recent transaction page
	Then I should see the transaction appear
	And the amount transferred should be "15"