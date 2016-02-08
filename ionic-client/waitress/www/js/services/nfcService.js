angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', 'slackService', '$cordovaToast'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, slackService, $cordovaToast) {
  var tag = {};
  function listenToTag(nfcEvent) {
          // slackService.getSlackId(10).then(function(resp) {
          // var record = ndef.textRecord(resp.data.slack_id);
          //   nfc.write(
          //   [record],
          //   function() {
          //     $rootScope.$apply(function() {
          //       $ionicPopup.alert({
          //         title: 'Successfully',
          //         template: 'wrote to tag'
          //       });
          //     });
          //   },
          //   function(reason) {
          //     $rootScope.$apply(function() {
          //       $ionicPopup.alert({
          //         title: 'failed',
          //         template: 'there was an error ' + reason
          //       });
          //     });
          //   }
          // );
          // });
          var showAlert = function(msg, error) {
            var alertPopup = $ionicPopup.alert({
              title: 'Waitress Says',
              template: msg,
              buttons: [{
                text: 'Ok',
                type: error ? 'button-assertive' : 'button-positive'
              }]
            });
            alertPopup.then(function(res) {
              console.log('Thank you for not eating my delicious ice cream cone', res);
            });
          };
          $rootScope.$apply(function() {
            angular.copy(nfcEvent.tag, tag);
            var slackId = $filter('decodePayload')(tag.ndefMessage[0]);
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
  var init = function() {
    $ionicPlatform.ready(function() {
      if ($window.nfc) {
        nfc.addNdefListener(listenToTag,
      function() {
        $cordovaToast.show('listening to nfc', 'long', 'top');
      },
      function(reason) {
        $cordovaToast.show('there was an error ' + reason, 'long', 'top');
      });
    }
    });
  };
    var removeListener = function() {
      if (window.nfc) {
        nfc.removeNdefListener(listenToTag,
          function() {
          $cordovaToast.show('Stopped Listening to nfc', 'long', 'top');
        },
          function() {
            $cordovaToast.show('There was an error', 'long', 'top');
          });
      }
    };
  return {
    remove: removeListener,
    init: init,
    tag: tag,
    clearTag: function() {
      angular.copy({}, this.tag);
    }
  };
}

