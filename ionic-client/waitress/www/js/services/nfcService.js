angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', 'slackService', '$cordovaToast'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, slackService, $cordovaToast) {
  self.write = false;
  function listenToTag(nfcEvent) {
    if (self.write) {
      slackService.getSlackId(105).then(function(resp) {
      var record = ndef.textRecord(resp.data.slack_id);
        nfc.write(
        [record],
        function() {
          $rootScope.$apply(function() {
            $ionicPopup.alert({
              title: 'Successfully',
              template: 'wrote to tag'
            });
          });
        },
        function(reason) {
          $rootScope.$apply(function() {
            $ionicPopup.alert({
              title: 'failed',
              template: 'there was an error ' + reason
            });
          });
        }
      );
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
          console.log('closed popup', res);
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
        $cordovaToast.show('listening to nfc', 'short', 'top');
      },
      function(reason) {
        $cordovaToast.show('there was an error ' + reason, 'short', 'top');
      });
    }
    });
  };
  var removeListener = function() {
    if (window.nfc) {
      nfc.removeNdefListener(listenToTag,
        function() {
          $cordovaToast.show('Stopped Listening to nfc', 'short', 'top');
        },
        function() {
          $cordovaToast.show('There was an error', 'short', 'top');
        });
    }
  };
  return {
    remove: removeListener,
    init: init
  };
}

