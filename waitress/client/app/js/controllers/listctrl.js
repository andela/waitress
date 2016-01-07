'use strict';

module.exports = function($scope, $stateParams, User) {
  $scope.character = $stateParams.character;

  // Show loading component
  $scope.loading = true;

  $scope.footerIsVisible = false;

  $scope.selectedUser = undefined;

  $scope.cancel = function() {
    $scope.selectedUser = undefined;
    $scope.footerIsVisible = false;
  }

  $scope.click = function(userId) {
    $scope.selectedUser = userId;
    $scope.footerIsVisible = true;
  }

  User.filter($stateParams.character, function(users) {
    // Make users available to the scope
    $scope.users = users;

    $scope.users = [
      {
        id: 9,
        firstname: "Chidiebere",
        lastname: "Nnadi"
      },
      {
        id: 5,
        firstname: "Femi",
        lastname: "Sule"
      },
    ];
    // Hide loading component
    $scope.loading = false;
  });

  $scope.tap = function(userId) {
    // Show loading component
    $scope.loading = true;

    User.tap(userId, function() {
      $scope.loading = false;
      $scope.cancel();
    })
  };
};
