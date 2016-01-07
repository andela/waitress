module.exports = function($http) {

  var User = {};

  /**
   * @namespace User
   * @desc Filter users based on first character in their name
   * @memberOf Factories.User
   */
  User.filter = function(character, cb) {
    if(!character) {
      return false;
    }

    var params = {
      filter: character
    };

    $http.get('/users', { params: params })
    .then(function(res) {
      cb(res)
      console.log("Done");
    }, function(res) {
      cb()
      console.log("Done");
    });
  };

  /**
   * @namespace User
   * @desc Tap a user
   * @memberOf Factories.User
   */
  User.tap = function(userId, cb) {
    var url = '/users/' + userId + '/tap'

    $http.get(url)
    .then(function(res) {
      cb(res)
    }, function(res) {
      cb()
    });
  };

  /**
   * @namespace User
   * @desc Untap a user
   * @memberOf Factories.User
   */
  User.untap = function(userId, passphrase, cb) {
    var url = '/users/' + userId + '/untap';

    var data = {
      passphrase: passphrase
    }

    $http.post(url, { data: data })
    .then(function(res) {
      cb(res)
    }, function() {
      cb()
    });
  }

  return User;
}
