angular.module('waitress')
  .factory('slackService', slackService);

slackService.$inject = ['$http', '$q', '$httpParamSerializerJQLike'];

/**
* Controller That takes care of the slackservice
@param {service} $http, $http service
@param {service} $q,
@param {service} $httpParamSerializerJQLike,
@return {void}
*/
function slackService($http, $q, $httpParamSerializerJQLike) {
/**
* Utility method to retrive data from url
@param {string} url, The input url to get data from
@param {object} data, The parameteer passed in from the calling function
@param {service} midday resolved service from ui-router
@return {promise} deffered.promise a promise funciton for the aysnchronous task
*/
  function getData(url, data) {
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
      deffered.resolve(result);
    })
    .catch(function(resp) {
      deffered.reject(resp);
    });

    return deffered.promise;
  }
  var getSlackId = function(id) {
    return getData('http://waitressandela.herokuapp.com/users/' + id + '/retrieve-secure/', {
      passphrase: 'andela2016'});
  };
  var tap = function(slackUserId) {
    return getData('http://waitressandela.herokuapp.com/users/nfctap/', {
      slackUserId: slackUserId
    });
  };

  return {
    getSlackId: getSlackId,
    tap: tap
  };
}
