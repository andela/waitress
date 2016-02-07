angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', '$cordovaToast','slackService'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, $cordovaToast, slackService) {
  var tag = {};
  var init = function() {

    $ionicPlatform.ready(function() {
      if ($window.nfc) {
        nfc.addNdefListener(function(nfcEvent) {
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
          $rootScope.$apply(function() {
            angular.copy(nfcEvent.tag, tag);
            var slackId = $filter('decodePayload')(tag.ndefMessage[0]);
            slackService.tap(slackId).then(function(resp) {
              $cordovaToast.show(resp.data.firstname + ' ' + resp.data.lastname + ' tapped successfully',
                'long', 'bottom');
            })
            .catch(function(err) {
              if (err.status === 400) {
                $cordovaToast.show(err.data.firstname +
                ' ' + err.data.lastname + ' has already tapped', 'long', 'bottom');
              }
            });
          });
        },
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
      alert("got here");
      if(window.nfc) {
        nfc.removeNdefListener(function(nfcEvent) {
        console.log('last event removed', nfcEvent)}, function(){
          console.log('success')},
          function() {
            console.log('failed');
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

