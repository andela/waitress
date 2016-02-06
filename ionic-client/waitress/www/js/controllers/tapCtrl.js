/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
angular.module('waitress')
    .controller('TapController', tapCtrl);

tapCtrl.$inject = ['$scope', 'nfcService'];

/**
* Dialog Directive controller
@param {service} $scope, This controlls the scope
@param {service} nfcService nfcService initialization
@param {sevice} $ionicView ionicvview Service
@return {void}
*/
function tapCtrl($scope, nfcService) {
  nfcService.init();
}
