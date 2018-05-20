var fs = require('fs')

module.exports = function () {
  'use strict';

  this.setDefaultTimeout(300000); // 5 minute default timeout
  
  this.Then(/^I should then see a form confirming my transaction$/, function () {
    let _el = '#confirmTransactionArea'
    browser.waitForVisible(_el, 60000)
  })

  this.When(/^I then click confirmation transaction$/, function () {
    browser.click('#confirmTransaction')
  })

  this.Then(/^I should see shortly after "([^"]*)"$/, function (arg1) {
    let _el = '#transferSuccessMessage'
    browser.waitForVisible(_el, 120000)
    expect(browser.getText(_el)).toEqual(arg1)

    // Write txn hash to file for Explorer test 6
    fs.writeFileSync('/tmp/chimp-TXN_HASH', browser.getText('#confirmedTransferTxnHash'))
  })

};