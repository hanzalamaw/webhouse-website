/**
 * WebHouse Inc. - Mega Menu (Services & Technologies)
 * Show/hide dropdown on hover; close on mouse leave or outside click.
 */
(function() {
    'use strict';

    function initMegaMenu() {
        const triggers = document.querySelectorAll('[data-mega-menu-trigger]');
        const panels = document.querySelectorAll('[data-mega-menu-panel]');

        triggers.forEach(trigger => {
            const name = trigger.getAttribute('data-mega-menu-trigger');
            const panel = document.querySelector('[data-mega-menu-panel="' + name + '"]');
            if (!panel) return;

            let hideTimeout;

            function show() {
                clearTimeout(hideTimeout);
                panel.classList.remove('invisible', 'opacity-0');
                panel.classList.add('visible', 'opacity-100');
            }

            function hide() {
                hideTimeout = setTimeout(() => {
                    panel.classList.add('invisible', 'opacity-0');
                    panel.classList.remove('visible', 'opacity-100');
                }, 150);
            }

            trigger.addEventListener('mouseenter', show);
            trigger.addEventListener('mouseleave', hide);
            panel.addEventListener('mouseenter', show);
            panel.addEventListener('mouseleave', hide);
        });

        // Close all on click outside
        document.addEventListener('click', function(e) {
            if (e.target.closest('[data-mega-menu-trigger]') || e.target.closest('[data-mega-menu-panel]')) return;
            panels.forEach(p => {
                p.classList.add('invisible', 'opacity-0');
                p.classList.remove('visible', 'opacity-100');
            });
        });
    }

    function run() {
        initMegaMenu();
    }
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', run);
    } else {
        run();
    }
    document.addEventListener('navbar-loaded', run);
})();
