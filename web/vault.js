angular.module('vaultapp', ['ui.bootstrap']);
angular.module('vaultapp').controller('mainCtrl', function ($scope, $http) {
	$scope.open = function () {};
  $scope.crypt = function () {
    var data = {password: $scope.password, source: $scope.source};
    var config = { headers : { 'Content-Type': 'application/json;charset=utf-8;' } };
    $http.post('/crypt', data, config)
      .then(function(resp) {
        $scope.result = resp.data.value;
      }, function(resp) {
        $scope.result = resp.data.value;
      });
  };
  $scope.copy = function () {
    var textarea = document.getElementById('result');
    textarea.setSelectionRange(0, textarea.value.length);
    console.log(textarea.value.length);
    try {
      var s = document.execCommand('copy');
      console.log(s);
    } catch (err) {
      console.log('Oops, unable to copy');
    }
  };
});
