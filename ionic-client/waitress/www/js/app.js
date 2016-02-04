angular.module('waitress', [
  'ionic',
  'nfcFilters',
  'ngCordova'
])
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if (window.cordova && window.cordova.plugins.Keyboard) {
      // Hide the accessory bar by default (remove this to show the accessory bar above the keyboard
      // for form inputs)
      cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);

      // Don't remove this line unless you know what you are doing. It stops the viewport
      // from snapping when text inputs are focused. Ionic handles this internally for
      // a much nicer keyboard experience.
      cordova.plugins.Keyboard.disableScroll(true);
    }
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider, $logProvider, $ionicConfigProvider) {
  $urlRouterProvider.otherwise('/');
  $ionicConfigProvider.tabs.position('bottom');
  $logProvider.debugEnabled(true);
  $stateProvider
    .state('home', {
      url: '/',
      resolve: {
        midday: ['$http', function($http) {
          return $http({method: 'GET', url: 'http://waitressandela.herokuapp.com/meal-sessions/'});
        }]
      },
      controller: 'MainController',
      templateUrl: 'partials/session.html'
    })
    .state('dashboard', {
      abstract: true,
      url: '/dashboard',
      controller: 'dashboardController',
      templateUrl: 'partials/dashboard.html'
    })
    .state('dashboard.tap', {
      url: '/dashboard/home',
      views: {
        'home-tab': {
          templateUrl: 'partials/tap.html',
          controller: 'TapController'
        }
      }
    })
    .state('dashboard.report', {
      url: 'dashboard/report',
      views: {
        'report-tab': {
          templateUrl: 'partials/report.html'
        }
      }
    })
    .state('dashboard.history', {
      url: 'dashboard/history',
      views: {
        'history-tab': {
          templateUrl: 'partials/history.html'
        }
      }
    })
    .state('dashboard.report-weekly', {
      url: 'dashboard/report/weekly',
      views: {
        'report-tab': {
          templateUrl: 'partials/weekly-report.html'
        }
      }

    });
});

