
angular.module('waitress')
  .service('User', User);

User.$inject = ['$http', '$q', 'slackService', '$httpParamSerializerJQLike'];

/**
* Controller That takes care of the slackservice
@param {service} $state, $state service
@return {void}
*/

function User($http, $q, slackService, $httpParamSerializerJQLike) {
  var User = {};

  /**
   * @namespace User
   * @desc Filter users based on first character in their name
   * @memberOf Factories.User
   */
  User.filter = function(character) {
    var deffered = $q.defer();
    if(!character) {
      return false;
    }
    var params = {
      filter: character
    };

    $http.get('http://waitressandela.herokuapp.com/users/', { params: params })
    .then(function(res) {
      deffered.resolve(res.data);
    }, function(res) {
      deffered.reject(res);
    });
    return deffered.promise;
  };

  /**
   * @namespace User
   * @desc Tap a user
   * @memberOf Factories.User
   */
  User.tap = function(userId) {
    var deffered = $q.defer();

    slackService.getSlackId(userId).then(function(resp) {
      slackService.tap(resp.data.slack_id).then(function(res) {
        deffered.resolve(res.data);
      }, function(err) {
        deffered.reject(err);
      });
    }, function(err) {
      deffered.reject(err);
    })
    return deffered.promise;
  };

  /**
   * @namespace User
   * @desc Untap a user
   * @memberOf Factories.User
   */
  User.untap = function(userId) {
    var url = 'http://waitressandela.herokuapp.com/users/' + userId + '/untap/';
    var deffered = $q.defer();
    var data = $httpParamSerializerJQLike({
      passphrase: 'andela2016'
    });
    $http({
      method: 'POST',
      url: url,
      data: data,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    })
    .then(function(res) {
      deffered.resolve(res.data);
    }, function(res) {
      deffered.reject(res);
    });
    return deffered.promise;
  };

  return User;
}
