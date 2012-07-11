// development database namespace

var dd = {

    // number fields in filter form that require number operator
    number_fields: ["complyr", "tothu", "pctaffall", "totemp"],

    // percent fields, strip % char and divide by 100 before used in query
    pct_fields: ["pctaffall"],

    // nullboolean fields
    nullboolean_fields: ["ovr55"],

    // operators used to filter integer, float, etc. fields
    // default lookup method for string fields is 'icontains'
    number_operators: function(number_field) {
        // TODO: can be done better with an change event that appends the 
        // correct lookup method to the following DOM (form) element
        var number_operators = {
            "lt": "<",
            "exact": "=",
            "gt": ">"
        }

        var $operators = $("<select />").addClass("operator span1 " + number_field);
        
        $.each(number_operators, function(key, value) {
            var option = $("<option />", {
                value: "__" + key,
                html: value
            });
            $operators.append(option);
        });
        
        return $operators;
    },

    // add previous and next urls to pagination links
    update_pagination: function(options) {
        var options = options || {};
        $(".pagination li").addClass("disabled");

        $.each(options, function(key, value) {
            if (value) {
                var $button = $(".pagination ." + key);
                $button.attr("href", $.url().attr("directory") + "?" + $.url(value).attr("query"));
                $button.parent().removeClass("disabled");
                $button
                .off()
                .on("click", function(e) {
                    e.preventDefault();
                    dd.load_projects($.url(value).param());
                });
            }
        });
    },

    // load projects based on given url or filter parameters
    load_projects: function(filter) {
        var filter = filter || {};
        filter["format"] = "json";
        filter["limit"] = filter["limit"] || 20;

        // serialize filter to url
        var url  = "/api/v1/project/?" + $.param(filter);

        $.getJSON(
            url,  
            function(data) {
                if (dd.map) {
                    // clear projects
                    dd.projects.clearLayers();

                    if (data.objects.length > 0) {
                        //add to map
                        $.each(data.objects, function(key, project) {
                            dd.map_project(
                                project["location"], 
                                {
                                    "popupContent": "<a href=\"" + project["absolute_url"] + "\">" + project["ddname"] + "</a>"
                                }
                            );
                        });
                        dd.map.fitBounds(dd.projects.getBounds());
                    }

                    // update pagination buttons
                    dd.update_pagination({
                        "next": data.meta["next"],
                        "previous": data.meta["previous"]
                    });

                    $(".countinfo").show();
                    $(".countinfo .range").html(data.meta.offset + " - " + (parseInt(data.meta.offset) + parseInt(data.meta.limit)));
                    $(".countinfo .totalcount").html(data.meta.total_count);
                    
                    // update permalink
                    $("a.permalink").attr("href", $.url().attr("directory") + "?"+ $.url(url).attr('query'));

                    // upate project per page dropdown
                    $("select.page_projectnr").val(filter["limit"]);
                }  
            }
        );
    },

    // add project to map
    map_project: function(geometry, properties) {
        var project = {
            "type": "Feature",
            "properties": properties,
            "geometry": geometry
        }
        dd.projects.addGeoJSON(project);
    },

    // serializes form to filter object
    // accepts form as jQuery object
    build_filter: function($form) {

        var form = $form.serializeObject();

        var filter = {
            "format": "json"
        }

        // amend filter with lookup methods
        $.each(form, function(key, value) {
            // see if we have an operator for that field
            var lookup_method = $form.find(".operator." + key).val() || "";
            if (value) {
                if ($.inArray(key, dd.pct_fields) > -1) value = parseFloat(value) / 100;
                filter[key + lookup_method] = value;
            }
        })

        return filter;
    }
}

/*
 * jQuery utility to serialize form
 * http://jsfiddle.net/sxGtM/3/
 */

$.fn.serializeObject = function()
{
    var o = {};
    var a = this.serializeArray();
    $.each(a, function() {
        if (o[this.name] !== undefined) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};