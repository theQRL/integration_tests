Feature: Token appears in Explorer
	The Block Explorer should show the previously created token

Background:
	Given I am on the explorer site

@watch
Scenario: Validate explorer shows token
	When I browse to the recent token creation page
	Then I should see the token appear
	And I should see the token title as "Mocknet Test (MNT)"