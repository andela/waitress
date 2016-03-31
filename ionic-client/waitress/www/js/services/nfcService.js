angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', 'slackService', '$cordovaToast'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, slackService, $cordovaToast) {
  self.write = false;
  var cardIndex = 164;

  function listenToTag(nfcEvent) {
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
    if (self.write) {
      slackService.getSlackId(cardIndex).then(function(resp) {
      var record = ndef.textRecord(resp.data.slack_id);
        nfc.write(
        [record],
        function() {
          cardIndex++;
          $rootScope.$apply(function() {
            showAlert('This tag now belongs to ' +
              resp.data.firstname + ' ' + resp.data.lastname);
          });
          // nfc.makeReadOnly(function() {
          //   alert('This tag is now read only please save the information displayed');
          // }, function(reason) {
          //   alert('there was an error obviously with the readonly ' + reason);
          // });
        },
        function(reason) {
          $rootScope.$apply(function() {
           showAlert('there was an error ' + reason, true);
          });
        }
      );
      });
    } else {
      $rootScope.$apply(function() {
        var slackId = $filter('decodePayload')(nfcEvent.tag.ndefMessage[0]);
        slackService.tap(slackId).then(function(resp) {
          showAlert(resp.data.firstname + ' ' +
            resp.data.lastname + ' tapped successfully');
        })
        .catch(function(err) {
          if (err.status === 400) {
            showAlert(err.data.firstname + ' ' +
              err.data.lastname + ' has already tapped', true);
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

