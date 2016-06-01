/* global window */
window.videojs = require('video.js');
require('videojs-playlist');
require('videojs-playlist-ui');
window.jQuery = window.$ = require('jquery');
require('bootstrap-sass');

const $ = window.$;
const videojs = window.videojs;

const StripeHandler = require('./payments');

$(() => {
    // Stripe Checkout
    const stripeHandler = new StripeHandler(window);

    // Close Checkout on page navigation:
    $(window).on('popstate', () => {
        stripeHandler.close();
    });

    /**
     * Subscription
     */
    // Month Button
    const monthBtn = $('#month-sub-btn');
    const monthPrice = monthBtn.data('price');
    monthBtn.on('click', stripeHandler.handleSub('month', monthPrice));

    // Year Button
    const yearBtn = $('#year-sub-btn');
    const yearPrice = yearBtn.data('price');
    yearBtn.on('click', stripeHandler.handleSub('year', yearPrice));

    // Playlist UI for video detail page.
    const player = videojs('video');

    $.get(`/api/videos/${window.currentVideoID}`, data => {
        player.playlist(data);
        player.playlistUi();
    }).fail(error => {
        alert('failed');
    });
});
