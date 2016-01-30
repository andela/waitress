/* eslint strict:0, func-names:0, no-use-before-define:0,
no-param-reassign:0, no-var:0 */
angular.module('waitress')
  .factory('MealSession', mealSessionService);

mealSessionService.$inject = ['$q', '$http', '$httpParamSerializerJQLike'];
/**
* Dialog Directive controller
@param {service} $q, handles the differed promise
@param {serivice} $http, handles the call to http server
@param {service} $httpParamSerializerJQLike, changes Params to serliazable objects
@return {void}
*/
function mealSessionService($q, $http, $httpParamSerializerJQLike) {
  /**
  * Dialog Directive controller
  @param {string} url, designated server url
  @param {object} data, handles the call to http server
  @return {void}
  */
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
    .then(function(result) {
      if (result.data.status) {
        deffered.resolve(result);
      }
    })
    .catch(function(resp) {
      deffered.reject(resp);
    });
    return deffered.promise;
  }
  return {
    start: startService
  };
}
