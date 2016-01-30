/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
'use strict';

angular.module('waitress')
.controller('MainController', mainCtrl);

mainCtrl.$inject = ['$scope', '$http', '$ionicPopup', '$log',
        'MealSession', '$state'];

function mainCtrl($scope, $http, $ionicPopup, $log, MealSession, $state) {
  $http.get('http://waitressandela.herokuapp.com/meal-sessions/')
    .then(function (result) {
      $log.debug(result.data.before_midday);
      $scope.beforeMidday = result.data.before_midday;
    });
  $scope.showDialog = function () {
    $scope.data = {};
    $ionicPopup.show({
      template: '<input type="password" ng-model="data.password">',
      title: 'Enter Passphrase here',
      cssClass: 'pass-phrase-dialog',
      scope: $scope,
      buttons: [
        {
          text: '<b>Submit</b>',
          type: 'button-positive',
          onTap: function (e) {
            var data = { before_midday: $scope.beforeMidday,
              passphrase: $scope.data.password
              };
            if (!$scope.data.password) {
              $log.debug("fired");
               e.preventDefault();
            } else {

              $log.debug(data);
              MealSession.start('http://waitressandela.herokuapp.com/meal-sessions/start/', data)
              .then(function(){
                $state.go('tap')
              }).catch(function(){
                $log.debug("error with authentication");
              })

            }
          }
        },
        { text: 'Cancel' }
      ]
  }).then(function (result) {
    $log.debug(result, "checking in");

  });
   };

};
