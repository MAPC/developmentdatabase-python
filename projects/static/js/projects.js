
/* Global Development Database namespace */

var dd = {};


/* Bootstrap DataTables */

/* Default class modification */
$.extend( $.fn.dataTableExt.oStdClasses, {
    "sWrapper": "dataTables_wrapper form-inline"
} );

/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
    return {
        "iStart":         oSettings._iDisplayStart,
        "iEnd":           oSettings.fnDisplayEnd(),
        "iLength":        oSettings._iDisplayLength,
        "iTotal":         oSettings.fnRecordsTotal(),
        "iFilteredTotal": oSettings.fnRecordsDisplay(),
        "iPage":          Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
        "iTotalPages":    Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
    };
}

/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
    "bootstrap": {
        "fnInit": function( oSettings, nPaging, fnDraw ) {
            var oLang = oSettings.oLanguage.oPaginate;
            var fnClickHandler = function ( e ) {
                e.preventDefault();
                if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
                    fnDraw( oSettings );
                }
            };

            $(nPaging).addClass('pagination').append(
                    '<ul>'+
                        '<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
                        '<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
                    '</ul>'
            );
            var els = $('a', nPaging);
            $(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
            $(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
        },

        "fnUpdate": function ( oSettings, fnDraw ) {
            var iListLength = 5;
            var oPaging = oSettings.oInstance.fnPagingInfo();
            var an = oSettings.aanFeatures.p;
            var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);

            if ( oPaging.iTotalPages < iListLength) {
                iStart = 1;
                iEnd = oPaging.iTotalPages;
            }
            else if ( oPaging.iPage <= iHalf ) {
                iStart = 1;
                iEnd = iListLength;
            } else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
                iStart = oPaging.iTotalPages - iListLength + 1;
                iEnd = oPaging.iTotalPages;
            } else {
                iStart = oPaging.iPage - iHalf + 1;
                iEnd = iStart + iListLength - 1;
            }

            for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
                // Remove the middle elements
                $('li:gt(0)', an[i]).filter(':not(:last)').remove();

                // Add the new list items and their event handlers
                for ( j=iStart ; j<=iEnd ; j++ ) {
                    sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
                    $('<li '+sClass+'><a href="#">'+j+'</a></li>')
                        .insertBefore( $('li:last', an[i])[0] )
                        .bind('click', function (e) {
                            e.preventDefault();
                            oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
                            fnDraw( oSettings );
                        } );
                }

                // Add / remove disabled classes from the static elements
                if ( oPaging.iPage === 0 ) {
                    $('li:first', an[i]).addClass('disabled');
                } else {
                    $('li:first', an[i]).removeClass('disabled');
                }

                if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
                    $('li:last', an[i]).addClass('disabled');
                } else {
                    $('li:last', an[i]).removeClass('disabled');
                }
            }
        }
    }
} );


$(document).ready(function() {

    dd = {

        // Django project API
        projectAPI: "/api/v1/project/",

        // project filter methods
        filter: (function() {
            var parameters = {
                "format": "json"
            };
            return {
                set: function(k,v) {
                    if (v) {
                        parameters[k] = v;
                    } else {
                        delete parameters[k];
                    }
                },
                get: function() {
                    return parameters;
                },
                apply: function() {
                    $.getJSON(dd.projectAPI, parameters, function(data) {
                        dd.projectTable.fnClearTable();
                        var rows = [];
                        $.each(data.objects, function(key, obj) {
                            rows.push( [obj["id"], obj["name"], obj["status"], obj["confirmed"], obj["located"], "-" ] );
                            dd.feature.create( obj["id"], {
                                "type": "Feature",
                                "properties": {
                                    "popupContent": obj["name"]
                                },
                                "geometry": obj["location"]
                            });
                        });
                        dd.projectTable.fnAddData( rows );
                    });
                }
            }
        }()),

        // manage project map objects
        feature: (function() {
            var objects = {};
            return {
                create: function(k,v) {
                    objects[k] = v;
                },
                remove: function(k) {
                    delete objects[k];
                },
                removeAll: function() {
                    for (var k in objects) {
                        delete objects[k];
                    }
                },
                get: function(k) {
                    return objects[k];
                },
                getAll: function() {
                    return objects;
                }
            }
        }())

    };

    // initialize map
    dd.map = new L.Map("map");
    dd.basemapUrl = "http://{s}.tile.cloudmade.com/a16f47619b8943b394e9da2009f89bfa/22677/256/{z}/{x}/{y}.png",
    dd.basemapAttrib = "Map data &copy; 2012 OpenStreetMap contributors, Imagery &copy; 2012 CloudMade";
    dd.basemap = new L.TileLayer(dd.basemapUrl, {maxZoom: 18, attribution: dd.basemapAttrib});
    dd.defaultMapCenter = new L.LatLng(42.357778, -71.061667);
    dd.map.addLayer(dd.basemap);

    // initialize project layer
    dd.projectLayer = new L.GeoJSON();
    dd.projectLayer.on("featureparse", function (e) {  
        if (e.properties && e.properties.popupContent) {
            e.layer.bindPopup(e.properties.popupContent);
        }
    });
    dd.map.addLayer(dd.projectLayer);

    // layer control
    // var layersControl = new L.Control.Layers({
    //     "Background": basemap
    // }, {
    //     "Projects": projectLayer
    // });
    // map.addControl(layersControl);

    // initialize project table
    dd.projectTable = $('#projects').dataTable({ 
        "sDom": "<'row'<'span6'l><'span6'f>r>t<'row'<'span6'i><'span6'p>>",
        "sPaginationType": "bootstrap",
        "fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
            dd.projectLayer.addGeoJSON(dd.feature.get(aData[0])); // project-id
        },
        "fnPreDrawCallback": function( oSettings ) {
            // clear map layer before adding new features from table
            dd.projectLayer.clearLayers();
        },
        "fnDrawCallback": function() {
            try {
                // zoom to projects
                dd.map.fitBounds(dd.projectLayer.getBounds());
            } catch (e) {
                // or zoom to boston
                // FIXME: throws Type Error and leads to inconsistent map views
                // dd.map.setView(dd.defaultMapCenter, 9); 
            }
        },
        "oLanguage": {
            "sSearch": "Search for project name:"
        },
        "aoColumnDefs": [ 
            { "bSearchable": false, "aTargets": [ 0,2,3,4,5 ] }
        ]
    })

    // Show/hide filter options
    $("#filter-container").on("hidden", function() {
        $("#filter-toggle-status").text("Show");
    })
    .on("shown", function() {
        $("#filter-toggle-status").text("Hide");
    });

    // build project filter
    $(".project-filter").on("change", function() {   
        dd.filter.set($(this).attr("id"), $(this).val());
        
    });
    $('.datepicker').datepicker().on("changeDate", function() {
        dd.filter.set($(this).attr("id"), $(this).val());
    });

    // apply filter
    $("#apply-filter").on("click", function() {
        // clear map features
        dd.feature.removeAll();
        dd.filter.apply();
    });

    // load defaults
    

});