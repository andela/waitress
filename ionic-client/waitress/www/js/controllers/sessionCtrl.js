'use strict';

angular.module('waitress')
.controller('sessionController', mainCtrl);

mainCtrl.$inject = ['$scope', '$log', 'midday', '$state'];
/**
* Dialog Directive controller
@param {service} $scope, This controlls the scope
@param {service} $log, for debugging purposes
@param {service} midday resolved service from ui-router
@return {void}
*/
function mainCtrl($scope, $log, midday, $state) {
  $scope.beforeMidday = midday.data.before_midday;
  $scope.reload = function() {
      $state.go($state.current, {}, {reload: true});
    };
}
