/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
'use strict';

angular.module('waitress')
.controller('MainController', mainCtrl);

mainCtrl.$inject = ['$scope', '$http', '$ionicPopup', '$log',
        '$httpParamSerializerJQLike', '$state'];

function mainCtrl($scope, $http, $ionicPopup, $log, $httpParamSerializerJQLike, $state) {
  $http.get('http://waitressandela.herokuapp.com/meal-sessions/')
    .then(function (result) {
      $log.debug(result.data.before_midday);
      $scope.beforeMidday = result.data.before_midday;
  });

   $scope.show = function(){
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
        onTap: function(e) {

          $log.debug($scope.data.password);
          if (!$scope.data.password) {
            $log.debug("not entered")
             e.preventDefault();
          } else {
            var data = {'before_midday':$scope.beforeMidday, 'passphrase':$scope.data.password};
            $log.debug(data);
            $http({
              method: 'POST',
              url:'http://waitressandela.herokuapp.com/meal-sessions/start/',
              data: $httpParamSerializerJQLike(data),
              headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
              }
            }).then(function(result){
                  if(result.data.status){

                    $state.go('tap');
                  }

                }).catch(function(resp){
                  $log.debug(resp);
                })
          }
        }
      },
      { text: 'Cancel' }
    ]
  }).then(function(result){

  });
};

};
