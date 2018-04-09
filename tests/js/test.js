
let grpc = require('grpc');
let temp = require('temp').track();
let fs = require("fs-extra");
let qrllib = require('./node_modules/qrllib/build/libjsqrl.js');
var assert = require('assert');
var expect = require('chai').expect

async function fetchRemoteProto(nodeAddr) {
    let protoDescriptor = grpc.load('qrlbase.proto');
    let client = new protoDescriptor.qrl.Base(nodeAddr, grpc.credentials.createInsecure());

    return new Promise( (resolve) => {
        client.getNodeInfo({}, function (err, nodeInfo) {
            if (err) {
                throw err;
            }
            let requiredFile = '/tmp/google/protobuf/timestamp.proto';
            if (!fs.existsSync(requiredFile))
            {
                fs.ensureDirSync('/tmp/google/protobuf');
                fs.copySync('timestamp.proto', requiredFile, { overwrite : true });
            }
            temp.open('proto', (err, info) => {
                if (!err) {
                    fs.write(info.fd, nodeInfo.grpcProto);
                    fs.close(info.fd, function () {
                        let remoteProtoDescriptor = grpc.load(info.path);
                        resolve(remoteProtoDescriptor);
                    });
                }
            });
        });
    });
}

async function getQRLClient(nodeAddr) {
    return new Promise(resolve => {
        const remoteProto = fetchRemoteProto(nodeAddr);
        remoteProto.then(function (remoteProto) {
            let client = new remoteProto.qrl.PublicAPI(nodeAddr, grpc.credentials.createInsecure());
            resolve(client);
        });
    });
}

// StringToBytes from QRLLIB
stringToBytes = (convertMe) => {
  // Convert String to Binary First
  const thisBinary = qrllib.hstr2bin(convertMe)
  // Now convert to Bytes
  return binaryToBytes(thisBinary)
}

// Convert Binary object to Bytes
binaryToBytes = (convertMe) => {
  // Convert Binary to Bytes
  const thisBytes = new Uint8Array(convertMe.size())
  for (let i = 0; i < convertMe.size(); i += 1) {
    thisBytes[i] = convertMe.get(i)
  }
  return thisBytes
}


function toBuffer(ab) {
  const buffer = Buffer.from(ab)
  return buffer
}

// Connecting to the API
// TODO: The IP should change to something running locally for tests
// let qrlClient = getQRLClient('104.251.219.215:9009');
let qrlClient = getQRLClient('35.177.60.137:9009');


// Concatenates multiple typed arrays into one.
concatenateTypedArrays = (resultConstructor, ...arrays) => {
    let totalLength = 0
    for (let arr of arrays) {
      totalLength += arr.length
    }
    let result = new resultConstructor(totalLength)
    let offset = 0
    for (let arr of arrays) {
      result.set(arr, offset)
      offset += arr.length
    }
    return result
}


// Take input and convert to unsigned uint64 bigendian bytes
toBigendianUint64BytesUnsigned = (input) => {
  if(!Number.isInteger(input)) {
    input = parseInt(input)
  }

  const byteArray = [0, 0, 0, 0, 0, 0, 0, 0]

  for ( let index = 0; index < byteArray.length; index ++ ) {
    const byte = input & 0xff
    byteArray[index] = byte
    input = (input - byte) / 256
  }

  byteArray.reverse()

  const result = new Uint8Array(byteArray)
  return result
}




// initiating the test wallets to use
var testfromaddress = '0105006d232eb403a0248f9d4c0476c06a7d7a1d0425420df2dd915b7fb46cf7da132699c27b93'
var testfromxmsspk = '0105007e41c011a706c8edd8d1a2f18d558d14311917cd549b3edae07775b12d6640ef35ea0d4dd47fc36e2bc6d5aa5f6ef7582fcf6b8a564ea0ff3af3b42af05cbac9'
var testtoaddress = '0105003e32fcbcdcaf09485272f1aa1c1e318daaa8cf7cd03bacf7cfceeddf936bb88efe1e4d21'
var testfromaddress_bytes = stringToBytes(testfromaddress);
var testfromxmsspk_bytes = stringToBytes(testfromxmsspk);
var testtoaddress_bytes = stringToBytes(testtoaddress);



// Test for GetNodeState
describe('GetNodeState', function() {
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getNodeState({}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    response = res;
                    resolve();
                });
            });
        });
    });
    it('GetNodeStateResp has NodeInfo *info* property', function(){
        expect(response).to.have.property('info');
    });
    it('GetNodeStateResp.info has correct *state* property', function(){
        expect(response.info).to.have.property('state');
        expect(response.info.state).to.be.a('string');
        expect(response.info.state).to.be.oneOf(['UNKNOWN', 'UNSYNCED', 'SYNCING', 'SYNCED', 'FORKED']);
    });
    it('GetNodeStateResp.info has correct *version* property', function(){
        expect(response.info).to.have.property('version');
        expect(response.info.version).to.be.a('string');
    });
    it('GetNodeStateResp.info has correct *num_connections* property', function(){
        expect(response.info).to.have.property('num_connections');
        expect(response.info.num_connections).to.be.a('number');
        expect(response.info.num_connections).to.be.below(4294967297); // uint32
    });
    it('GetNodeStateResp.info has correct *num_known_peers* property', function(){
        expect(response.info).to.have.property('num_known_peers');
        expect(response.info.num_known_peers).to.be.a('number');
        expect(response.info.num_known_peers).to.be.below(4294967297); // uint32
    });
    it('GetNodeStateResp.info has correct *uptime* property', function(){
        expect(response.info).to.have.property('uptime');
        expect(response.info.uptime).to.be.a('string');
        expect(parseInt(response.info.uptime)).to.be.a('number');
        expect(parseInt(response.info.uptime)).to.be.below(18446744073709551617); // uint64
    });
    it('GetNodeStateResp.info has correct *block_height* property', function(){
        expect(response.info).to.have.property('block_height');
        expect(response.info.block_height).to.be.a('string');
        expect(parseInt(response.info.block_height)).to.be.a('number');
        expect(parseInt(response.info.block_height)).to.be.below(18446744073709551617); // uint64
    });
    it('GetNodeStateResp.info has correct *block_last_hash* property', function(){
        expect(response.info).to.have.property('block_last_hash');
        expect(typeof(response.info.block_last_hash)).to.equal('object');
        expect(Buffer.isBuffer(response.info.block_last_hash)).to.equal(true);
    });
    it('GetNodeStateResp.info has correct *network_id* property', function(){
        expect(response.info).to.have.property('network_id');
        expect(response.info.network_id).to.be.a('string');
    });
});


// Test for getKnownPeers
// describe('GetKnownPeers', function() {
//     let response;
//     // call API
//     before(function() {
//         return new Promise((resolve) => {
//             qrlClient.then( function (qrlClient) {
//                 qrlClient.GetKnownPeers({}, (err, res) => {
//                     if (err){
//                         console.log("Error: ", err.message);
//                         return;
//                     }
//                     console.log(res)
//                     response = res;
//                     resolve();
//                 });
//             });
//         });
//     });
//
//     it('GetAddressStateResp has AddressState state property', function(){
//         expect(response).to.have.property('state');
//     });
// });



// Test for getStats
describe('GetStats', function() {
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getStats({include_timeseries: true}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    response = res;
                    resolve();
                });
            });
        });
    });
    it('GetStatsResp has NodeInfo *node_info* property', function(){
        expect(response).to.have.property('node_info');
    });
    it('GetStatsResp.node_info has correct *version* property', function(){
        expect(response.node_info).to.have.property('version');
        expect(response.node_info.version).to.be.a('string');
    });
    it('GetStatsResp.node_info has correct *state* property', function(){
        expect(response.node_info).to.have.property('state');
        expect(response.node_info.state).to.be.a('string');
        expect(response.node_info.state).to.be.oneOf(['UNKNOWN', 'UNSYNCED', 'SYNCING', 'SYNCED', 'FORKED']);
    });
    it('GetStatsResp.node_info has correct *num_connections* property', function(){
        expect(response.node_info).to.have.property('num_connections');
        expect(response.node_info.num_connections).to.be.a('number');
        expect(response.node_info.num_connections).to.be.a('number');
        expect(response.node_info.num_connections).to.be.below(4294967297); // uint32
    });
    it('GetStatsResp.node_info has correct *num_known_peers* property', function(){
        expect(response.node_info).to.have.property('num_known_peers');
        expect(response.node_info.num_known_peers).to.be.a('number');
        expect(response.node_info.num_known_peers).to.be.a('number');
        expect(response.node_info.num_known_peers).to.be.below(4294967297); // uint32
    });
    it('GetStatsResp.node_info has correct *uptime* property', function(){
        expect(response.node_info).to.have.property('uptime');
        expect(response.node_info.uptime).to.be.a('string');
        expect(parseInt(response.node_info.uptime)).to.be.a('number');
        expect(parseInt(response.node_info.uptime)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp.node_info has correct *block_height* property', function(){
        expect(response.node_info).to.have.property('block_height');
        expect(response.node_info.block_height).to.be.a('string');
        expect(parseInt(response.node_info.block_height)).to.be.a('number');
        expect(parseInt(response.node_info.block_height)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp.node_info has correct *block_last_hash* property', function(){
        expect(response.node_info).to.have.property('block_last_hash');
        expect(typeof(response.node_info.block_last_hash)).to.equal('object');
        expect(Buffer.isBuffer(response.node_info.block_last_hash)).to.equal(true);
    });
    it('GetStatsResp.node_info has correct *network_id* property', function(){
        expect(response.node_info).to.have.property('network_id');
        expect(response.node_info.network_id).to.be.a('string');
    });
    it('GetStatsResp has correct *epoch* property', function(){
        expect(response).to.have.property('epoch');
        expect(response.epoch).to.be.a('string');
        expect(parseInt(response.epoch)).to.be.a('number');
        expect(parseInt(response.epoch)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *uptime_network* property', function(){
        expect(response).to.have.property('uptime_network');
        expect(response.uptime_network).to.be.a('string');
        expect(parseInt(response.uptime_network)).to.be.a('number');
        expect(parseInt(response.uptime_network)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *block_last_reward* property', function(){
        expect(response).to.have.property('block_last_reward');
        expect(response.block_last_reward).to.be.a('string');
        expect(parseInt(response.block_last_reward)).to.be.a('number');
        expect(parseInt(response.block_last_reward)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *block_time_mean* property', function(){
        expect(response).to.have.property('block_time_mean');
        expect(response.block_time_mean).to.be.a('string');
        expect(parseInt(response.block_time_mean)).to.be.a('number');
        expect(parseInt(response.block_time_mean)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *block_time_sd* property', function(){
        expect(response).to.have.property('block_time_sd');
        expect(response.block_time_sd).to.be.a('string');
        expect(parseInt(response.block_time_sd)).to.be.a('number');
        expect(parseInt(response.block_time_sd)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *coins_total_supply* property', function(){
        expect(response).to.have.property('coins_total_supply');
        expect(response.coins_total_supply).to.be.a('string');
        expect(parseInt(response.coins_total_supply)).to.be.a('number');
        expect(parseInt(response.coins_total_supply)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *coins_emitted* property', function(){
        expect(response).to.have.property('coins_emitted');
        expect(response.coins_emitted).to.be.a('string');
        expect(parseInt(response.coins_emitted)).to.be.a('number');
        expect(parseInt(response.coins_emitted)).to.be.below(18446744073709551617); // uint64
    });
    it('GetStatsResp has correct *block_timeseries* property', function(){
        expect(response).to.have.property('block_timeseries');
        expect(typeof(response.block_timeseries)).to.equal('object');
        response.block_timeseries.forEach(i => expect(i).to.have.all.keys(['number','difficulty','timestamp','time_last','time_movavg','hash_power','header_hash','header_hash_prev']));
        // Difficulty should be a number
        response.block_timeseries.forEach(i => expect(i.difficulty).to.be.a('string'));
    });
    it('GetStatsResp has correct *block_timeseries.number* property: is a uint64', function(){
        response.block_timeseries.forEach(i => expect(i.number).to.be.a('string'));
        response.block_timeseries.forEach(i => expect(parseInt(i.number)).to.be.a('number'));
        response.block_timeseries.forEach(i => expect(parseInt(i.number)).to.be.below(18446744073709551617));
    });
    it('GetStatsResp has correct *block_timeseries.timestamp* property: is a uint64', function(){
        response.block_timeseries.forEach(i => expect(i.timestamp).to.be.a('string'));
        response.block_timeseries.forEach(i => expect(parseInt(i.timestamp)).to.be.a('number'));
        response.block_timeseries.forEach(i => expect(parseInt(i.timestamp)).to.be.below(18446744073709551617));
    });
    it('GetStatsResp has correct *block_timeseries.time_last* property: is a uint64', function(){
        response.block_timeseries.forEach(i => expect(i.time_last).to.be.a('string'));
        response.block_timeseries.forEach(i => expect(parseInt(i.time_last)).to.be.a('number'));
        response.block_timeseries.forEach(i => expect(parseInt(i.time_last)).to.be.below(18446744073709551617));
    });
    it('GetStatsResp has correct *block_timeseries.time_movavg* property: is a uint64', function(){
        response.block_timeseries.forEach(i => expect(i.time_movavg).to.be.a('string'));
        response.block_timeseries.forEach(i => expect(parseInt(i.time_movavg)).to.be.a('number'));
        response.block_timeseries.forEach(i => expect(parseInt(i.time_movavg)).to.be.below(18446744073709551617));
    });
    it('GetStatsResp has correct *block_timeseries.hash_power* property: is a number', function(){
        response.block_timeseries.forEach(i => expect(i.hash_power).to.be.a('number'));
        response.block_timeseries.forEach(i => expect(parseFloat(i.hash_power)).to.be.a('number'));
    });
    it('GetStatsResp has correct *block_timeseries.header_hash* property: is a Buffer composed of 32 octets', function(){
        response.block_timeseries.forEach(i => expect(Buffer.isBuffer(i.header_hash)).to.equal(true));
        response.block_timeseries.forEach(i => expect(i.header_hash.length).to.equal(32));
    });
    it('GetStatsResp has correct *block_timeseries.header_hash_prev* property: is a Buffer composed of 32 octets', function(){
        response.block_timeseries.forEach(i => expect(Buffer.isBuffer(i.header_hash_prev)).to.equal(true));
        response.block_timeseries.forEach(i => expect(i.header_hash_prev.length).to.equal(32));
    });
});



// Test for GetObject for AddressState
describe('GetObject - AddressState', function() {
    // example wallet address
    let response;
    // testaddress = stringToBytes('01050048a8b31d8dda8a25c5c0d02994fe87e54032ba67910657ade9114d0cdff2eeb5f6285446');
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getObject({query : testfromaddress_bytes }, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    // console.log(res)
                    console.log(typeof(res.address_state.ots_bitfield[0]))
                    response = res;
                    resolve();
                });
            });
        });
    });
    it('GetObjectResp has correct *result* property', function(){
        expect(response).to.have.property('result');
        expect(response.result).to.be.a('string');
        expect(response.result).to.equal('address_state');
    });
    it('GetObjectResp has correct *found* property', function(){
        expect(response).to.have.property('found');
        expect(response.found).to.equal(true);
    });
    it('GetObjectResp has correct *transaction* property', function(){
        expect(response).to.have.property('transaction');
        expect(response.transaction).to.equal(null);
    });
    it('GetObjectResp has correct *block_extended* property', function(){
        expect(response).to.have.property('block_extended');
        expect(response.block_extended).to.equal(null);
    });
    it('GetObjectResp has correct *address_state* property', function(){
        expect(response).to.have.property('address_state');
        expect(response.address_state).to.have.all.keys(['address','balance','nonce','ots_bitfield','transaction_hashes','tokens','latticePK_list','slave_pks_access_type','ots_counter']);
    });
    it('GetObjectResp has correct *AdressState.address* property', function(){
        expect(Buffer.isBuffer(response.address_state.address)).to.equal(true);
        expect(response.address_state.address.length).to.equal(39);
        // check the first three octets values are correct
    });
    it('GetObjectResp has correct *AdressState.balance* property', function(){
        expect(response.address_state.balance).to.be.a('string');
        expect(parseInt(response.address_state.balance)).to.be.a('number');
        expect(parseInt(response.address_state.balance)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.nonce* property', function(){
        expect(response.address_state.nonce).to.be.a('string');
        expect(parseInt(response.address_state.nonce)).to.be.a('number');
        expect(parseInt(response.address_state.nonce)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.ots_counter* property', function(){
        expect(response.address_state.ots_counter).to.be.a('string');
        expect(parseInt(response.address_state.ots_counter)).to.be.a('number');
        expect(parseInt(response.address_state.ots_counter)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.ots_bitfield* property', function(){
        response.address_state.ots_bitfield.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.address_state.ots_bitfield.forEach(i => expect(i.length).to.equal(1));
    });
    it('GetObjectResp has correct *AdressState.transaction_hashes* property', function(){
        response.address_state.transaction_hashes.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.address_state.transaction_hashes.forEach(i => expect(i.length).to.equal(32));
    });

});


// Test for GetObject for TransactionExtended
describe('GetObject - TransactionExtended', function() {
    // example wallet address
    let response;
    testtx = stringToBytes('010600e62ec20b7397949a132f7e6efa80ba3fe1e94af646e50035f1db1a5985734fff11284143');
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getObject({query : testtx }, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    // console.log(res)
                    response = res;
                    resolve();
                });
            });
        });
    });

    it('GetObjectResp has correct *result* property', function(){
        expect(response).to.have.property('result');
        expect(response.result).to.equal('address_state');
    });
    it('GetObjectResp has correct *found* property', function(){
        expect(response).to.have.property('found');
        expect(response.found).to.equal(true);
    });
    it('GetObjectResp has correct *transaction* property', function(){
        expect(response).to.have.property('transaction');
        expect(response.transaction).to.equal(null);
    });
    it('GetObjectResp has correct *block_extended* property', function(){
        expect(response).to.have.property('block_extended');
        expect(response.block_extended).to.equal(null);
    });
    it('GetObjectResp has correct *address_state* property', function(){
        expect(response).to.have.property('address_state');
        expect(response.address_state).to.have.all.keys(['address','balance','nonce','ots_bitfield','transaction_hashes','tokens','latticePK_list','slave_pks_access_type','ots_counter']);
    });
    it('GetObjectResp has correct *AdressState.address* property', function(){
        expect(Buffer.isBuffer(response.address_state.address)).to.equal(true);
        expect(response.address_state.address.length).to.equal(39);
        // check the first three octets values are correct
    });
    it('GetObjectResp has correct *AdressState.balance* property', function(){
        expect(response.address_state.balance).to.be.a('string');
        expect(parseInt(response.address_state.balance)).to.be.a('number');
        expect(parseInt(response.address_state.balance)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.nonce* property', function(){
        expect(response.address_state.nonce).to.be.a('string');
        expect(parseInt(response.address_state.nonce)).to.be.a('number');
        expect(parseInt(response.address_state.nonce)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.ots_counter* property', function(){
        expect(response.address_state.ots_counter).to.be.a('string');
        expect(parseInt(response.address_state.ots_counter)).to.be.a('number');
        expect(parseInt(response.address_state.ots_counter)).to.be.below(18446744073709551617); // uint64
    });
    it('GetObjectResp has correct *AdressState.ots_bitfield* property', function(){
        response.address_state.ots_bitfield.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.address_state.ots_bitfield.forEach(i => expect(i.length).to.equal(1));
    });
    it('GetObjectResp has correct *AdressState.transaction_hashes* property', function(){
        response.address_state.transaction_hashes.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.address_state.transaction_hashes.forEach(i => expect(i.length).to.equal(32));
    });
});


// Test for GetAddressState
describe('GetAddressState', function() {
    // example wallet address
    testaddress = stringToBytes('01050048a8b31d8dda8a25c5c0d02994fe87e54032ba67910657ade9114d0cdff2eeb5f6285446');
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getAddressState({address : testaddress}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    // console.log(res)
                    response = res;
                    resolve();
                });
            });
        });
    });

    it('GetAddressStateResp has AddressState state property', function(){
        expect(response).to.have.property('state');
    });
    it('GetAddressStateResp.state has correct *address* property', function(){
        expect(response.state).to.have.property('address');
        expect(Buffer.isBuffer(response.state.address)).to.equal(true);
        expect(response.state.address.length).to.equal(39);
    });
    it('GetAddressStateResp.state has correct *balance* property', function(){
        expect(response.state).to.have.property('balance');
        expect(response.state.balance).to.be.a('string');
        expect(parseInt(response.state.balance)).to.be.a('number');
        expect(parseInt(response.state.balance)).to.be.below(18446744073709551617); // uint64
    });
    it('GetAddressStateResp.state has correct *nonce* property', function(){
        expect(response.state).to.have.property('nonce');
        expect(response.state.nonce).to.be.a('string');
        expect(parseInt(response.state.nonce)).to.be.a('number');
        expect(parseInt(response.state.nonce)).to.be.below(18446744073709551617); // uint64
    });
    it('GetAddressStateResp.state has correct *ots_bitfield* property', function(){
        expect(response.state).to.have.property('ots_bitfield');
        response.state.ots_bitfield.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.state.ots_bitfield.forEach(i => expect(i.length).to.equal(1));
    });
    it('GetAddressStateResp.state has correct *transaction_hashes* property', function(){
        expect(response.state).to.have.property('transaction_hashes');
        response.state.transaction_hashes.forEach(i => expect(Buffer.isBuffer(i)).to.equal(true));
        response.state.transaction_hashes.forEach(i => expect(i.length).to.equal(32));
    });
    it('GetAddressStateResp.state has correct *tokens* property', function(){
        expect(response.state).to.have.property('tokens');
    });
    it('GetAddressStateResp.state has correct *latticePK_list* property', function(){
        expect(response.state).to.have.property('latticePK_list');
    });
    it('GetAddressStateResp.state has correct *slave_pks_access_type* property', function(){
        expect(response.state).to.have.property('slave_pks_access_type');
    });
    it('GetAddressStateResp.state has correct *ots_counter* property', function(){
        expect(response.state).to.have.property('ots_counter');
        expect(response.state.ots_counter).to.be.a('string');
        expect(parseInt(response.state.ots_counter)).to.be.a('number');
        expect(parseInt(response.state.ots_counter)).to.be.below(18446744073709551617); // uint64
    });

});


// rpc GetLatestData(GetLatestDataReq) returns (GetLatestDataResp);
describe('GetLatestData - All', function() {
    // example wallet address
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getLatestData({filter:0 , offset: 10, quantity: 20}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    response = res;
                    resolve();
                });
            });
        });
    });

    it('GetLatestDataResp has correct *blockheaders* property', function(){
        expect(response).to.have.property('blockheaders');
    });
    it('GetLatestDataResp has correct *transactions* property', function(){
        expect(response).to.have.property('transactions');
    });
    it('GetLatestDataResp has correct *transactions_unconfirmed* property', function(){
        expect(response).to.have.property('transactions_unconfirmed');
    });
});


describe('GetLatestData - TransactionExtended', function() {
    // example wallet address
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.getLatestData({filter:0 , offset: 1, quantity: 10}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    response = res;
                    resolve();
                });
            });
        });
    });

    it('GetLatestDataResp has correct *blockheaders* property', function(){
        expect(response).to.have.property('blockheaders');
    });
    it('GetLatestDataResp has correct *transactions* property', function(){
        expect(response).to.have.property('transactions');
    });
    it('GetLatestDataResp has correct *transactions_unconfirmed* property', function(){
        expect(response).to.have.property('transactions_unconfirmed');
    });
});


let transaction_unsigned;
// rpc TransferCoins (TransferCoinsReq) returns (TransferCoinsResp);
describe('TransferCoins', function() {
    let response;
    // call API
    before(function() {
        return new Promise((resolve) => {
            qrlClient.then( function (qrlClient) {
                qrlClient.transferCoins({master_addr: testfromaddress_bytes, addresses_to: testtoaddress_bytes, amounts: 100, fee:0.001, xmss_pk: testfromxmsspk_bytes}, (err, res) => {
                    if (err){
                        console.log("Error: ", err.message);
                        return;
                    }
                    transaction_unsigned = res.extended_transaction_unsigned.tx;
                    response = res;
                    resolve();
                });
            });
        });
    });

    it('TransferCoinsResp has correct *extended_transaction_unsigned* property', function(){
        expect(response).to.have.property('extended_transaction_unsigned');
    });
    it('TransferCoinsResp.extended_transaction_unsigned has correct *header* property', function(){
        expect(response.extended_transaction_unsigned).to.have.property('header');
        expect(response.extended_transaction_unsigned.header).to.equal(null);
    });
    it('TransferCoinsResp.extended_transaction_unsigned has correct *tx* property', function(){
        expect(response.extended_transaction_unsigned).to.have.property('tx');
        expect(response.extended_transaction_unsigned.tx).to.have.property('transactionType');
        expect(response.extended_transaction_unsigned.tx).to.have.property('master_addr');
        expect(Buffer.from(response.extended_transaction_unsigned.tx.master_addr).toString('hex')).to.equal(testfromaddress);
        expect(response.extended_transaction_unsigned.tx).to.have.property('fee');
        expect(response.extended_transaction_unsigned.tx).to.have.property('public_key');
        expect(Buffer.from(response.extended_transaction_unsigned.tx.public_key).toString('hex')).to.equal(testfromxmsspk);
        expect(response.extended_transaction_unsigned.tx).to.have.property('signature');
        expect(response.extended_transaction_unsigned.tx).to.have.property('nonce');
        expect(response.extended_transaction_unsigned.tx).to.have.property('transaction_hash');
        expect(response.extended_transaction_unsigned.tx).to.have.property('transfer');
        expect(response.extended_transaction_unsigned.tx).to.have.property('coinbase');
        expect(response.extended_transaction_unsigned.tx.coinbase).to.equal(null);
        expect(response.extended_transaction_unsigned.tx).to.have.property('latticePK');
        expect(response.extended_transaction_unsigned.tx.latticePK).to.equal(null);
        expect(response.extended_transaction_unsigned.tx).to.have.property('message');
        expect(response.extended_transaction_unsigned.tx.message).to.equal(null);
        expect(response.extended_transaction_unsigned.tx).to.have.property('token');
        expect(response.extended_transaction_unsigned.tx.token).to.equal(null);
        expect(response.extended_transaction_unsigned.tx).to.have.property('transfer_token');
        expect(response.extended_transaction_unsigned.tx.transfer_token).to.equal(null);
        expect(response.extended_transaction_unsigned.tx).to.have.property('slave');
        expect(response.extended_transaction_unsigned.tx.slave).to.equal(null);
    });
    it('TransferCoinsResp.extended_transaction_unsigned has correct *addr_from* property', function(){
        expect(response.extended_transaction_unsigned).to.have.property('addr_from');
        expect(Buffer.from(response.extended_transaction_unsigned.addr_from).toString('hex')).to.equal(testfromaddress);
    });
});
