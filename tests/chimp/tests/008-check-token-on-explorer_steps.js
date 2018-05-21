var fs = require('fs')

module.exports = function () {
  'use strict';

  this.When(/^I browse to the recent token creation page$/, function () {
    // Grab txn hash from temp file
    var txnHash = fs.readFileSync('/tmp/chimp-TOKEN_HASH').toString()
    // Browse to txn URL
    browser.url('http://localhost:3003/tx/' + txnHash)
  })

  this.Then(/^I should see the token appear$/, function () {
    let _el = '#txnPageSegment'
    browser.waitForVisible(_el, 20000)
  })

  this.Then(/^I should see the token title as "([^"]*)"$/, function (arg1) {
    let _el = '#tokenTitle'
    browser.waitForVisible(_el, 20000)
    expect(browser.getText(_el)).toEqual(arg1)
  })
};