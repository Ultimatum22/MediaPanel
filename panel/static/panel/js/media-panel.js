!function(module, $, window, document, undefined) {
    'use strict';
 
    var mediaPanel = function() {
        console.log('mediaPanel');

        // variables
        var api = {};
        var pluginName = 'mediaPanel';

        var full_days = [ 'Zondag', 'Maandag', 'Dinsdag', 'Woensdag', 'Donderdag', 'Vrijdag', 'Zaterdag' ];
        var short_months = [ 'Jan', 'Feb', 'Maa', 'Apr', 'Mei', 'Juni', 'Juli', 'Aug', 'Sept', 'Okt', 'Nov', 'Dec' ];
        var full_months = [ 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December' ];

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
	        var now = new Date();

			var hours = now.getHours();
			var minutes = now.getMinutes();
			var seconds = now.getSeconds();
			
			hours = (hours < 10 ? '0' : '') + hours;
			minutes = (minutes < 10 ? '0' : '') + minutes;
			seconds = (seconds < 10 ? '0' : '') + seconds;
	
			var time = hours + ':' + minutes;

			$('#current_date_time .date').html(full_days[now.getDay()] + ', ' + now.getDate() + ' ' + full_months[now.getMonth()]);
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
         * Update weather every 60 minutes
         *
         */
        api.updateWeather = function() {
            $('#weather').load('/weather/forecast');

            // 15 minutes
            setTimeout(function() {
                api.updateWeather();
            }, 3600000);

            $('.forecast').css('width', ($('#weather').outerWidth() / 5));
        };

        api.gatherBackgrounds = function() {
            $.get('/background/update', function(data) {
                // Do nothing, just call url
            });

            // Every 5 minutes
            setTimeout(function() {
                api.gatherBackgrounds();
            }, 300000);
        }

		/**
		 * Update background photo periodically
		 *
		 */
		api.updateBackground = function() {
            var top;
            var bottom;

            if ($('#background-underlay-1').is(':visible')) {
				top = $('#background-underlay-1');
				bottom = $('#background-underlay-2');
			}
			else {
				bottom = $('#background-underlay-1');
				top = $('#background-underlay-2');
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

                var owner = '<span class="dark">Photo</span> ';
                if(data.taken_by != null) {
                    owner += ' <span class="dark">by</span>  ' + data.taken_by;
                }

                var date_taken = new Date(data.date_taken);

                owner += ' <span class="dark">taken</span>  ' + date_taken.getDate() + ' ' + full_months[date_taken.getMonth()] + ' ' + date_taken.getFullYear();

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
                api.updateBackground();
            }, 30000);
		};
       
       api.init = function(options) {
            console.log(pluginName + ':api.init');
            api.settings = $.extend({}, api.defaults, options);

            $('#calendar').css('width', ($('#top_panel').outerWidth() - $('#current_date_time').outerWidth()));

            return api;
        };
 
        // return the public API (Plugin) to expose
        return api;
    };
 
    module.mediaPanel = mediaPanel;
}(this, jQuery, window, document);