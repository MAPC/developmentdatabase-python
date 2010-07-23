var CC = {
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
	
	switch (section) {
		case "project_list":
			CC.section.project_list();
	  		break;	
		case "project_edit":
			CC.section.project_edit();
	  		break;	
		default:
			CC.map.setCenter(new OpenLayers.LonLat(-71.08, 42.34).transform(CC.projection.WGS84, CC.projection.OSM), 9);
	}
}

CC.section.project_list = function () {

	CC.layer.projects = new OpenLayers.Layer.Vector("Projects", {
		format: OpenLayers.Format.GeoJSON,
		projection: CC.projection.WGS84
		// styleMap: CC.styles.projects
	});
	
	CC.layer.projects.addFeatures(CC.geojson.read(CC.featurecollection.projects));
	
	CC.map.addLayers([CC.layer.projects]);
	
	CC.map.zoomToExtent(CC.layer.projects.getDataExtent());

}

CC.section.project_edit = function () {

	CC.layer.project = new OpenLayers.Layer.GML(CC.project.title, "/project/" + CC.project.id + "/geojson/", {
		format: OpenLayers.Format.GeoJSON,
		projection: CC.map.displayProjection
		// styleMap: CC.styles.projects
	});
	
	CC.map.addLayers([CC.layer.project]);
	
	CC.map.setCenter(CC.project.location.transform(CC.projection.WGS84, CC.projection.OSM), 13);
	
	// drag action
	CC.map.addControl(new OpenLayers.Control.MousePosition());
	CC.drag = new OpenLayers.Control.DragFeature(CC.layer.project);
	CC.map.addControl(CC.drag);
	CC.drag.activate();

}


