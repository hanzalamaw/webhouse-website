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

    // Newsletter Forms
    function initNewsletterForms() {
        document.querySelectorAll('[data-newsletter-form]').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const emailInput = form.querySelector('input[type="email"]');
                const email = emailInput?.value.trim();

                if (email && isValidEmail(email)) {
                    const subject = encodeURIComponent('Newsletter Subscription');
                    const body = encodeURIComponent('Please subscribe this email to the WebHouse Inc. newsletter:\n\n' + email);
                    window.location.href = 'mailto:connect@webhouseinc.co?subject=' + subject + '&body=' + body;
                    emailInput.value = '';
                } else if (emailInput) {
                    emailInput.setCustomValidity('Please enter a valid email address');
                    emailInput.reportValidity();
                }
            });
        });
    }

    // Contact Form (contact_us.html)
    function initContactForm() {
        const form = document.getElementById('contactForm');
        if (!form) return;

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('contactName')?.value.trim() || '';
            const from = document.getElementById('contactEmail')?.value.trim() || '';
            const subject = document.getElementById('contactSubject')?.value.trim() || 'Contact from WebHouse Inc. website';
            const message = document.getElementById('contactMessage')?.value.trim() || '';
            const body = 'Name: ' + name + '\nReply-to: ' + from + '\n\n' + message;
            window.location.href = 'mailto:connect@webhouseinc.co?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        });
    }

    // Consultation sidebar forms
    function initConsultForms() {
        document.querySelectorAll('#heroConsultForm').forEach(form => {
            form.addEventListener('submit', (e) => {
                e.preventDefault();
                const name = form.querySelector('[name="name"]')?.value.trim() || '';
                const email = form.querySelector('[name="email"]')?.value.trim() || '';
                const phone = form.querySelector('[name="phone"]')?.value.trim() || '';
                const message = form.querySelector('[name="message"]')?.value.trim() || '';
                const subject = 'Consultation Request from WebHouse Inc. website';
                const body = 'Name: ' + name + '\nEmail: ' + email + '\nPhone: ' + phone + '\n\n' + message;
                window.location.href = 'mailto:connect@webhouseinc.co?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
            });
        });
    }

    // Clickable cards with data-card-link
    function initClickableCards() {
        document.querySelectorAll('[data-card-link]').forEach(card => {
            card.addEventListener('click', (e) => {
                if (e.target.closest('a, button')) return;
                window.location.href = card.dataset.cardLink;
            });
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    window.location.href = card.dataset.cardLink;
                }
            });
            if (!card.hasAttribute('tabindex')) {
                card.setAttribute('tabindex', '0');
                card.setAttribute('role', 'link');
            }
        });
    }

    // Case study industry filters
    function initCaseStudyFilters() {
        const filters = document.querySelectorAll('[data-case-filter]');
        const cards = document.querySelectorAll('[data-case-industry]');
        if (!filters.length || !cards.length) return;

        function applyFilter(filter) {
            filters.forEach(btn => {
                const active = btn.dataset.caseFilter === filter;
                btn.classList.toggle('bg-gradient-to-r', active);
                btn.classList.toggle('from-[#b90606]', active);
                btn.classList.toggle('to-[#c80505]', active);
                btn.classList.toggle('text-white', active);
                btn.classList.toggle('shadow-glow', active);
                btn.classList.toggle('bg-white', !active);
                btn.classList.toggle('border', !active);
                btn.classList.toggle('border-gray-200', !active);
            });

            cards.forEach(card => {
                const industry = card.dataset.caseIndustry;
                const show = filter === 'all' || industry === filter;
                card.classList.toggle('hidden', !show);
            });
        }

        filters.forEach(btn => {
            btn.addEventListener('click', () => applyFilter(btn.dataset.caseFilter));
        });
    }

    // Email validation helper
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Testimonial Carousel
    function initTestimonialCarousel() {
        const carousel = document.querySelector('[data-testimonial-carousel]');
        if (!carousel) return;

        const testimonials = [
            {
                quote: 'WebHouse didn\'t just redesign our site; they <span class="bg-primary/10 text-primary px-2 rounded">reimagined our entire digital presence</span>. The ROI was immediate and significant.',
                name: 'Sarah Jenkins',
                role: 'CMO, TechGlobal',
                avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC5SvLVAWgE7fFz68xfqJTPQoz07A2tSR2Pgh-t05FNQN1C96uD1xFlhDPyPZxtvMgiLeAnuNwXdWTs073am_WoD0rywWlXYqlNoo9gJlwZu9PzurRMVZc1b7vv9aAxFQNPhDkfwH9cFYVanh2-MQ5QmYkjv-CL-vmLJd_LUXJuFhTz5zztt5divD1FpJxP_cGzadJkFBSIna9HQ8DLrt6BuFldaHvxXvUJDaDr9ypM4hRKHyGg5ycliU4GHQeRtXKFiCFQT7hcJw',
                stat1: { value: '300%', label: 'Increase in Leads' },
                stat2: { value: '2.5x', label: 'Faster Load Times' }
            },
            {
                quote: 'Their team delivered a <span class="bg-primary/10 text-primary px-2 rounded">production-ready platform in half the time</span> we expected. Exceptional engineering and communication throughout.',
                name: 'Marcus Chen',
                role: 'CTO, FinEdge',
                avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBIseH3-Wup4PNp9fJuYIuPzYVbl3d_K1aNM9Ix9auC1KuLcDpEodR1NGy1tBlQtVCGrYsC_bSbmLk10qOTghTzZA38smF0rjHgU8w-4B3ubkA8sjEzVYwgC5jnSbpXG6mE1FutQRTH8glUoqG_U2V4EHALmgHxEK1eSOTuy_83vzksC0EVbQ9rFJajioWsO857Pbvw1tdVBDBgQxQz6zOnfK5znPU6bmc60ZgFo5hfcW46B9tdDAsDkL-JgxqliaCMrhwgNNCa4A',
                stat1: { value: '50%', label: 'Faster Time to Market' },
                stat2: { value: '99.9%', label: 'Platform Uptime' }
            },
            {
                quote: 'From strategy to launch, WebHouse was a true partner. They <span class="bg-primary/10 text-primary px-2 rounded">scaled our e-commerce revenue by 4x</span> within the first year.',
                name: 'Elena Rodriguez',
                role: 'VP of Digital, RetailCo',
                avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuAH15Z2nl8xnAXd1fgMorN6oQcttWRkTTGRsHRyYKj6VA-L9jmuKYsBMpO4uZIKJH1SM4GWM-nn8NWNkEUOgJksz8EMMlf6vdXnIzyAxdVAltewRzKqefAo80iUnFtTFfbYfVxTfYI8DHPCGJ2X91bNxcAaB5fNoeZIg8ZG_CCb4lM9g9MJPZUanv2zBXy_Iv9iWcpNaY7cwd1RGFQAKbOs8O1hAacv2Su8H-JIrVUbPhqh0vcCr0PeNaD-MmvESmMmvRQFV8Do9w',
                stat1: { value: '4x', label: 'Revenue Growth' },
                stat2: { value: '45%', label: 'Higher Conversion' }
            }
        ];

        let currentIndex = 0;
        const quoteEl = carousel.querySelector('[data-testimonial-quote]');
        const avatarEl = carousel.querySelector('[data-testimonial-avatar]');
        const nameEl = carousel.querySelector('[data-testimonial-name]');
        const roleEl = carousel.querySelector('[data-testimonial-role]');
        const stat1ValueEl = carousel.querySelector('[data-testimonial-stat1-value]');
        const stat1LabelEl = carousel.querySelector('[data-testimonial-stat1-label]');
        const stat2ValueEl = carousel.querySelector('[data-testimonial-stat2-value]');
        const stat2LabelEl = carousel.querySelector('[data-testimonial-stat2-label]');
        const prevBtn = carousel.querySelector('[data-testimonial-prev]');
        const nextBtn = carousel.querySelector('[data-testimonial-next]');

        function showTestimonial(index) {
            const t = testimonials[index];
            quoteEl.innerHTML = t.quote;
            avatarEl.src = t.avatar;
            avatarEl.alt = t.name;
            nameEl.textContent = t.name;
            roleEl.textContent = t.role;
            stat1ValueEl.textContent = t.stat1.value;
            stat1LabelEl.textContent = t.stat1.label;
            stat2ValueEl.textContent = t.stat2.value;
            stat2LabelEl.textContent = t.stat2.label;
        }

        prevBtn?.addEventListener('click', () => {
            currentIndex = (currentIndex - 1 + testimonials.length) % testimonials.length;
            showTestimonial(currentIndex);
        });

        nextBtn?.addEventListener('click', () => {
            currentIndex = (currentIndex + 1) % testimonials.length;
            showTestimonial(currentIndex);
        });

        showTestimonial(0);
    }

    // Methodology Accordion
    function initAccordion() {
        const accordion = document.querySelector('[data-accordion]');
        if (!accordion) return;

        const items = accordion.querySelectorAll('[data-accordion-item]');

        function setItemState(item, isOpen) {
            const content = item.querySelector('[data-accordion-content]');
            const icon = item.querySelector('[data-accordion-icon]');
            const number = item.querySelector('[data-accordion-number]');

            if (isOpen) {
                item.setAttribute('data-accordion-open', '');
                content.style.maxHeight = content.scrollHeight + 'px';
                content.classList.remove('max-h-0');
                icon.classList.add('rotate-45', 'text-primary');
                number.classList.remove('bg-gray-100', 'text-gray-500');
                number.classList.add('bg-primary/10', 'text-primary');
            } else {
                item.removeAttribute('data-accordion-open');
                content.style.maxHeight = '0px';
                content.classList.add('max-h-0');
                icon.classList.remove('rotate-45', 'text-primary');
                number.classList.add('bg-gray-100', 'text-gray-500');
                number.classList.remove('bg-primary/10', 'text-primary');
            }
        }

        items.forEach(item => {
            const trigger = item.querySelector('[data-accordion-trigger]');
            const isInitiallyOpen = item.hasAttribute('data-accordion-open');

            if (isInitiallyOpen) {
                const content = item.querySelector('[data-accordion-content]');
                content.style.maxHeight = content.scrollHeight + 'px';
                item.querySelector('[data-accordion-icon]')?.classList.add('rotate-45', 'text-primary');
            } else {
                setItemState(item, false);
            }

            trigger?.addEventListener('click', () => {
                const isOpen = item.hasAttribute('data-accordion-open');
                items.forEach(other => {
                    if (other !== item) setItemState(other, false);
                });
                setItemState(item, !isOpen);
            });
        });
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
        initNewsletterForms();
        initContactForm();
        initConsultForms();
        initClickableCards();
        initCaseStudyFilters();
        initTestimonialCarousel();
        initAccordion();
    }

    // Start initialization
    init();
})();

