// global dd namespace
window.dd = window.dd || {};

// IIFE pattern
(function(){

    /**** Private */

    var map, projectLayer,

        // Url for AJAX calls
        projectUrl = '/projects/', 

        /*** Search form field settings */

        // Object translating Django lookups (url GET params) to search form fields
        fieldLookups = {
            taz__municipality: 'municipality',
            ddname__icontains: 'ddname',
            projecttype: 'projecttype',
            status: 'status',
            complyr__exact: 'complyr',
            tothu__exact: 'tothu',
            ovr55: 'ovr55',
            pctaffall__exact: 'pctaffall',
            totempl__exact: 'totemp'
        },

        // form field with prepended operator dropdown
        // [0]: int, [1]: float
        operatorFields = [ ['complyr'], ['tothu', 'pctaffall', 'totemp'] ],

        // tooltip fields
        tooltipFields = [
            { 
                id: "complyr",
                title: "Estimated or actual"
             }, { 
                id: "tothu",
                title: "Number of units" 
            }, { 
                id: "pctaffall",
                title: "In percent" 
            },
            {
                id: "totemp",
                title: "MAPC Estimated Employment"
            } 
        ];

    /*** Page Setups */

    // Search Page: requests projects according to options and url params
    function initSearchPage( args ) {
        /* options: 
         * + query object to be passed to searchProjects
        */
        
        var args = args || {};
        var query = args.query || {};

        // add url params to query
        var urlParams = $.url().param();
        // no url params return object with one empty key/value
        delete urlParams[""]; 

        if ( _.isEmpty( urlParams ) === false ) {
            query = urlParams;
        }

        /*** Tweak Search Form UI */

        // Nullable Boolean in Django defaults to "unknown" option
        $("#id_ovr55 option:first-child").before("<option value=''>---------</option>");
        $("#id_ovr55").val("");
        
        _.forEach( tooltipFields, function( field ) {
                // $().tooltip(options)    
            $( "#id_" + field.id ).tooltip( 
                { 
                    title: field.title,
                    placement: "right" 
                });
        });
        
        // prepand operator select to operator form fields
        var operatorHtml = _.template(
            $( "script.operator-select" ).html()
        );

        _.forEach( _.flatten( operatorFields ), function( value ) {

            // jQuery 1.9 being picky about whitespaces 
            // http://stage.jquery.com/upgrade-guide/1.9/#jquery-htmlstring-versus-jquery-selectorstring
            var html = $.trim( operatorHtml( { field: value }) );
            var $operator = $( html );

            // change lookup method in fieldLookups object
            $operator.on( "change", function() {
                var field = $(this).next( "input" ).attr( "name" );
                var lookup = $(this).val();
                var lookups = _.invert( fieldLookups );
                delete fieldLookups[ lookups[field] ];
                fieldLookups[ field + lookup ] = field;
            });

            // add lookup before value field and tweak styling
            $( "#id_" + value )
                .addClass("span2 pull-right")
                .before( $operator );
        });
        
        // update searchform values with url param values
        if (typeof query !== "undefined") {
            
            _.forEach( query, function(value, key) {

                var field = fieldLookups[key] || key.split("__")[0];
                var $field = $( "#id_" + field );
                $field.val( value );
                
                if ( _.contains( operatorFields, field ) === true ) {
                    var lookup = key.split("__")[1]
                    $field.prev( "select" ).val( "__" + lookup );
                }
            
            });
        }

        // search
        $("form.projectfilters .btn[type='submit']").on("click", function( event ) {
            event.preventDefault();
            var formQueryObject = $("form.projectfilters").serializeObject();
            var query = cleanFormQuery( formQueryObject );
            searchProjects( query );
        });

        // reset form
        $("form.projectfilters button.reset").on( "click", function( event ) {
            event.preventDefault();
            $("form.projectfilters").find("input:text, select").val("");
            $("form.projectfilters select.operator").val("__exact");
            var formQueryObject = $("form.projectfilters").serializeObject();
            var query = cleanFormQuery( formQueryObject );
            searchProjects( query );
        });

        // open new project with map zoom and center
        $("#add-project.btn").on( "click", function( event ) {
            event.preventDefault();
            var center = map.getCenter(),
                zoom = map.getZoom();     
            var locationHash =  "#" + [ zoom, center.lat.toFixed(4), center.lng.toFixed(4) ].join("/");
            window.location = $( this ).attr( "href" ) + locationHash;
        });
  
        initMap();
        searchProjects( query );

    }

    // Update Page: drag marker on map, submit form

    function initUpdatePage( args ) {
        console.log( args );
        initMap();
    }

    /*** Mapping */

    // initialize dd.map with basemaps, layercontrol and empty projectLayer
    function initMap( args ) {

        // defaults
        var args = args || {},
            center = args.center || new L.LatLng(42.33, -71.13),
            zoom = args.zoom || 9,
            showLayerControl = ( args.showLayerControl !== false ) ? true : false;
        
        // available basemaps
        var basemaps = {
            mapc: new L.MAPCTileLayer("basemap"),
            bing: new L.BingLayer(dd.BING_API_KEY, "Aerial"),
            osm: new L.TileLayer("http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                maxZoom: 18, 
                attribution: "Map data &copy; OpenStreetMap contributors"
            })
        }
        var basemap = basemaps[args.basemap] || basemaps.mapc;

        map = L.map( "map_canvas", {
            minZoom: 9,
            maxZoom: 17,
            layers: [ basemap ]
        })
        .setView( center, zoom );

        // initialize empty projectlayer
        projectLayer = L.geoJson( null, {
            pointToLayer: function ( feature, latlng ) {
                return L.circleMarker(latlng, {
                    radius: 6,
                    fillColor: "#044388",
                    color: "#fff",
                    weight: 1,
                    opacity: 0.6,
                    fillOpacity: 0.6
                })
            }
            // , onEachFeature: function( feature, layer ) {
            //     layer.bindPopup( popup_html( feature.properties ), {
            //         offset: new L.Point( -18, -20 ) // FIXME: positioning not ideal
            //     } );
            // }
        } ).addTo( map );

        // custom project popup template and click event
        var popupHtml = _.template(
            $( 'script.map-popup' ).html()
        );
        projectLayer.on( "click", function( e ) {
            var popup = L.popup()
                .setLatLng( e.layer.getLatLng() )
                .setContent( popupHtml( e.layer.feature.properties ) )
                .openOn( this._map );
        });

        // layer control
        // FIXME: order?
        if (showLayerControl === true ) {
            var layerControl = new L.Control.Layers( {
                    "MAPC Basemap": basemaps.mapc,
                    "OpenStreetMap": basemaps.osm,
                    "Bing Aerial": basemaps.bing
                }, {
                    "Development Projects": projectLayer
                }
            );
            map.addControl( layerControl );
        }
    
    }

    /*** Data requests */

    // request projects=, add them to projectslayer and zoom map to extent
    function searchProjects( args ) {

        // query object defines GET url (filter) parameters
        var query = args || {};

        $.ajax({
            dataType: "json",
            url: projectUrl,
            data: query,
            success: function ( projects ) {

                projectLayer.clearLayers();

                $("#search-permalink").html( projects.features.length + " " + plural( "project", projects.features.length ) + " found.");
                $("#search-permalink").attr( 'href', "?" + $.param( query ) );

                if (projects.features.length > 0 ) {
                    projectLayer.addData( projects );
                    map.fitBounds( projectLayer.getBounds() );
                } 

            }
        });
    }

    /*** Utilities */

    // modify serialized form to match Django's lookup methods and trigger search
    function cleanFormQuery( query ) {

        // remove properties with empty strings
        query =_.omit( query, function( value ) {
            return value === '';
        });

        // inverse fieldLookups and build query with valid django lookups
        var lookups = _.invert( fieldLookups );
        var lookupQuery = {};
        _.forEach( query, function(value, key) {
            var field = key;
            // make sure type is correct
            if ( _.contains( operatorFields[0], field ) ) {
                value = parseInt( value );
            } else if ( _.contains( operatorFields[1], field ) ) {
                value = parseFloat( value );
            }
            lookupQuery[ lookups[ field ] ] = value;
        });

        return lookupQuery;
    }

    // change string to simple plural depending on given number
    function plural( string, number ) {
        if ( number != 1 ) {
            return string + "s";
        } else {
            return string;
        }

    }

    /**** Public */

    dd.initMap = initMap;
    dd.searchProjects = searchProjects;
    dd.initSearchPage = initSearchPage;
    dd.initUpdatePage = initUpdatePage;

})();

// development database namespace

// var dd = {

//     // number fields in filter form that require number operator
//     number_fields: ["complyr", "tothu", "pctaffall", "totemp"],

//     // percent fields, strip % char and divide by 100 before used in query
//     pct_fields: ["pctaffall", "retpct", "ofcmdpct", "indmfpct", "whspct", "rndpct", "edinstpct", "othpct"],

//     // nullboolean fields
//     nullboolean_fields: ["ovr55"],

//     // related fields
//     related_fields: ["status", "projecttype"],

//     // operators used to filter integer, float, etc. fields
//     // default lookup method for string fields is 'icontains'
//     number_operators: function(number_field) {
//         // TODO: can be done better with an change event that appends the 
//         // correct lookup method to the following DOM (form) element
//         var number_operators = {
//             "lt": "<",
//             "exact": "=",
//             "gt": ">"
//         }

//         var $operators = $("<select />").addClass("operator span1 " + number_field);
        
//         $.each(number_operators, function(key, value) {
//             var option = $("<option />", {
//                 value: "__" + key,
//                 html: value
//             });
//             $operators.append(option);
//         });
        
//         return $operators;
//     },

//     // add previous and next urls to pagination links
//     update_pagination: function(options) {
//         var options = options || {};
//         $(".pagination li").addClass("disabled");

//         $.each(options, function(key, value) {
//             if (value) {
//                 var $button = $(".pagination ." + key);
//                 $button.attr("href", $.url().attr("directory") + "?" + $.url(value).attr("query"));
//                 $button.parent().removeClass("disabled");
//                 $button
//                 .off()
//                 .on("click", function(e) {
//                     e.preventDefault();
//                     dd.load_projects($.url(value).param());
//                 });
//             }
//         });
//     },

//     // load projects based on given url or filter parameters
//     load_projects: function(filter) {
//         var filter = filter || {};
//         filter["format"] = "json";
//         filter["limit"] = (filter["limit"] !== undefined) ? filter["limit"] : 20;
//         filter["order_by"] = filter["order_by"] || "-last_modified";

//         // serialize filter to url
//         var url  = "/api/v1/project/?" + $.param(filter);

//         $.getJSON(
//             url,  
//             function(data) {
//                 if (dd.map) {
//                     // clear projects
//                     dd.projects.clearLayers();

//                     if (data.objects.length > 0) {
//                         //add to map
//                         $.each(data.objects, function(key, project) {
//                             dd.map_project(
//                                 project["location"], 
//                                 {
//                                     "popupContent": "<a href=\"" + project["absolute_url"] + "\">" + project["ddname"] + "</a>"
//                                 }
//                             );
//                         });
//                         dd.map.fitBounds(dd.projects.getBounds());
//                     }

//                     // update pagination buttons
//                     dd.update_pagination({
//                         "next": data.meta["next"],
//                         "previous": data.meta["previous"]
//                     });

//                     $(".countinfo").show();
//                     var page_range = [data.meta.offset];
//                     page_range[1] = (data.meta.limit === 0) ? data.meta.total_count : (parseInt(data.meta.offset) + parseInt(data.meta.limit));
//                     $(".countinfo .range").html(page_range[0] + " - " +  page_range[1]);
//                     $(".countinfo .totalcount").html(data.meta.total_count);
                    
//                     // update permalink
//                     $("a.permalink").attr("href", $.url().attr("directory") + "?"+ $.url(url).attr('query'));

//                     // upate project per page dropdown
//                     $("select.page_projectnr").val(filter["limit"]);
//                 }  
//             }
//         );
//     },

//     // add project to map
//     map_project: function(geometry, properties) {
//         var project = {
//             "type": "Feature",
//             "properties": properties,
//             "geometry": geometry
//         }
//         dd.projects.addData(project);
//     },

//     // serializes form to filter object
//     // accepts form as jQuery object
//     build_filter: function($form) {

//         var form = $form.serializeObject();

//         var filter = {
//             "format": "json"
//         }

//         // amend filter with lookup methods
//         $.each(form, function(key, value) {
//             // see if we have an operator for that field
//             var lookup_method = $form.find(".operator." + key).val() || "";
//             if (value) {
//                 if ($.inArray(key, dd.pct_fields) > -1) value = parseFloat(value) / 100;
//                 filter[key + lookup_method] = value;
//             }
//         })

//         return filter;
//     }
// }

// /*
//  * jQuery utility to serialize form
//  * http://jsfiddle.net/sxGtM/3/
//  */

// $.fn.serializeObject = function()
// {
//     var o = {};
//     var a = this.serializeArray();
//     $.each(a, function() {
//         if (o[this.name] !== undefined) {
//             if (!o[this.name].push) {
//                 o[this.name] = [o[this.name]];
//             }
//             o[this.name].push(this.value || '');
//         } else {
//             o[this.name] = this.value || '';
//         }
//     });
//     return o;
// };

// https://github.com/hongymagic/jQuery.serializeObject

$.fn.serializeObject = function () {
    "use strict";

    var result = {};
    var extend = function (i, element) {
        var node = result[element.name];

// If node with same name exists already, need to convert it to an array as it
// is a multi-value field (i.e., checkboxes)

        if ('undefined' !== typeof node && node !== null) {
            if ($.isArray(node)) {
                node.push(element.value);
            } else {
                result[element.name] = [node, element.value];
            }
        } else {
            result[element.name] = element.value;
        }
    };

// For each serialzable element, convert element names to camelCasing and
// extend each of them to a JSON object

    $.each(this.serializeArray(), extend);
    return result;
};