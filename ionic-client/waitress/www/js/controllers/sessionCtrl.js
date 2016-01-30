'use strict';

angular.module('waitress')
.controller('MainController', mainCtrl);

mainCtrl.$inject = ['$scope', '$log', 'midday'];
/**
* Dialog Directive controller
@param {service} $scope, This controlls the scope
@param {serice} $log, for debugging purposes
@param {service} midday resolved service from ui-router
@return {void}
*/
function mainCtrl($scope, $log, midday) {
  $scope.beforeMidday = midday.data.before_midday;
}
