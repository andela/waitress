'use strict';

module.exports = function($scope, $state, $localForage, MealSession) {
  $scope.stop = function() {
    // MealSession.stop($scope.beforeMidday, $scope.passphrase, function() {
    //
    // });
    $localForage.removeItem('waitressSession').then(function() {
      $state.go('session')
    })
  };
}
