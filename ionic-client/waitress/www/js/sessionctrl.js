'use strict';

angular.module('waitress')

.controller('MainController', ['$scope','$http','$ionicPopup', mainCtrl]);


function mainCtrl($scope, $http,$ionicPopup) {
  $http.get('/').success(function(result){
    console.log("this was fired");
    $scope.beforeMidday = result.before_midday;
  });
  console.log("this was logged");
  function startTime() {
    var today = new Date();
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    var a = checkPeriod(h);
    h = checkHour(h);
    m = checkTime(m);
    s = checkTime(s);
    var clockElem = document.getElementById('live-clock');
    if (clockElem)
      clockElem.innerHTML = h + ":" + m + ":" + s + " " + a;

    var t = setTimeout(startTime, 500);
  }

  function checkHour(i) {
    return i > 12 ? i - 12 : i
  }
 
  function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
  }

  function checkPeriod(i) {
    return i >= 12 ? "PM" : "AM";
  }

  startTime();

  var _nextAction = undefined;

  $scope.passphrase = "";
  $scope.passphraseDialogVisible = false;

  // $scope.start = function() {
  //   console.log('ydhfd');
  //   MealSession.start($scope.beforeMidday, $scope.passphrase, function(res) {
  //     if (res.status == "Invalid passphrase") {
  //       toastr.error('Invalid Passphrase!');
  //     } else {
  //       $localForage.setItem('waitressSession', {
  //         date: moment().format("YYYY-MM-DD"),
  //         before: $scope.beforeMidday
  //       }).then(function() {
  //         toastr.success('Session started!');
  //         $scope.clearDialog();
  //         window.location = '/start';
  //       });
  //     }
  //   });
  // };
   $scope.show = function(){ $ionicPopup.show({
    template: '<input type="password" ng-model="passphrase">',
    title: 'Enter Passphrase here',
    cssClass: 'passphraseDialog',
    scope: $scope,
    buttons: [
      {
        text: '<b>Submit</b>',
        type: 'button-positive',
        onTap: function(e) {
          e.preventDefault();
          if (!$scope.passphrase) {
            $scope.passphrase.$setValidity('invalid',false);
            return false;
            //don'$ht allow the user to close unless he enters wifi password
            
          } else {
            $http.post('').then(function(result){
              //if success
              if(result.status === 'authorized')
                $state.go('home');
            })
          }
        }
      },
      { text: 'Cancel' }
    ]
  }).then(function(result){
    console.log("looged");
  });
}

  $scope.secureAction = function(action) {
    _nextAction = action;
    $scope.show()
  };

  $scope.processAction = function() {
    switch (_nextAction) {
      case 'start':
        $scope.start()
        break;
      case 'stop':
        $scope.stop()
        break;
      default:
        break;
    }
  }

  $scope.clearDialog = function() {
    $scope.passphrase = "";
    $scope.passphraseDialogVisible = false;
  }

};
