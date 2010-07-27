var CC = {
	baseurl: "/",
	map: {}, // the map
	symbolizer: {}, // icons
	styles: {}, // map styles
	projection: {}, // Projections
	layer: {}, // OL layers
	featurecollection: {},
	markers: {},
	section: {}, // site section
	project: {} // project to edit
}

function init(section) {
	
	CC.projection.WGS84 = new OpenLayers.Projection('EPSG:4326');
	CC.projection.OSM = new OpenLayers.Projection('EPSG:900913');
	
	// format to read from geodjango
	CC.geojson = new OpenLayers.Format.GeoJSON();
	
	CC.map = new OpenLayers.Map ('map', {
		controls:[
			new OpenLayers.Control.Navigation(),
			new OpenLayers.Control.PanZoom(),
			new OpenLayers.Control.LayerSwitcher(),
			new OpenLayers.Control.Attribution()],
		projection: CC.projection.OSM,
		displayProjection: CC.projection.WGS84,
	});
	
	CC.layer.osm = new OpenLayers.Layer.OSM(
		"OpenStreetMap"
	);
	
	CC.map.addLayers([CC.layer.osm]);
	
	// default center
	CC.map.setCenter(new OpenLayers.LonLat(-71.08, 42.34).transform(CC.projection.WGS84, CC.projection.OSM), 9);
	
	switch (section) {
		case "index":
			CC.section.project_list();
			CC.section.town_taz();
	  		break;
		case "project_detail":
			CC.section.project_detail();
			break;
		case "project_list":
			CC.section.project_list();
	  		break;	
		case "project_locate":
			CC.section.project_locate();
			CC.section.town_taz();
		  	break;
		default:
			CC.map.setCenter(new OpenLayers.LonLat(-71.08, 42.34).transform(CC.projection.WGS84, CC.projection.OSM), 9);
	}
}

CC.section.town_taz = function () {
		
	CC.layer.taz = new OpenLayers.Layer.Vector("TAZ", {
		format: OpenLayers.Format.GeoJSON
		// styleMap: CC.styles.projects
	});
	
	// FIXME: ajax loading with OL (loadend event)
	$.getJSON(CC.baseurl + CC.town + "/taz/geojson/", function(data) {
  		CC.featurecollection.taz = data;
		CC.layer.taz.addFeatures(CC.geojson.read(CC.featurecollection.taz));		
		// CC.map.zoomToExtent(CC.layer.taz.getDataExtent());
	});

	CC.map.addLayers([CC.layer.taz]);	
}

CC.section.project_list = function () {

	CC.layer.projects = new OpenLayers.Layer.Vector("Projects", {
		format: OpenLayers.Format.GeoJSON,
		// styleMap: CC.styles.projects
	});
	
	CC.layer.projects.addFeatures(CC.geojson.read(CC.featurecollection.projects));
	
	CC.map.addLayers([CC.layer.projects]);
	
	CC.map.zoomToExtent(CC.layer.projects.getDataExtent());

}

CC.section.project_detail = function () {
	
	CC.layer.project = new OpenLayers.Layer.GML(CC.project.title, CC.baseurl + "project/" + CC.project.id + "/geojson/", {
		format: OpenLayers.Format.GeoJSON,
		projection: CC.map.displayProjection
		// styleMap: CC.styles.projects
	});
	
	CC.map.addLayers([CC.layer.project]);
	
	CC.map.setCenter(CC.project.location.transform(CC.projection.WGS84, CC.projection.OSM), 14);
	
}

CC.section.project_locate = function () {

	CC.layer.project = new OpenLayers.Layer.Vector("New Project Location");
	
	CC.project.locationLonLat.transform(CC.projection.WGS84, CC.projection.OSM);
	
	CC.project.locationPoint = new OpenLayers.Geometry.Point(CC.project.locationLonLat.lon, CC.project.locationLonLat.lat)
	CC.project.locationFeature = new OpenLayers.Feature.Vector(CC.project.locationPoint);
	
	CC.layer.project.addFeatures([CC.project.locationFeature]);
	CC.map.addLayers([CC.layer.project]);
	
	CC.map.setCenter(CC.project.locationLonLat, 14);
	
	// drag action
	CC.map.addControl(new OpenLayers.Control.MousePosition());
	CC.drag = new OpenLayers.Control.DragFeature(CC.layer.project);
	CC.drag.onComplete = function(f) {

		CC.project.locationLonLat = new OpenLayers.LonLat(CC.project.locationFeature.geometry.x, CC.project.locationFeature.geometry.y).transform(CC.projection.OSM, CC.projection.WGS84);
		
		// write loc coord to hidden geometry field (in WGS84)
		$("#id_location").val("POINT (" + CC.project.locationLonLat.lon + " " +  CC.project.locationLonLat.lat + ")");
	};
	
	CC.map.addControl(CC.drag);
	CC.drag.activate();	
	
}


