/* ============================================
   VlogVerse - Premium Interactive Animations
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    'use strict';

    // ============================================
    // 1. Particle System
    // ============================================
    const particlesContainer = document.getElementById('particles');
    const particleCount = window.innerWidth < 768 ? 30 : 60;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        
        const size = Math.random() * 3 + 2;
        const posX = Math.random() * 100;
        const duration = Math.random() * 15 + 10;
        const delay = Math.random() * 10;
        const opacity = Math.random() * 0.4 + 0.1;
        
        particle.style.cssText = `
            left: ${posX}%;
            width: ${size}px;
            height: ${size}px;
            animation-duration: ${duration}s;
            animation-delay: ${delay}s;
            opacity: ${opacity};
        `;
        
        particlesContainer.appendChild(particle);
    }

    // ============================================
    // 2. Navigation Scroll Effect
    // ============================================
    const nav = document.querySelector('.nav');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.scrollY;
        
        if (currentScroll > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
        
        lastScroll = currentScroll;
    }, { passive: true });

    // ============================================
    // 3. Mobile Menu Toggle
    // ============================================
    const navToggle = document.getElementById('navToggle');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileLinks = document.querySelectorAll('.mobile-link');

    function toggleMenu() {
        navToggle.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }

    navToggle.addEventListener('click', toggleMenu);

    mobileLinks.forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    // Close mobile menu on resize to desktop
    window.addEventListener('resize', () => {
        if (window.innerWidth > 900 && mobileMenu.classList.contains('active')) {
            toggleMenu();
        }
    });

    // ============================================
    // 4. Counter Animation
    // ============================================
    const statNumbers = document.querySelectorAll('.stat-number');
    let countersAnimated = false;

    function animateCounters() {
        if (countersAnimated) return;
        
        statNumbers.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000;
            const steps = 60;
            const increment = target / steps;
            let current = 0;
            let step = 0;

            const updateCounter = () => {
                step++;
                current = Math.min(current + increment, target);
                counter.textContent = Math.floor(current);
                
                if (step < steps) {
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                    countersAnimated = true;
                }
            };

            updateCounter();
        });
    }

    // Trigger counter animation when hero is in view
    const heroStats = document.querySelector('.hero-stats');
    if (heroStats) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(heroStats);
    }

    // ============================================
    // 5. Scroll Reveal for Feature Cards
    // ============================================
    const featureCards = document.querySelectorAll('.feature-card');

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const card = entry.target;
                const delay = parseInt(card.getAttribute('data-delay')) || 0;
                
                setTimeout(() => {
                    card.classList.add('visible');
                    card.style.animationDelay = '0s';
                }, delay);
                
                revealObserver.unobserve(card);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    featureCards.forEach(card => revealObserver.observe(card));

    // ============================================
    // 6. Smooth Hover Effects for Nav Links
    // ============================================
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-1px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // ============================================
    // 7. Parallax Effect on Floating Shapes
    // ============================================
    const shapes = document.querySelectorAll('.shape');
    
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        shapes.forEach((shape, index) => {
            const speed = (index + 1) * 15;
            const moveX = (x - 0.5) * speed;
            const moveY = (y - 0.5) * speed;
            
            shape.style.transform = `translate(${moveX}px, ${moveY}px)`;
        });
    });

    // ============================================
    // 8. Typing/Text Effect for Hero Subtitle
    // ============================================
    const heroDescription = document.querySelector('.hero-description');
    if (heroDescription) {
        heroDescription.style.opacity = '0';
        setTimeout(() => {
            heroDescription.style.transition = 'opacity 1s ease-out';
            heroDescription.style.opacity = '1';
        }, 1200);
    }

    // ============================================
    // 9. Button Ripple Effect
    // ============================================
    document.querySelectorAll('.btn-hero-primary, .btn-hero-secondary').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.style.cssText = `
                position: absolute;
                width: 20px;
                height: 20px;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                left: ${x - 10}px;
                top: ${y - 10}px;
                transform: scale(0);
                animation: rippleEffect 0.6s ease-out;
                pointer-events: none;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Add ripple keyframe dynamically
    const style = document.createElement('style');
    style.textContent = `
        @keyframes rippleEffect {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    // ============================================
    // 10. Loading Animation (initial page load)
    // ============================================
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-out';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);

    // ============================================
    // 11. Password Visibility Toggle
    // ============================================
    document.querySelectorAll('.password-toggle').forEach(btn => {
        btn.addEventListener('click', function() {
            const input = this.parentElement.querySelector('.form-input');
            if (!input) return;
            
            const icon = this.querySelector('i');
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // ============================================
    // 12. Form Submission Animation
    // ============================================
    document.querySelectorAll('.auth-submit').forEach(btn => {
        btn.addEventListener('click', function(e) {
            const form = this.closest('form');
            if (!form || !form.getAttribute('action') || form.getAttribute('action') === '#') return;
            
            if (!form.checkValidity()) {
                return;
            }
            
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            // this.disabled = true;
            
            // Re-enable if form submission takes too long (for demo)
            setTimeout(() => {
                if (this.disabled) {
                    this.innerHTML = originalText;
                    this.disabled = false;
                }
            }, 5000);
        });
    });

    // ============================================
    // 13. Form Input Auto-fill Detection (has-value class)
    // ============================================
    document.querySelectorAll('.form-input').forEach(input => {
        if (input.value) {
            input.classList.add('has-value');
        }
        input.addEventListener('input', function() {
            if (this.value) {
                this.classList.add('has-value');
            } else {
                this.classList.remove('has-value');
            }
        });
    });

    // ============================================
    // 14. Auto-focus first input on auth pages
    // ============================================
    const authSection = document.querySelector('.auth-section');
    if (authSection) {
        const firstInput = authSection.querySelector('.form-input');
        if (firstInput) {
            setTimeout(() => firstInput.focus(), 600);
        }
    }

    console.log('VlogVerse loaded! 🚀');
});
