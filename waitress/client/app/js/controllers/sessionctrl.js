'use strict';

module.exports = function($scope, $state, $localForage, MealSession) {
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

  MealSession.which(function(res) {
    $scope.beforeMidday = res.before_midday;
  });

  $scope.secureAction = function(action) {
    _nextAction = action;
    $scope.showPassphraseDialog();
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

  $scope.start = function() {
    MealSession.start($scope.beforeMidday, $scope.passphrase, function(res) {
      if (res.status == "Invalid passphrase") {
        //
      } else {
        $localForage.setItem('waitressSession', {
          date: moment().format("YYYY-MM-DD"),
          before: moment().format("a") === 'am' ? true : false
        }).then(function() {
          $scope.clearDialog();
          $state.go('start');
        });
      }
    });
  };

  $scope.showPassphraseDialog = function() {
    $scope.passphraseDialogVisible = true;
  }

};
