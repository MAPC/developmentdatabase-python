// create app namespace
window.dd = window.dd || {};

(function() {

	var Project = Backbone.Model.extend({

		defaults: function() {
			return {
				title: "project title"
			}
		}

	});

	// expose
	window.dd.Project = Project;

}());

$(function(){

	// load projects from server
	// instantiate

	var pUno = new dd.Project()

	console.log(pUno);

});