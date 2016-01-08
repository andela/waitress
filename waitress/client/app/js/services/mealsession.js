module.exports = function($http) {

  var MealSession = {};

  var toggleMeal = function(action, beforeMidday, passphrase, cb) {
    var data = $.param({
      before_midday: beforeMidday,
      passphrase: passphrase
    });
    var url = '/meal-sessions/' + action +'/';
    $http({
      method: 'POST',
      url: url,
      data: data,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
    .then(function(res) {
      cb(res.data)
    }, function(res) {
      cb()
    });
  };

  /**
   * @namespace MealSession
   * @desc Find out the meal session to start
   * @memberOf Factories.MealSession
   */
  MealSession.which = function(cb) {
    $http.get('/meal-sessions/')
    .then(function(res) {
      cb(res.data)
    }, function(res) {
      cb()
    });
  };

  /**
   * @namespace MealSession
   * @desc Start a new meal session based on the time
   * @memberOf Factories.MealSession
   */
  MealSession.start = function(beforeMidday, passphrase, cb) {
    toggleMeal('start', beforeMidday, passphrase, cb);
  };

  /**
   * @namespace MealSession
   * @desc Stop the on-going meal session
   * @memberOf Factories.MealSession
   */
  MealSession.stop = function(beforeMidday, passphrase, cb) {
    toggleMeal('stop', beforeMidday, passphrase, cb);
  };

  return MealSession;
}
