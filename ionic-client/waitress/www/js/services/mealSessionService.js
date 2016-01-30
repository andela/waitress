/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
angular.module('waitress')
  .factory('MealSession', mealSessionService);

mealSessionService.$inject = ['$q', '$http', '$httpParamSerializerJQLike'];

function mealSessionService($q, $http, $httpParamSerializerJQLike) {
  function startService(url, data) {
    var deffered = $q.defer();
    $http({
      method: 'POST',
      url: url,
      data: $httpParamSerializerJQLike(data),
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    .then(function (result) {
      if (result.data.status) {
        deffered.resolve();
      }
    })
    .catch(function (resp) {
      deffered.reject();
    });
    return deffered.promise;
  }
  return {
    start: startService
  };

}