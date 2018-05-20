var fs = require('fs')

// This file contains steps shared over multiple tests.
module.exports = function() {  
  this.setDefaultTimeout(300000); // 5 minute default timeout
  'use strict';

  /* SHARED */
  this.Then(/^I should see the title as "([^"]*)"$/, function (arg1) {
    expect(browser.getTitle()).toEqual(arg1)
  })

  /* WALLET */
  this.Given(/^I am on the wallet site$/, function () {
    browser.url('http://localhost:3000')
    // Hide top warning bar
    browser.execute(function() {
      document.getElementsByClassName('main-content-warning')[0].style.visibility = 'hidden';
    })
  })

  this.When(/^I click New Wallet$/, function () {
    browser.click('#newWalletButton')
  })

  this.When(/^type a passphrase "([^"]*)" in$/, function (arg1) {
    // For some reason, having a password type input element on the page breaks
    // the tests. This is a hack to change the type of the passphrase input
    // to text such that the walletCode setValue statement works.
    browser.execute(function() {
      // browser context
      passphraseBox = document.getElementById("passphrase");
      passphraseBox.type = "text";
    })

    browser.setValue('#passphrase', arg1)
  })
  
  this.When(/^press Create Wallet$/, function () {
    client.moveToObject('#generate')
    browser.click('#generate')
  })

  this.Then(/^I should see Generating new wallet$/, function () {
    let _el = '#generating'
    // client.moveToObject(_el)
    browser.waitForVisible(_el, 30000)
  })

  this.Then(/^I should then see my wallet details$/, function () {
    let _el = '#newAddressMnemonic'
    browser.waitForText(_el, 30000) // Wait for a mnemonic to appear
  })

  this.Then(/^I should see a loader icon$/, function () {
    let _el = '.loader'
    browser.waitForVisible(_el, 30000)
  })

  this.Then(/^I should see a loading icon$/, function () {
    let _el = '.loading'
    browser.waitForVisible(_el, 30000)
  })

  this.When(/^enter my mnemonic phrase "([^"]*)"$/, function (arg1) {
    // For some reason, having a password type input element on the page breaks
    // the tests. This is a hack to change the type of the passphrase input
    // to text such that the walletCode setValue statement works.
    browser.execute(function() {
        // browser context
        passphraseBox = document.getElementById("passphrase");
        passphraseBox.type = "text";
    })
    
    browser.setValue('#walletCode', arg1)
  })

  // Sending Txn Shared Functions
  this.When(/^enter the fee as "([^"]*)"$/, function (arg1) {
    browser.setValue('#fee', arg1)
  })

  this.When(/^change the OTS Key Index to "([^"]*)"$/, function (arg1) {
    browser.setValue('#otsKey', arg1)
  })

  this.When(/^click confirm$/, function () {
    browser.click('#generateTransaction')
  })

  this.When(/^I then fill in the to address as "([^"]*)"$/, function (arg1) {
    browser.setValue('#to_1', arg1)
  })

  this.When(/^enter the amount as "([^"]*)"$/, function (arg1) {
    browser.setValue('#amounts_1', arg1)
  })

  this.Then(/^I should see "([^"]*)"$/, function (arg1) {
    let _el = '#transferRelayingMsg'
    browser.waitForVisible(_el)
    expect(browser.getText(_el)).toEqual(arg1)
  })

  this.Then(/^I should "([^"]*)"$/, function (arg1) {
    let _el = '#transferFinalTxnStatus'

    browser.waitUntil(function () {
      const thisResult = browser.getText(_el)
      if(thisResult.indexOf(arg1) >=0) {
        return true
      }
    }, 300000, 'expected transaction to be in pending state')
  })

  this.Then(/^shortly after I should see "([^"]*)"$/, function (arg1) {
    let _el = '#transferFinalTxnStatus'

    browser.waitUntil(function () {
      const thisResult = browser.getText(_el)
      if(thisResult.indexOf(arg1) >=0) {
        return true
      }
    }, 300000, 'expected transaction confirmation within 5 minutes')

  })

  /* EXPLORER */
  this.Given(/^I am on the explorer site$/, function () {
    browser.url('http://localhost:3003')
  })

};
