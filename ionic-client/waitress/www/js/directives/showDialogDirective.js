angular.module('waitress')
  .directive('showDialog', showDialogDirective);

showDialogDirective.$inject = ['$ionicPopup', 'MealSession',
                  '$state', '$log'];
  /**
  * Dialog Directive controller
  *@param {service} $ionicPopup service for the dialog direcitve
  @param {Service} MealSession, This makes a call to the server to start
  *with a passphrase
  @param {provider} $state this provides transition from one of the set state to the other
  @param {provider} $log for debugging purposes
  @return {void}
  */
function showDialogDirective($ionicPopup, MealSession, $state, $log) {
  return {
    scope: {
      beforeMidday: '=midday'
    },
    link: function(scope, el) {
      el.on('click', function() {
        scope.data = {};
        scope.errorMessage = '';
        var dialog = $ionicPopup.show({
          template: '<input type="password" ng-model="data.password">' +
                      '<p class="assertive">{{errorMessage}}</p>',
          title: 'Enter Passphrase here',
          cssClass: 'pass-phrase-dialog',
          scope: scope,
          buttons: [
            {
              text: '<b>Submit</b>',
              type: 'button-positive',
              onTap: function(e) {
                e.preventDefault();
                var data = {before_midday: scope.beforeMidday,
                  passphrase: scope.data.password
                  };
                $log.debug(data);
                if (scope.data.password) {
                  $log.debug(data);
                  MealSession.start('http://waitressandela.herokuapp.com/meal-sessions/start/', data)
                  .then(function() {
                    dialog.close();
                    $state.go('dashboard.tap');
                  }).catch(function(res) {
                    scope.errorMessage = res.statusText;
                  });
                } else {
                  scope.errorMessage = 'password can\'t be blank';
                }
              }
            },
            {text: 'Cancel'}
          ]
        });
      });
    }
  };
}
