angular.module('nfcFilters', [])
  .filter('decodePayload', function() {
    function decodePayload(record) {
      var payload,
        recordType = nfc.bytesToString(record.type);
      if (recordType === 'T') {
        payload = ndef.textHelper.decodePayload(record.payload);
      } else if (recordType === 'U') {
        payload = ndef.uriHelper.decodePayload(record.payload);
      } else {
      // we don't know how to translate this type, try and print it out.
      // your app should know how to process tags it receives
        var printableData = record.payload.map(function(i) {
          if (i <= 0x1F) {
            return 0x2e;
          }
          return i;
        });
        payload = nfc.bytesToString(printableData);
      }
      return payload;
    }
    return function(input) {
      if (window.nfc) {
        return decodePayload(input);
      }
      return input.payload;
    };
  });
