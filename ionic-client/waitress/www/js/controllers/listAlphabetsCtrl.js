angular.module('waitress')
  .controller('ListAlphabetsController', ListAlphabetsController);
ListAlphabetsController.$inject = ['$scope'];

function ListAlphabetsController($scope) {
  $scope.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');

}
