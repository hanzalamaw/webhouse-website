/**
 * Load navbar.html into #navbar-container and fix relative links for subfolders.
 * Navbar content is written for site root; this script prefixes href/src with ../ when in services/, language/, or platform/.
 */
(function() {
    'use strict';
    var container = document.getElementById('navbar-container');
    if (!container) return;

    var pathname = window.location.pathname || '';
    var depth = (pathname.indexOf('/services/') !== -1 || pathname.indexOf('/language/') !== -1 || pathname.indexOf('/platform/') !== -1) ? 1 : 0;
    var prefix = depth ? '../' : '';
    var navbarPath = depth ? '../navbar.html' : 'navbar.html';

    fetch(navbarPath)
        .then(function(r) { return r.text(); })
        .then(function(html) {
            container.innerHTML = html;
            var root = container;
            [].forEach.call(root.querySelectorAll('a[href], img[src]'), function(el) {
                var attr = el.tagName === 'A' ? 'href' : 'src';
                var val = el.getAttribute(attr);
                if (!val || val.indexOf('#') === 0 || val.indexOf('http') === 0 || val.indexOf('mailto:') === 0 || val.indexOf('//') === 0) return;
                if (depth && val.indexOf('services/') === 0) val = val.replace(/^services\//, '');
                el.setAttribute(attr, prefix + val);
            });
            document.dispatchEvent(new CustomEvent('navbar-loaded'));
        })
        .catch(function() {
            container.innerHTML = '<!-- Navbar failed to load -->';
        });
})();
