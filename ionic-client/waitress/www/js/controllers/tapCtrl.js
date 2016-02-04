/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
angular.module('waitress')
    .controller('TapController', tapCtrl);

tapCtrl.$inject = ['$scope'];

function tapCtrl($scope) {
  $scope.test = 'blank page';
}
