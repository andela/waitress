angular.module('waitress')
  .factory('nfcService', nfcService);

nfcService.$inject = ['$rootScope', '$ionicPlatform',
      '$ionicPopup', '$filter', '$window', '$cordovaToast'];

function nfcService($rootScope, $ionicPlatform, $ionicPopup, $filter, $window, $cordovaToast) {
  var tag = {};
  var init = function() {
    $ionicPlatform.ready(function() {
      if ($window.nfc) {
        nfc.addNdefListener(function(nfcEvent) {
        //   var record = ndef.textRecord('Message of the holly');
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
          $rootScope.$apply(function() {
            angular.copy(nfcEvent.tag, tag);
            $ionicPopup.alert({
              title: 'content',
              template: $filter('decodePayload')(tag.ndefMessage[0])
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
    var removeListener = function(){
      nfc.removeNdefListener(function(nfcEvent){
        console.log('last event removed', nfcEvent)}, function(){
          console.log('success')},
          function(){
            console.log('failed');
          });
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

