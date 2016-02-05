angular.module('waitress')
  .controller('CustomReportController', customReportController);

customReportController.$inject = ['$scope', '$filter', 'MealSession'];

function customReportController($scope, $filter, MealSession) {
    var defaultProps = {
      todayLabel: 'Today',
      closeLabel: 'Close',
      setLabel: 'Set',
      setButtonType: 'button-assertive',
      todayButtonType: 'button-assertive',
      closeButtonType: 'button-assertive',
      inputDate: new Date(),
      mondayFirst: true,
      showTodayButton: 'true',
      modalHeaderColor: 'bar-positive',
      modalFooterColor: 'bar-positive',
      from: new Date(2015, 12, 1),
      to: new Date(),
      closeOnSelect: false
    };
//   $scope.$watchGroup(['fromDate.inputDate', 'toDate.inputDate'], function(newValues, oldValues, scope) {
//     console.log(newValues);
//     console.log(oldValues);
// });
  $scope.currentDate = new Date();
  $scope.dateFormat = 'yyyy-MM-dd';
  $scope.fromDate = {
    titleLabel: 'Select Start Date',
    callback: function (val) {
      $scope.fromDate.inputDate = val;
    }
  };

  $scope.toDate = {
    titleLabel: 'Select End Date',
    callback: function(val) {
      $scope.toDate.inputDate = val;
    }
  };
  angular.extend($scope.fromDate, defaultProps);
  angular.extend($scope.toDate, defaultProps);

  $scope.report = function() {
    var data = {
      from: $filter('date')($scope.fromDate.inputDate, 'yyyy-MM-dd'),
      to: $filter('date')($scope.toDate.inputDate, 'yyyy-MM-dd')
    };
    MealSession.report(data).then(function(result) {
      $scope.reportData = result.data;
    });
  };
}