angular.module('waitress')
  .service('offlineDetectorService', offlineDetectorService);

offlineDetectorService.$inject = ['$state'];

/**
* Controller That takes care of the slackservice
@param {service} $state, $state service
@return {void}
*/
function offlineDetectorService($state) {
  return function() {
    if (!navigator.onLine) {
      $state.go('dashboard.error');
    }
    else {
      console.log('continue');
    }
  };

}
