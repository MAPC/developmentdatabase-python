// global dd namespace
window.dd = window.dd || {};

(function(){

    /**** Private */

    var map, projectLayer,

        // Url for AJAX calls
        projectUrl = '/projects/',

        // Form or Page elements with percent values
        pctEl = ["pctaffall", "retpct", "ofcmdpct", "indmfpct", "whspct", "rndpct", "edinstpct", "othpct"]; 


    /*** Page Setups */

    // Search Page: requests projects according to options and url params
    function initSearchPage( args ) {
        /* options: 
         * + query object to be passed to searchProjects
        */
        
        var args = args || {};
        var query = args.query || {};

        // Object translating Django lookups (url GET params) to search form fields
        var fieldLookups = {
            taz__municipality: 'municipality',
            ddname__icontains: 'ddname',
            projecttype: 'projecttype',
            status: 'status',
            complyr__exact: 'complyr',
            tothu__exact: 'tothu',
            ovr55: 'ovr55',
            pctaffall__exact: 'pctaffall',
            totempl__exact: 'totemp',
            ch40: 'ch40', 
            todstation: 'todstation',
            prjacrs__exact: 'prjacrs', 
            singfamhu__exact: 'singfamhu', 
            twnhsmmult__exact: 'twnhsmmult', 
            lgmultifam__exact: 'lgmultifam', 
            gqpop__exact: 'gqpop', 
            commsf__exact: 'commsf', 
            retpct__exact: 'retpct', 
            ofcmdpct__exact: 'ofcmdpct', 
            indmfpct__exact: 'indmfpct', 
            whspct__exact: 'whspct', 
            rndpct__exact: 'rndpct', 
            othpct__exact: 'othpct', 
            hotelrms__exact: 'hotelrms', 
            parking_spaces__exact: 'parking_spaces', 
            total_cost__exact: 'total_cost',
            rdv: 'rdv', 
            clustosrd: 'clustosrd',
            as_of_right: 'as_of_right',
            stalled: 'stalled', 
            phased: 'phased'
        };

        
        // number form fields, require prepended operator dropdown
        // [0]: int fields, [1]: float fields
        var numberFields = [ ['complyr', 'singfamhu', 'twnhsmmult', 'lgmultifam', 'gqpop', 'parking_spaces', 'total_cost' ], ['tothu', 'pctaffall', 'totemp', 'prjacrs', 'commsf', 'retpct', 'ofcmdpct', 'indmfpct', 'whspct', 'rndpct', 'othpct', 'hotelrms' ] ];

        var nullbooleanFields = ['ovr55', 'rdv', 'clustosrd','as_of_right']

        // tooltip fields
        var tooltipFields = [
            { 
                id: "complyr",
                title: "Estimated or actual"
             }, { 
                id: "tothu",
                title: "Number of units" 
            }, { 
                id: "singfamhu",
                title: "Number of units" 
            }, { 
                id: "twnhsmmult",
                title: "Number of units" 
            }, { 
                id: "lgmultifam",
                title: "Number of units" 
            }, { 
                id: "gqpop",
                title: "Number of beds" 
            }, { 
                id: "commsf",
                title: "In square feet" 
            }, { 
                id: "pctaffall",
                title: "In percent" 
            }, {
                id: "totemp",
                title: "MAPC Estimated Employment"
            } 
        ];

        // add url params to query
        var urlParams = $.url().param();
        // no url params return object with one empty key/value
        delete urlParams[""]; 

        if ( _.isEmpty( urlParams ) === false ) {
            query = urlParams;
        }

        /*** Tweak Search Form UI */

        // Nullable Boolean in Django defaults to "unknown" option
        _.forEach( nullbooleanFields, function( field ) {
            $("#id_" + field + " option:first-child").before("<option value=''>---------</option>");
            $("#id_" + field ).val("");
        });
        
        // Add tooltips
        _.forEach( tooltipFields, function( field ) {  
            $( "#id_" + field.id ).tooltip( { 
                title: field.title,
                placement: "right" 
            } );
        });
        
        // Prepend operator to number fields
        var operatorHtml = _.template(
            $( "script.operator-select" ).html()
        );
        _.forEach( _.flatten( numberFields ), function( value ) {

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

                var field = fieldLookups[ key ] || key.split( "__" )[0];
                var $field = $( "#id_" + field );
                $field.val( value );
                
                if ( _.contains( numberFields, field ) === true ) {
                    var lookup = key.split( "__" )[1]
                    $field.prev( "select" ).val( "__" + lookup );
                }
            
            });
        }

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
                if ( _.contains( numberFields[0], field ) ) {
                    value = parseInt( value );
                } else if ( _.contains( numberFields[1], field ) ) {
                    value = parseFloat( value );
                }
                lookupQuery[ lookups[ field ] ] = value;
            });

            return lookupQuery;
        }

        /*** User Interaction Events */

        // search query 
        $(".form-actions .btn[type='submit']").on("click", function( event ) {
            event.preventDefault();
            var formQueryObject = $("form.projectfilters").serializeObject();
            var query = cleanFormQuery( formQueryObject );
            searchProjects( query );
        });

        // reset form
        $(".form-actions button.reset").on( "click", function( event ) {
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

        /*** Render Map and Form */
  
        initMap();
        searchProjects( query );

    }

    // Update Page: drag marker on map, validate and submit form
    function initUpdatePage( args ) {

        // Render map without projectLayer
        initMap( { showProjectLayer: false } );

        // clean percent values
        adjustPctFields( { method: "humanize" } );

        // read form project location
        var projectLocation = $( "#id_location" ).val();

        // stored project location > hash
        if ( _.isEmpty( projectLocation ) === false ) {

            // center map on projet
            var coords = projectLocation.split(" "),
                lng = parseFloat( coords[1].substring(1) ),
                lat = parseFloat( coords[2] ),
                center = new L.LatLng( lat, lng );
            map.setView( center, 16, true );

        } else {

            // check for and zoom to location hash
            var hash = location.hash;
            if ( hash.indexOf("#") === 0 ) {
                hash = hash.substr(1);
            }
            var hashArr = hash.split( "/" );
            if ( hashArr.length === 3 ) {
                var zoom = parseInt( hashArr[0], 10 ),
                    lat = parseFloat( hashArr[1] ),
                    lon = parseFloat( hashArr[2] );
                if ( !isNaN( zoom ) && !isNaN( lat ) && !isNaN( lon ) ) {
                    var center = new L.LatLng( lat, lon );
                    map.setView( center, zoom, true );
                }
            }

        }

        // add and place project marker
        var projectMarker = new L.marker( map.getCenter(), {
                draggable: true
            })
            .addTo( map )
            .on( "dragend", function( event ) {
                // update form values
                var lat = event.target.getLatLng().lat.toFixed(4);
                var lng = event.target.getLatLng().lng.toFixed(4);
                $( "#id_location" ).val( "POINT (" + lng + " " +  lat + ")" );
                // remove error
                if ( $( "#map-caption p" ).hasClass( "error" ) === true ) {
                    $( "#map-caption p" ).removeClass( "error" );
                }
            });
        $( "#center-marker" ).on( "click", function( event ) {
            event.preventDefault();
            projectMarker
                .setLatLng( map.getCenter() ) 
                .fireEvent( "dragend" );
        });

        // Enable Field Tooltips
        // FIXME: tooltips do not show in collapse containers
        $( "form.projectdata div.controls" ).tooltip({
            placement: "right"
        });

        /*** Client-side Form Validation */

        var validator = $( "form.projectdata" ).validate({
            rules: {
                ddname: {
                    required: true,
                    maxlength: 100
                },
                status: "required",
                projecttype: "required",
                complyr: {
                        required: true,
                        number: true,
                        rangelength: [4, 4],
                        min: 1900,
                        max: 2100
                },
                tothu: {
                        required: true,
                        number: true
                },
                commsf: {
                        required: true,
                        number: true
                },
                prjacrs: {
                    required: true,
                    number: true
                },
                url: { 
                    url: true,
                    maxlength: 200 
                },
                url_add: { 
                    url: true,
                    maxlength: 200 
                },
                hotelrms: "number",
                rptdemp: "number",
                totemp: "number",
                parking_spaces: "digits",
                total_cost: "digits",
                dev_name: { maxlength: 100 }
            },
            messages: {
                    complyr: "Please enter a valid year, like \"2013\"."
            },
            errorElement: "span",
            errorPlacement: function(error, element) {
                    element.after(error);
            }
        });

        // conditional form field relations
        var conditionalFields = {
            id_tothu: {
                elCollapse: "div.housing",
                fieldValidationRules: {
                    id_singfamhu: {
                        required: true,
                        digits: true
                    }, 
                    id_twnhsmmult: {
                        required: true,
                        digits: true
                    }, 
                    id_lgmultifam: {
                        required: true,
                        digits: true
                    }, 
                    id_ovr55: {
                        required: true
                    },
                    id_pctaffall: {
                        required: true
                    },
                    id_gqpop: {
                        required: true,
                        digits: true
                    }
                }
            },
            id_commsf: {
                elCollapse: "div.non-res",
                fieldValidationRules: {
                    id_retpct: {
                        required: true
                    },
                    id_ofcmdpct: {
                        required: true
                    },
                    id_indmfpct: {
                        required: true
                    },
                    id_whspct: {
                        required: true
                    },
                    id_rndpct: {
                        required: true
                    },
                    id_edinstpct: {
                        required: true
                    },
                    id_othpct: {
                        required: true
                    }
                }
            }
        }
        // collapse, add validation rules and red asterisk
        _.forEach( conditionalFields, function( properties, fieldId ) {

            $( "#" + fieldId ).on( "change", function( event ) {

                // empty value returns NaN and therefore 0
                var elValue = parseInt( $( this ).val() ) || 0;

                if ( elValue > 0 ) {

                    // show fields
                    $( properties.elCollapse ).collapse( "show" );

                    // make all fields required
                    _.forEach( properties.fieldValidationRules, function( rules, conditionalFieldId ) {
                        var $conditionalField = $( "#" + conditionalFieldId ),
                            $label = $( "label[for='" + conditionalFieldId + "']" ),
                            requiredHtml = "<span class=\"required\">&nbsp;*</span>",
                            isRequired = $label.find( "span.required" ).length > 0 ? true : false;
                        
                        if ( isRequired === false ) {
                            $conditionalField.rules( "add", rules );
                            $label.html( $label.html() + requiredHtml );
                        }
                        
                    });

                } else {

                    // hide fields
                    $( properties.elCollapse ).collapse( "hide" );

                    // remove rules
                    _.forEach( properties.fieldValidationRules, function( rules, conditionalFieldId ) {
                        var $conditionalField = $( "#" + conditionalFieldId ),
                            $label = $( "label[for='" + conditionalFieldId + "']" ),
                            isRequired = $label.find( "span.required" ).length > 0 ? true : false;

                        if ( isRequired === true ) {
                            // FIXME: cannot remove granular rules
                            $conditionalField.rules( "remove" );
                            $label.html( $label.text().slice( 0,-2 ) );
                        }
                        
                    });

                    // remove error messages
                    $( properties.elCollapse + " span.error" ).remove();

                }
            });
        });

        // check for location before submit
        $("form.projectdata").on("submit", function(event) {

            // no location provided
            var projectLocation = $( "#id_location" ).val();
            if ( _.isEmpty( projectLocation ) === true ) {
                // add error
                $( "#map-caption p" ).addClass( "error" );
                return false;
            }

            // form doesn't validate
            if ( $("form.projectdata").valid() === false ) {
                return false;
            }

            // clean percent values
            adjustPctFields( { method: "computerize" } );

            // clean float and integer fields
            // FIXME: give better error feedback to user
            var floatFields = ["prjacrs", "tothu", "rptdemp", "emploss", "commsf", "hotelrms"];
            var intFields = ["singfamhu", "twnhsmmult", "lgmultifam", "gqpop"];
            _.forEach( floatFields, function( value ) {
                var cleanVal = parseFloat( $( "#id_" + value ).val() );
                if ( isNaN( cleanVal ) === false ) {
                    $( "#id_" + value ).val( cleanVal );
                }
            });
            _.forEach( intFields, function( value ) {
                var cleanVal = parseInt( $( "#id_" + value ).val() );
                if ( isNaN( cleanVal ) === false ) {
                    $( "#id_" + value ).val( cleanVal );
                }
            });

        });

    }

    // detail page with bing map and project point
    function initDetailPage( args ) {

        var args = args || {};

        // Render map without projectLayer
        initMap( { 
            basemap: "bing",
            projectMarkerStyle: {
                radius: 10,
                color: "#fff",
                weight: 2,
                opacity: 1,
                fillColor: "#044388",
                fillOpacity: 0.4
            }
        } );

        if ( isNaN( args.dd_id ) === false ) {  
            searchProjects( { dd_id: args.dd_id } );
        }

    }

    /*** Mapping */

    // initialize dd.map with basemaps, layercontrol and empty projectLayer
    function initMap( args ) {

        // defaults
        var args = args || {},
            center = args.center || new L.LatLng(42.33, -71.13),
            zoom = args.zoom || 9,
            overlays = {},
            showLayerControl = ( args.showLayerControl !== false ) ? true : false,
            showProjectLayer = ( args.showProjectLayer !== false ) ? true : false,
            projectMarkerStyle = args.projectMarkerStyle || {};
        
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

        if ( showProjectLayer === true ) {

            // point style
            var defaultStyle = {
                radius: 6,
                fillColor: "#044388",
                color: "#fff",
                weight: 1,
                opacity: 0.6,
                fillOpacity: 0.6
            };
            projectMarkerStyle = _.assign( defaultStyle, projectMarkerStyle );

            // initialize empty projectlayer
            projectLayer = L.geoJson( null, {
                pointToLayer: function ( feature, latlng ) {
                    return L.circleMarker(latlng, projectMarkerStyle )
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
            overlays = {
                "Development Projects": projectLayer
            }
        }

        // layer control
        // FIXME: order?
        if ( showLayerControl === true ) {
            var layerControl = new L.Control.Layers( {
                    "MAPC Basemap": basemaps.mapc,
                    "OpenStreetMap": basemaps.osm,
                    "Bing Aerial": basemaps.bing
                }, 
                overlays
            );
            map.addControl( layerControl );
        }
    
    }

    /*** Data Requests */

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

    // change string to simple plural depending on given number
    function plural( string, number ) {
        if ( number != 1 ) {
            return string + "s";
        } else {
            return string;
        }

    }

    // transform percent values to human readable strings ("57%") or database values (0.57)
    function adjustPctFields( args ) {

        var args = args || {};
        var method = args.method;

        function adjustValue( value ) {
            if ( method === "humanize" ) {
                var value = value * 100 + "%";
            } else if ( method === "computerize" ) {
                var value = parseFloat( value ) / 100;
            }
            return value;
        }

        // adjust percent values in form
        _.forEach( pctEl, function( el ) {
            var $el = $( "#id_" + el ),
                elValue = $el.val();
                if ( _.isEmpty( elValue ) === false ) {
                    elValue = adjustValue( $el.val() );
                    $el.val( elValue );
                }
        });
    }

    /**** Public */

    dd.initMap = initMap;
    dd.searchProjects = searchProjects;
    dd.initSearchPage = initSearchPage;
    dd.initUpdatePage = initUpdatePage;
    dd.initDetailPage = initDetailPage;

})();


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