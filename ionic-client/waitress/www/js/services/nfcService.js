angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', 'slackService', '$cordovaToast'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, slackService, $cordovaToast) {
  self.write = false;
/**
* Utility method to generate id of fellows
*/
  function * idMaker() {
    var index = 1;
    while (index < 200) {
      yield index++;
    }
  }
  var gen = idMaker();
  function listenToTag(nfcEvent) {
    if (self.write) {
      var id = gen.next().value;
      slackService.getSlackId(id).then(function(resp) {
      var record = [
        ndef.textRecord(resp.data.slack_id)
      ];
      var failure = function(reason) {
        $rootScope.$apply(function() {
          $ionicPopup.alert({
            title: 'Waitress Says',
            template: 'There was an error writing for ' +
            reason
          });
        });
      };
      var lockSuccess = function() {
        $ionicPopup.alert({
          title: 'Waitress Says',
          template: 'This tag now belongs to ' +
          resp.data.firstname + ' ' + resp.data.lastname
        });
      };
      var lock = function() {
        nfc.makeReadOnly(lockSuccess, failure);
      };
      nfc.write(record, lock, failure);
      //   nfc.write(
      //   [record],
      //   function() {
      //     nfc.makeReadOnly(function() {
      //       $ionicPopup.alert({
      //         title: 'Waitress Says',
      //         template: 'This tag now belongs to ' +
      //         resp.data.firstname + ' ' + resp.data.lastname
      //       });
      //     });
      //     $rootScope.$apply();
      //   },
      //   function(reason) {
      //     $rootScope.$apply(function() {
      //       $ionicPopup.alert({
      //         title: 'Waitress Says',
      //         template: 'There was an error writing for ' +
      //         reason
      //       });
      //     });
      //   }
      // );
      });
    } else {
      var showAlert = function(msg, error) {
        $ionicPopup.alert({
          title: 'Waitress Says',
          template: msg,
          buttons: [{
            text: 'Ok',
            type: error ? 'button-assertive' : 'button-positive'
          }]
        }).then(function(res) {
      });
      };
      $rootScope.$apply(function() {
        var slackId = $filter('decodePayload')(nfcEvent.tag.ndefMessage[0]);
        slackService.tap(slackId).then(function(resp) {
          showAlert(resp.data.firstname + ' ' + resp.data.lastname + ' tapped successfully');
        })
        .catch(function(err) {
          if (err.status === 400) {
            showAlert(err.data.firstname + ' ' + err.data.lastname + ' has already tapped', true);
          }
        });
      });
    }
  }
  var init = function(write) {
    self.write = write;
    $ionicPlatform.ready(function() {
      if ($window.nfc) {
        nfc.addNdefListener(listenToTag,
      function() {
        $rootScope.msgToNfc = 'Listening to Nfc';
        $rootScope.$apply();
      },
      function(reason) {
        $rootScope.msgToNfc = 'There was an error ' + reason;
      });
    }
    });
  };
  var removeListener = function() {
    if (window.nfc) {
      nfc.removeNdefListener(listenToTag,
        function() {

        },
        function() {

        });
    }
  };
  return {
    remove: removeListener,
    init: init
  };
}

