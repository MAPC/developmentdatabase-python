$(document).ready(function() {
	
	map = new OpenLayers.Map('map');
	
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
		
	map.setCenter(new OpenLayers.LonLat(0, 0), 3);
	
 });