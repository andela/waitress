(function () {

  'use strict';

  require('angular');
  require('angular-ui-router');
  require('angular-animate');

  var mainCtrl = require('./controllers/mainctrl');
  var listCtrl = require('./controllers/listctrl');

  var userFactory = require('./services/user');

  angular.module('WaitressApp', ['ui.router', 'ngAnimate'])

  .config([
    '$urlRouterProvider',
    '$stateProvider',
    '$locationProvider',
    function($urlRouterProvider, $stateProvider, $locationProvider) {
      $locationProvider.html5Mode(true);

      // routes
      $urlRouterProvider.otherwise("/")
      $stateProvider
        .state('start', {
          url: '/',
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

  //Load controller
  .factory('User', ['$http', userFactory])
  .controller('MainController', ['$scope', mainCtrl])
  .controller('ListController', ['$scope', '$stateParams', 'User', listCtrl]);

}());
