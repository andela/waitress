(function () {

  'use strict';

  require('angular');
  require('angular-ui-router');
  require('angular-animate');
  require('angular-toastr');
  require('angular-localforage');

  var mainCtrl = require('./controllers/mainctrl');
  var listCtrl = require('./controllers/listctrl');
  var sessionCtrl = require('./controllers/sessionctrl');
  var headerCtrl = require('./controllers/headerctrl');

  var userFactory = require('./services/user');
  var mealSessionFactory = require('./services/mealsession');

  angular.module('WaitressApp', ['ui.router', 'ngAnimate', 'toastr', 'LocalForageModule'])

  .config([
    '$urlRouterProvider',
    '$stateProvider',
    '$locationProvider',
    function($urlRouterProvider, $stateProvider, $locationProvider) {
      $locationProvider.html5Mode(true);

      // routes
      $urlRouterProvider.otherwise("/")
      $stateProvider
        .state('session', {
          url: '/',
          templateUrl: './client/dist/partials/session.html',
          controller: 'SessionController'
        })
        .state('start', {
          url: '/start',
          templateUrl: './client/dist/partials/start.html',
          controller: 'MainController'
        })
        .state('list', {
          url: '/list/:character',
          templateUrl: './client/dist/partials/list.html',
          controller: 'ListController'
        });
    }
  ])

  .run(['$rootScope', '$localForage', '$state', 'MealSession', function($rootScope, $localForage, $state, MealSession) {
    $rootScope.$on('$stateChangeStart', function(e, toState, toParams, fromState, fromParams) {
      MealSession.which(function(res) {
        $rootScope.beforeMidday = res.before_midday;
        var today = moment().format("YYYY-MM-DD");
        $localForage.getItem('waitressSession').then(function(current) {
          if (current) {
            if (current.date === today && current.before == $rootScope.beforeMidday) {
              if (toState.name === 'session') {
                $state.go('start');
              }
            } else {
              $localForage.removeItem('waitressSession').then(function() {
                // Stop session from backend
                if (toState.name !== 'session') {
                  $state.go('session');
                }
              });
            }
          } else {
            if (toState.name !== 'session') {
              $state.go('session');
            }
          }
        });
      });
    });
  }])

  //Load Factories
  .factory('User', ['$http', userFactory])
  .factory('MealSession', ['$http', mealSessionFactory])

  // Load Controllers
  .controller('MainController', ['$scope', mainCtrl])
  .controller('ListController', ['$scope', '$stateParams', 'toastr', 'User', listCtrl])
  .controller('HeaderCtrl', ['$scope', '$state', '$localForage', 'toastr', 'MealSession', headerCtrl])
  .controller('SessionController', ['$scope', '$state', '$localForage', 'toastr', 'MealSession', sessionCtrl])

}());
