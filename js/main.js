/**
 * WebHouse Inc. - Main JavaScript
 * Handles dark mode, mobile menu, and interactive features
 */

(function() {
    'use strict';

    // Dark Mode Toggle - DISABLED: Light theme only
    function initDarkMode() {
        // Dark mode is disabled - always use light theme
        // Remove any dark class if it exists
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
    }

    // Mobile Menu Toggle
    function initMobileMenu() {
        const menuButton = document.querySelector('[data-mobile-menu-toggle]');
        const mobileMenu = document.querySelector('[data-mobile-menu]');
        const menuLinks = mobileMenu?.querySelectorAll('a');

        if (menuButton && mobileMenu) {
            menuButton.addEventListener('click', () => {
                const isOpen = mobileMenu.classList.toggle('hidden');
                menuButton.setAttribute('aria-expanded', !isOpen);
                menuButton.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
            });

            // Close menu when clicking a link
            menuLinks?.forEach(link => {
                link.addEventListener('click', () => {
                    mobileMenu.classList.add('hidden');
                    menuButton.setAttribute('aria-expanded', 'false');
                });
            });
        }
    }

    // Smooth Scroll for Anchor Links
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const href = this.getAttribute('href');
                if (href === '#') return;

                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    const headerOffset = 80;
                    const elementPosition = target.getBoundingClientRect().top;
                    const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Intersection Observer for Animations
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('[data-animate]').forEach(el => {
            observer.observe(el);
        });
    }

    // Form Validation
    function initFormValidation() {
        const newsletterForm = document.querySelector('[data-newsletter-form]');
        if (newsletterForm) {
            newsletterForm.addEventListener('submit', (e) => {
                e.preventDefault();
                const emailInput = newsletterForm.querySelector('input[type="email"]');
                const email = emailInput.value.trim();

                if (email && isValidEmail(email)) {
                    // Here you would typically send the email to your backend
                    console.log('Newsletter subscription:', email);
                    alert('Thank you for subscribing!');
                    emailInput.value = '';
                } else {
                    emailInput.setCustomValidity('Please enter a valid email address');
                    emailInput.reportValidity();
                }
            });
        }
    }

    // Email validation helper
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Initialize all features when DOM is ready
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
            return;
        }

        initDarkMode();
        initMobileMenu();
        initSmoothScroll();
        initScrollAnimations();
        initFormValidation();
    }

    // Start initialization
    init();
})();

