
angular.module('waitress')
.directive('myCurrentTime', myCurrentTimeDirective);

myCurrentTimeDirective.$inject = ['$interval', 'dateFilter'];

/**
* Dialog Directive controller
@param {service} $interval sets the time interval to 500 millisecnds
@param {service} dateFilter, Sets the format in which the date would appear
*with a passphrase
@return {void}
*/
function myCurrentTimeDirective($interval, dateFilter) {
  /**
  * Dialog Directive controller
  @param {service} scope, This controlls the isolated scope of the directive
  @param {jqLite} element, controlls what happens on the do
  *with a passphrase
  @return {void}
  */
  function link(scope, element) {
    var timeoutId;
    /**
    * Updates Time
    */
    function updateTime() {
      element.text(dateFilter(new Date(), 'h:mm:ss a'));
    }
    element.addClass('add-margin-top');
    element.on('$destroy', function() {
      $interval.cancel(timeoutId);
    });

    // start the UI update process; save the timeoutId for canceling
    timeoutId = $interval(function() {
      updateTime(); // update DOM
    }, 500);
  }

  return {
    link: link
  };
}