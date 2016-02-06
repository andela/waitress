/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
angular.module('waitress')
    .controller('dailyReportController', dailyReportController);

dailyReportController.$inject = ['$scope', 'dailyReports'];

function dailyReportController($scope, dailyReports) {
    $scope.reports = dailyReports.data[0];
}
