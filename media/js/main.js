var CC = {
	map: {}, // the map
	symbolizer: {}, // icons
	styles: {}, // map styles
	projection: {}, // Projections
	layer: {}, // OL layers
	featurecollection: {},
	markers: {},
	section: {}
}

function init(section) {
	
	CC.projection.WGS84 = new OpenLayers.Projection('EPSG:4326');
	CC.projection.OSM = new OpenLayers.Projection('EPSG:900913');
	
	// format to read geodjango
	CC.geojson = new OpenLayers.Format.GeoJSON();
	
	CC.map = new OpenLayers.Map ('map', {
		controls:[
			new OpenLayers.Control.Navigation(),
			new OpenLayers.Control.PanZoom(),
			new OpenLayers.Control.LayerSwitcher(),
			new OpenLayers.Control.Attribution()]
	});
	
	CC.layer.osm = new OpenLayers.Layer.OSM(
		"OpenStreetMap"
	);
	
	/*
	var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS",
	    "http://labs.metacarta.com/wms/vmap0?", {layers: 'basic'});
	
	vectors = new OpenLayers.Layer.Vector("Vector Layer");
	
	map.addLayers([wms, vectors]);
	map.addControl(new OpenLayers.Control.LayerSwitcher());
	map.addControl(new OpenLayers.Control.MousePosition());
	
	var point = new OpenLayers.Geometry.Point(0, 0);
    var pointFeature = new OpenLayers.Feature.Vector(point);
	
	vectors.addFeatures(pointFeature);
	
	var drag = new OpenLayers.Control.DragFeature(vectors);
	map.addControl(drag);
	drag.activate();
	*/	
	
	CC.map.addLayers([CC.layer.osm]);
	// CC.map.zoomToMaxExtent();
	// CC.map.setCenter(new OpenLayers.LonLat(-71.08, 42.34).transform(CC.projection.WGS84, CC.projection.OSM), 9);
	
	
	switch (section) {
		case 'project_list':
			CC.section.project_list();
	  		break;
		default:
			CC.map.setCenter(new OpenLayers.LonLat(-71.08, 42.34).transform(CC.projection.WGS84, CC.projection.OSM), 9);
	}
}

CC.section.project_list = function () {

	CC.layer.projects = new OpenLayers.Layer.Vector("Projects", {
		format: OpenLayers.Format.GeoJSON
		// styleMap: CC.styles.projects
		});
	
	CC.layer.projects.addFeatures(CC.geojson.read(CC.featurecollection.projects));
	
	CC.map.addLayers([CC.layer.projects]);
	
	CC.map.zoomToExtent(CC.layer.projects.getDataExtent());

}


