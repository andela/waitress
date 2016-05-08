angular.module('waitress')
  .controller('dashboardController', dashboardCtrl);
dashboardCtrl.$inject = ['$scope', '$state', '$ionicHistory'];

function dashboardCtrl($scope, $state, $ionicHistory) {
  $scope.logout = function() {
    $state.go('index');
    $ionicHistory.clearHistory();
  };
  $scope.reload = function() {
      $state.go($state.current, {}, {reload: true});
    };
}