angular.module('nfcFilters', [])
    .filter('bytesToHexString', function() {
        return function (input) {
            if (window.nfc) {
                return nfc.bytesToHexString(input);
            } else {
                return input;
            }
        }
    })

    .filter('bytesToString', function() {
        return function(input) {
            if (window.nfc) {
                return nfc.bytesToString(input);
            } else {
                return input;
            }
        };
    })

    .filter('tnfToString', function() {

        function tnfToString(tnf) {
            var value = tnf;

            switch (tnf) {
                case ndef.TNF_EMPTY:
                    value = "Empty";
                    break;
                case ndef.TNF_WELL_KNOWN:
                    value = "Well Known";
                    break;
                case ndef.TNF_MIME_MEDIA:
                    value = "Mime Media";
                    break;
                case ndef.TNF_ABSOLUTE_URI:
                    value = "Absolute URI";
                    break;
                case ndef.TNF_EXTERNAL_TYPE:
                    value = "External";
                    break;
                case ndef.TNF_UNKNOWN:
                    value = "Unknown";
                    break;
                case ndef.TNF_UNCHANGED:
                    value = "Unchanged";
                    break;
                case ndef.TNF_RESERVED:
                    value = "Reserved";
                    break;
            }
            return value;
        }

        return function(input) {

            if (window.ndef) {
                return tnfToString(input);
            } else {
                return input;
            }

        };
    })

    .filter('decodePayload', function() {

        function decodePayload(record) {

            var payload,
                recordType = nfc.bytesToString(record.type);

            if (recordType === "T") {
                payload = ndef.textHelper.decodePayload(record.payload);

            } else if (recordType === "U") {
                payload = ndef.uriHelper.decodePayload(record.payload);

            } else {

                // we don't know how to translate this type, try and print it out.
                // your app should know how to process tags it receives

                var printableData = record.payload.map(function(i) {
                    if (i <= 0x1F) {
                        return 0x2e; // unprintable, replace with "."
                    } else {
                        return i;
                    }
                });

                payload = nfc.bytesToString(printableData);
            }

            return payload;
        }

        return function(input) {

            if (window.nfc) {
                return decodePayload(input);
            } else {
                return input.payload;
            }

        };
    });