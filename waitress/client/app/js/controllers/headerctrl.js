'use strict';

module.exports = function($scope, $state, $localForage, toastr, MealSession) {
  $scope.isVisible = false;

  $localForage.getItem('waitressSession').then(function(current) {
    if(current) {
      $scope.isVisible = true;
    }
  })

  $scope.stop = function() {
    $localForage.getItem('waitressSession').then(function(current) {
      if(current) {
        var before = current.before;
        $localForage.removeItem('waitressSession').then(function() {
          MealSession.stop(before, $scope.passphrase, function() {
            toastr.success('Stopped session!');
            $scope.isVisible = false;
            $state.go('session')
          });
        });
      }
    });
  };
}
