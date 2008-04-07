/**
 * jQuery lightBox plugin
 * This jQuery plugin was inspired and based on Lightbox 2 by Lokesh Dhakar (http://www.huddletogether.com/projects/lightbox2/)
 * and adapted to me for use like a plugin from jQuery.
 * @name jquery-lightbox-0.2.js
 * @author Leandro Vieira Pinho - http://leandrovieira.com
 * @version 0.2
 * @date October 4, 2007
 * @category jQuery plugin
 * @copyright (c) 2007 Leandro Vieira Pinho (leandrovieira.com)
 * @example Visit http://leadrovieira.com/projects/jquery/lightbox/ for more informations about this jQuery plugin
 */
jQuery.fn.lightBox = function(settings) {
	/**
	 * Default settings. These values can be modified when call this plugin.
	 * Example: $('#gallery a').lightBox({overlayBgColor: #fff});
	 */
	settings = jQuery.extend({
		// You can change these configuration how you like
		overlayBgColor:		'#000', 	// (string) Background color to overlay; inform a hexadecimal value like: #RRGGBB. Where RR, GG, and BB are the hexadecimal values for the red, green, and blue values of the color.
		overlayOpacity: 	0.8, 		// (integer) Opacity value to overlay; inform: 0.X. Where X are number from 0 to 9
		imageLoading: 		'/static/lightbox-ico-loading.gif', 		// (string) Path and the name of the loading icon
		imageBtnClose: 		'/static/lightbox-btn-close.gif',		// (string) Path and the name of the close btn
		// Don´t alter these variables in any way
		imageArray:			new Array,
		activeImage:		null
	},settings);
	// Cache the jQuery object with all elements matched
	var _$ = this;
	function _initialize() {
		_start($(this),_$);
		return false;		
	}
	/**
	 * Start the jQuery lightBox plugin receiving the object (a) clicked and jQuery matched object(s)
	 */
	function _start(objectClicked,jQueryMatchedObject) {
		// Hide some elements when overlay is showed. In IE, these elements appear above the overlay.
		$('select, embed, object').hide();
		// Create the markup structure
		_markup_structure();
		// Get the page size and show the overlay
		var arrPageSizes = ___getPageSize();
		$('#jquery-overlay').css({ backgroundColor: settings.overlayBgColor, opacity: settings.overlayOpacity, width: arrPageSizes[0], height: arrPageSizes[1] }).fadeIn();
		// Create an Array to storage the images references
		settings.imageArray = [];
		imageNum = 0;
		// We have an image set? Or just an image? Let´s see it.
		if ( jQueryMatchedObject.length == 1 ) {
			// Add an Array, with href and title atributes, inside the Array that storage the images references
			settings.imageArray.push(new Array(jQueryMatchedObject.attr('href'),jQueryMatchedObject.attr('title')));
		} else {
			// Add an Array (as many as we have), with href and title atributes, inside the Array that storage the images references		
			for ( var i = 0; i < jQueryMatchedObject.length; i++ ) {
				settings.imageArray.push(new Array(jQueryMatchedObject[i].getAttribute('href'),jQueryMatchedObject[i].getAttribute('title')));
			}
		}
		/**
		 * In some cases IE get the full path and in another get just the relative path.
		 * So, use match to verify better instead the operator !=
		 */
		while ( !settings.imageArray[imageNum][0].match(objectClicked.attr('href')) ) {
			imageNum++;
		}
		// Calculate top and left offset for the jquery-lightbox div object and show it
		var arrPageScroll = ___getPageScroll();
		$('#jquery-lightbox').css({ top: arrPageScroll[1] + (arrPageSizes[3] / 10), left: arrPageScroll[0] }).show();
		// Prepare the image that the user have clicked to show it
		_set_image_to_view(imageNum);
	};
	/**
	 * Create the markup structure to jQuery lightBox plugin
	 * The markup will be like that:
		<div id="jquery-overlay"></div>
		<div id="jquery-lightbox">
			<div id="lightbox-container-image-box">
				<div id="lightbox-container-image">
					<img src="../fotos/XX.jpg" id="lightbox-image">
					<div id="lightbox-nav">
						<a href="#" id="lightbox-nav-btnPrev"></a>
						<a href="#" id="lightbox-nav-btnNext"></a>
					</div>
					<div id="lightbox-loading">
						<a href="#" id="lightbox-loading-link">
							<img src="../images/lightbox-ico-loading.gif">
						</a>
					</div>
				</div>
			</div>
			<div id="lightbox-container-image-data-box">
				<div id="lightbox-container-image-data">
					<div id="lightbox-image-details">
						<span id="lightbox-image-details-caption"></span>
						<span id="lightbox-image-details-currentNumber"></span>
					</div>
					<div id="lightbox-secNav">
						<a href="#" id="lightbox-secNav-btnClose">
							<img src="../images/lightbox-btn-close.gif">
						</a>
					</div>
				</div>
			</div>
		</div>
	 */
	function _markup_structure() {
		$('body').append('<div id="jquery-overlay"></div><div id="jquery-lightbox"><div id="lightbox-container-image-box"><div id="lightbox-container-image"><img id="lightbox-image"><div style="" id="lightbox-nav"><a href="#" id="lightbox-nav-btnPrev"></a><a href="#" id="lightbox-nav-btnNext"></a></div><div id="lightbox-loading"><a href="#" id="lightbox-loading-link"><img src="' + settings.imageLoading + '"></a></div></div></div><div id="lightbox-container-image-data-box"><div id="lightbox-container-image-data"><div id="lightbox-image-details"><span id="lightbox-image-details-caption"></span><span id="lightbox-image-details-currentNumber"></span></div><div id="lightbox-secNav"><a href="#" id="lightbox-secNav-btnClose"><img src="' + settings.imageBtnClose + '"></a></div></div></div></div>');
		// Hide the jquery-overlay and jquery-lightbox objects and assign the _finish function to them when click on it
		$('#jquery-overlay,#jquery-lightbox').click(function() {
			_finish();									
		}).hide();
		// Assign the _finish function to lightbox-loading-link and lightbox-secNav-btnClose objects
		$('#lightbox-loading-link,#lightbox-secNav-btnClose').click(function() {
			_finish();
			return false;
		});
	};
	/**
	 * Hide some elements of jQuery lightBox and preloader the image to calculate its size to resize the container image
	 */
	function _set_image_to_view(imageNum) {
		settings.activeImage = imageNum
		// Hide some elements
		$('#lightbox-image,#lightbox-nav,#lightbox-nav-btnPrev,#lightbox-nav-btnNext,#lightbox-container-image-data-box,#lightbox-image-details-currentNumber').hide();
		// Preload the image process
		var objImagePreloader = new Image();
		objImagePreloader.onload = function() {
			$('#lightbox-image').attr('src',settings.imageArray[settings.activeImage][0]);
			_resize_container_image_box(objImagePreloader.width,objImagePreloader.height);
			//	clear onLoad, IE behaves irratically with animated gifs otherwise
			objImagePreloader.onload=function(){};
		}
		objImagePreloader.src = settings.imageArray[settings.activeImage][0];
	};
	/**
	 * Resize the container of the image
	 */
	function _resize_container_image_box(intImageWidth,intImageHeight) {
		// Get current width and height
		var intCurrentWidth = $('#lightbox-container-image-box').width();
		var intCurrentHeight = $('#lightbox-container-image-box').height();
		// Get the width and height of the selected image plus the padding
		var intWidth = (intImageWidth + (10 * 2)); //
		var intHeight = (intImageHeight + (10 * 2)); //
		// Diferences
		var intDiffW = intCurrentWidth - intWidth;
		var intDiffH = intCurrentHeight - intHeight;
		/*if ( ! ( intDiffW == 0 ) ) {
			$('#lightbox-container-image-box').animate({ width: intWidth },400);
		}
		if ( ! ( intDiffH == 0 ) ) {
			$('#lightbox-container-image-box').animate({ height: intHeight },400);
		}*/
		$('#lightbox-container-image-box').animate({ width: intWidth, height: intHeight },400,function() { _show_image(); });
		if ( ( intDiffW == 0 ) && ( intDiffH == 0 ) ) {
			if ( $.browser.msie ) {
				___pause(250);
			} else {
				___pause(100);	
			}
		}
		$('#lightbox-nav-btnPrev,#lightbox-nav-btnNext').css({ height: intImageHeight });
		$('#lightbox-container-image-data-box').css({ width: intImageWidth });
	};
	/**
	 * Show the especified image
	 */
	function _show_image() {
		$('#lightbox-loading').hide();
		$('#lightbox-image').fadeIn(function() {
			_show_image_data();
		});
		_preload_neighbor_images();
	};
	/**
	 * Show data about a especified image
	 */
	function _show_image_data() {
		$('#lightbox-container-image-data-box').slideDown('fast');
		if ( settings.imageArray[settings.activeImage][1] ) {
			$('#lightbox-image-details-caption').html(settings.imageArray[settings.activeImage][1]).show(function() { _update_nav(); });
		}
		// If we have a image set, display 'Image X of X'
		if ( settings.imageArray.length > 1 ) {
			$('#lightbox-image-details-currentNumber').html('Image ' + ( settings.activeImage + 1 ) + ' of ' + settings.imageArray.length).show();
		}		
	};
	/**
	 * Update the navigation
	 */
	function _update_nav() {
		$('#lightbox-nav').show();
		// Show the prev button, if not the first image in set
		if ( settings.activeImage != 0 ) {
			$('#lightbox-nav-btnPrev').unbind();
			$('#lightbox-nav-btnPrev').show().bind('click',function() {
				_set_image_to_view(settings.activeImage - 1);
				return false;
			});
		}
		// Show the next button, if not the last image in set
		if ( settings.activeImage != ( settings.imageArray.length -1 ) ) {
			$('#lightbox-nav-btnNext').unbind();
			$('#lightbox-nav-btnNext').show().bind('click',function() {
				_set_image_to_view(settings.activeImage + 1);
				return false;
			});
		}
	};
	/**
	 * Preload prev and next image
	 */
	function _preload_neighbor_images() {
		if ( (settings.imageArray.length -1) > settings.activeImage ) {
			objNext = new Image();
			objNext.src = settings.imageArray[settings.activeImage + 1][0];
		}
		if ( settings.activeImage > 0 ) {
			objPrev = new Image();
			objPrev.src = settings.imageArray[settings.activeImage -1][0];
		}
	};
	/**
	 * Finish the jQuery lightBox plugin
	 */
	function _finish() {
		$('#jquery-lightbox').remove();
		$('#jquery-overlay').fadeOut(function() { $('#jquery-overlay').remove(); });
		// Display some elements when overlay is closed. In IE, these elements appear above the overlay.
		$('select, embed, object').show();
	};

	/**
	 * Third functions
	 * - pause() by Lightbox 2.0 script
	 * - getPageSize() by quirksmode.com
	 * - getPageScroll() by quirksmode.com
	 */
	 
	 /**
	  * Stop the code execution from a escified time in milisecond
	  */
	 function ___pause(ms) {
		var date = new Date(); 
		curDate = null;
		do { var curDate = new Date(); }
		while ( curDate - date < ms);
	 };
	 /**
	  * Returns array with page width, height and window width, height
	  */
	function ___getPageSize() {
		var xScroll, yScroll;
		if (window.innerHeight && window.scrollMaxY) {	
			xScroll = window.innerWidth + window.scrollMaxX;
			yScroll = window.innerHeight + window.scrollMaxY;
		} else if (document.body.scrollHeight > document.body.offsetHeight){ // all but Explorer Mac
			xScroll = document.body.scrollWidth;
			yScroll = document.body.scrollHeight;
		} else { // Explorer Mac...would also work in Explorer 6 Strict, Mozilla and Safari
			xScroll = document.body.offsetWidth;
			yScroll = document.body.offsetHeight;
		}
		var windowWidth, windowHeight;
		if (self.innerHeight) {	// all except Explorer
			if(document.documentElement.clientWidth){
				windowWidth = document.documentElement.clientWidth; 
			} else {
				windowWidth = self.innerWidth;
			}
			windowHeight = self.innerHeight;
		} else if (document.documentElement && document.documentElement.clientHeight) { // Explorer 6 Strict Mode
			windowWidth = document.documentElement.clientWidth;
			windowHeight = document.documentElement.clientHeight;
		} else if (document.body) { // other Explorers
			windowWidth = document.body.clientWidth;
			windowHeight = document.body.clientHeight;
		}	
		// for small pages with total height less then height of the viewport
		if(yScroll < windowHeight){
			pageHeight = windowHeight;
		} else { 
			pageHeight = yScroll;
		}
		// for small pages with total width less then width of the viewport
		if(xScroll < windowWidth){	
			pageWidth = xScroll;		
		} else {
			pageWidth = windowWidth;
		}
		arrayPageSize = new Array(pageWidth,pageHeight,windowWidth,windowHeight) 
		return arrayPageSize;
	};
	/**
	 * Returns array with x,y page scroll values.
	 */
	function ___getPageScroll() {
		var xScroll, yScroll;
		if (self.pageYOffset) {
			yScroll = self.pageYOffset;
			xScroll = self.pageXOffset;
		} else if (document.documentElement && document.documentElement.scrollTop){	 // Explorer 6 Strict
			yScroll = document.documentElement.scrollTop;
			xScroll = document.documentElement.scrollLeft;
		} else if (document.body) {// all other Explorers
			yScroll = document.body.scrollTop;
			xScroll = document.body.scrollLeft;	
		}
		arrayPageScroll = new Array(xScroll,yScroll) 
		return arrayPageScroll;
	};
	return this.click(_initialize);
};
