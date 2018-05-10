var fs = require('fs')

module.exports = function () {
  'use strict';

  this.setDefaultTimeout(300000); // 5 minute default timeout

  this.Then(/^I should then see my new address on the page$/, function () {
    let _el = '#walletAddress'
    // All time for gRPC call to be made and reply with data for view state.
    browser.waitForText(_el, 30000)
    expect(browser.getText(_el)).toEqual(newAddress)
  })

  this.When(/^I then click Send and Receive$/, function () {4
    client.moveToObject('#sendAndReceiveButton')
    browser.click('#sendAndReceiveButton')
  })

  this.Then(/^I should see my new address$/, function () {
    let _el = '#transferFormFromAddress'

    // All time for gRPC call to be made and reply with data for view state.
    browser.waitForText(_el, 30000)
  })

  this.When(/^I then fill in the to address as "([^"]*)"$/, function (arg1) {
    browser.setValue('#to_1', arg1)
  })

  this.When(/^enter the amount as "([^"]*)"$/, function (arg1) {
    browser.setValue('#amounts_1', arg1)
  })

  this.When(/^enter the fee as "([^"]*)"$/, function (arg1) {
    browser.setValue('#fee', arg1)
  })

  this.When(/^change the OTS Key Index to "([^"]*)"$/, function (arg1) {
    browser.setValue('#otsKey', arg1)
  })

  this.When(/^click confirm$/, function () {
    browser.click('#generateTransaction')
  })

  this.Then(/^I should then see a form confirming my transaction$/, function () {
    let _el = '#confirmTransactionArea'
    browser.waitForVisible(_el, 60000)
  })

  this.When(/^I then click confirmation transaction$/, function () {
    browser.click('#confirmTransaction')
  })

  this.Then(/^I should see "([^"]*)"$/, function (arg1) {
    let _el = '#transferRelayingMsg'
    browser.waitForVisible(_el)
    expect(browser.getText(_el)).toEqual(arg1)
  })

  this.Then(/^I should see shortly after "([^"]*)"$/, function (arg1) {
    let _el = '#transferSuccessMessage'
    browser.waitForVisible(_el, 120000)
    expect(browser.getText(_el)).toEqual(arg1)

    // Write txn hash to file for Explorer test 6
    fs.writeFileSync('/tmp/chimp-TXN_HASH', browser.getText('#confirmedTransferTxnHash'))
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

};