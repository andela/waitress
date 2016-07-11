'use strict';

angular.module('waitress')
.controller('listController', listCtrl);

listCtrl.$inject = ['$scope', 'names', 'User', '$ionicActionSheet', '$cordovaToast'];
/**
* Dialog Directive controller
@param {service} $scope, This controlls the scope
@param {service} $log, for debugging purposes
@param {service} midday resolved service from ui-router
@return {void}
*/
function listCtrl($scope, names, User, $ionicActionSheet, $cordovaToast) {
  $scope.names = names;

  var tapAction = function(user) {
    var buttonText = user.is_tapped ? ' Untap': 'Tap';
    var hideSheet = $ionicActionSheet.show({
      buttons: [
         {text: '<b> Confirm ' + buttonText + ' </b>', user: user}
      ],
      cancelText: 'Cancel',
      cancel: function() {
        hideSheet();
      },
      titleText: buttonText + ' ' + user.firstname + ' ' + user.lastname,
      buttonClicked: function(index, userObj) {
        if (user.is_tapped) {
          return unTap(userObj.user, hideSheet);
        }
        return tap(userObj.user, hideSheet);
      }
    });
    return hideSheet;
  };

  function cleanUp(closeSheet, user, msg, error) {
    if(!error) {
      var index;
      $scope.names.forEach(function(userObj, i) {
        if (userObj.id === user.id) index = i;
      });
      $scope.names[index].is_tapped = !user.is_tapped;
    }
    $cordovaToast.show(msg, 'long', 'top');
    closeSheet();
  }
  function tap(user, closeSheet) {
    User.tap(user.id).then(function() {
      cleanUp(closeSheet, user, 'successfully tapped ' + user.firstname);
    }, function(error) {
      cleanUp(closeSheet, user, 'there was an error ' + error.statusText, error);
    });
  }
  function unTap(user, closeSheet) {
    User.untap(user.id).then(function() {
      cleanUp(closeSheet, user, 'successfully untapped ' + user.firstname);
    }, function(error) {
      cleanUp(closeSheet, user, 'there was an error ' + error.statusText, error);
    });
  }
    $scope.tapAction = function(user) {
      tapAction(user);
    };
}
