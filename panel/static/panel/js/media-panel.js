!function(module, $, window, document, undefined) {
    'use strict';
 
    var mediaPanel = function() {
        console.log('mediaPanel');

        // variables
        var api = {};
        var pluginName = 'mediaPanel';
 
        // methods
        var constructor = (function() {
            console.log(pluginName + ':constructor');
        })();
 
        /*!
         * Public properties and methods
         */
 
        // properties
        api.defaults = {};
        api.settings = {};
 
        /**
         * Update the time and date every second
         *
         */
        api.updateTime = function() {
	        var days = [ 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ];
	        var months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ];
	        var now = new Date();
	
			var day = now.getDay();
			var date = now.getDate();
			var month = now.getMonth();
			//var year = now.getFullYear();
	
			var date = days[day] + ', ' + date + ' ' + months[month];
			
			var hours = now.getHours();
			var minutes = now.getMinutes();
			var seconds = now.getSeconds();
			
			hours = (hours < 10 ? '0' : '') + hours;
			minutes = (minutes < 10 ? '0' : '') + minutes;
			seconds = (seconds < 10 ? '0' : '') + seconds;
	
			var time = hours + ':' + minutes;
	
			$('#current_date_time .date').html(date);
			$('#current_date_time .time').html(time + '<span class="sec">' + seconds + '</span>');
	
			setTimeout(function() {
				api.updateTime();
			}, 1000);
        };

        /**
         * Update agenda every hour
         *
         */
        api.updateAgenda = function() {
			$('#calendar').load('/agenda');

			// 1 hour
			setTimeout(function() {
				api.updateAgenda();
			}, 3600000);
        };

        /**
		 * Update weather every 15 minutes
		 *
		 */
        api.updateWeather = function() {
	     	$('#weather').load('/panel/weather');

			// 15 minutes
			setTimeout(function() {
				api.updateWeather();
			}, 900000);

            $('.forecast').css('width', ($('#weather').outerWidth() / 5));
       };

		/**
		 * Update background photo periodically
		 *
		 */
		api.updatePhoto = function() {
            /*$("#progressTimer").progressTimer({
                timeLimit: 30,
                baseStyle: 'progress-bar-info',
            });*/

			if ($('#background-underlay-1').is(':visible')) {
				var top = $('#background-underlay-1');
				var bottom = $('#background-underlay-2');
			}
			else {
				var bottom = $('#background-underlay-1');
				var top = $('#background-underlay-2');
			}

			$.getJSON('/background', function(data) {
                $('#img-info').fadeOut(1000);

                $(this).remove(); // prevent memory leaks
                bottom.css({
                    background: 'url("static_media/' + decodeURIComponent(data.path) + '") center center',
                    backgroundSize: 'cover',
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    display: 'block'
                });

                var owner = '<span class="dark">Photo</span> '
                if(data.taken_by != null) {
                    owner += ' <span class="dark">by</span>  ' + data.taken_by
                }

                owner += ' <span class="dark">taken</span>  ' + data.date_taken

                $('#img-owner').html(owner);
                $('#img-title').html('<span class="dark">Album</span>  ' + data.album);

                bottom.show();

                top.fadeOut(1500, function() {
                    top.hide().css({background: 'none', zIndex: 0});
                    bottom.css({zIndex: 1});
                });

                top.fadeOut(1500, function() {
                    top.hide().css({ background: 'none', zIndex: 0 });
                    bottom.css({ zIndex: 1 });
                    $('#img-info').fadeIn(1000);
                });
			
			}); //end getJSON
			
			setTimeout(function() {
				api.updatePhoto();
			}, 30000);
		
		};
       
       api.init = function(options) {
            console.log(pluginName + ':api.init');
            api.settings = $.extend({}, api.defaults, options);

            //console.log('TW: ' + $('#top_panel').outerWidth());
            //console.log('CDTW: ' + $('#current_date_time').outerWidth());
            //console.log('CW: ' + ($('#top_panel').outerWidth() - $('#current_date_time').outerWidth()));
            $('#calendar').css('width', ($('#top_panel').outerWidth() - $('#current_date_time').outerWidth()));



            //alert('W: ' + ($('#weather').outerWidth() / 5));

           // privateMethod1('defaults' + JSON.stringify(publicApi.defaults));
           // privateMethod1('options' + JSON.stringify(options));
           // privateMethod1('settings' + JSON.stringify(publicApi.settings));
            return api;
        };
 
        // return the public API (Plugin) to expose
        return api;
    };
 
    module.mediaPanel = mediaPanel;
}(this, jQuery, window, document);