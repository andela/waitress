'use strict';

module.exports = function($scope, $stateParams, toastr, User) {
  $scope.character = $stateParams.character;

  // Show loading component
  $scope.loading = true;

  $scope.footerIsVisible = false;

  $scope.selectedUser = undefined;

  var _nextAction = undefined;

  $scope.passphrase = "";
  $scope.passphraseDialogVisible = false;

  $scope.cancel = function() {
    $scope.selectedUser = undefined;
    $scope.footerIsVisible = false;
  }

  $scope.click = function(user) {
    $scope.selectedUser = user;
    $scope.footerIsVisible = true;
  }

  User.filter($stateParams.character, function(users) {
    // Make users available to the scope
    $scope.users = users;

    // Hide loading component
    $scope.loading = false;
  });

  $scope.tap = function() {
    // Show loading component
    $scope.loading = true;

    User.tap($scope.selectedUser.id, function(res) {
      $scope.users.forEach(function(user, i) {
        if(user.id == $scope.selectedUser.id)
          $scope.users[i].is_tapped = true
      })
      toastr.success('Tap Successful!');
      $scope.loading = false;
      $scope.cancel();
    })
  };


  $scope.untap = function() {
    User.untap($scope.selectedUser.id, $scope.passphrase, function(res) {
      if (res.status == "Invalid passphrase") {
        toastr.error('Invalid Passphrase!');
      } else {
        $scope.users.forEach(function(user, i) {
          if(user.id == $scope.selectedUser.id)
            $scope.users[i].is_tapped = false
        })
        toastr.success('Untap Successful!');
        $scope.loading = false;
        $scope.clearDialog();
        $scope.cancel();
      }
    })
  }

  $scope.secureAction = function(action) {
    _nextAction = action;
    $scope.showPassphraseDialog();
  };

  $scope.processAction = function() {
    switch (_nextAction) {
      case 'untap':
        $scope.untap()
        break;
      default:
        break;
    }
  }

  $scope.showPassphraseDialog = function() {
    $scope.passphraseDialogVisible = true;
  }

  $scope.clearDialog = function() {
    $scope.passphrase = "";
    $scope.passphraseDialogVisible = false;
    $scope.cancel();
  }
};
