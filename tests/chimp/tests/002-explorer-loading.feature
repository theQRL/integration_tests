Feature: QRL Explorer is Loading
	The QRL explorer website should load and have the correct title

Background:
	Given I am on the explorer site

@watch
Scenario: Visitor opens homepage
	Then I should see the title as "QRL Block Explorer"