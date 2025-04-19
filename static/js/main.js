/**
 * SPNK - Sissy Punk Unhinged
 * Main JavaScript File
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('SPNK protocol initialized...');
    
    // Initialize glitch effects
    initGlitchEffects();
    
    // Add page transition effects
    initPageTransitions();
    
    // Random glitch animation for images
    initRandomGlitchAnimation();
});

/**
 * Initialize glitch effects for text elements
 */
function initGlitchEffects() {
    // Randomly apply glitch effects to certain elements
    const glitchableElements = document.querySelectorAll('.navbar-brand, h1, h2, h3');
    
    glitchableElements.forEach(element => {
        // Random glitch effect on hover
        element.addEventListener('mouseover', function() {
            // Skip if element already has active glitch animation
            if (this.classList.contains('glitching')) return;
            
            this.classList.add('glitching');
            
            // Add extra glitch effect temporarily
            const intensity = Math.random() * 2 + 1;
            this.style.setProperty('--glitch-intensity', intensity.toString());
            
            // Remove extra effect after animation
            setTimeout(() => {
                this.classList.remove('glitching');
                this.style.removeProperty('--glitch-intensity');
            }, 1000);
        });
    });
    
    // Apply persistent random glitches to specific elements
    setInterval(() => {
        const randomElement = glitchableElements[Math.floor(Math.random() * glitchableElements.length)];
        
        if (randomElement && !randomElement.classList.contains('glitching')) {
            randomElement.classList.add('glitching');
            
            setTimeout(() => {
                randomElement.classList.remove('glitching');
            }, 500);
        }
    }, 5000); // Random glitch every 5 seconds
}

/**
 * Initialize page transition effects
 */
function initPageTransitions() {
    // Store the current page URL for comparison
    let currentPage = window.location.href;
    
    // Add click event listeners to all internal links
    document.querySelectorAll('a').forEach(link => {
        // Only handle internal links to the same site
        if (link.href.includes(window.location.origin) && 
            !link.getAttribute('target') && 
            link.href !== currentPage) {
            
            link.addEventListener('click', function(e) {
                // Skip if modifier keys are pressed (new tab/window)
                if (e.metaKey || e.ctrlKey) return;
                
                e.preventDefault();
                const targetUrl = this.href;
                
                // Apply exit animation
                document.querySelector('.page-content').style.opacity = '0';
                document.querySelector('.page-content').style.transform = 'translateY(20px)';
                
                // Navigate after animation
                setTimeout(() => {
                    window.location.href = targetUrl;
                }, 300);
            });
        }
    });
}

/**
 * Initialize random glitch animations for images
 */
function initRandomGlitchAnimation() {
    const images = document.querySelectorAll('.character-image img, .nft-image img');
    
    // Apply random glitch effect to images
    images.forEach(img => {
        img.addEventListener('load', function() {
            setInterval(() => {
                const shouldGlitch = Math.random() > 0.7; // 30% chance to glitch
                
                if (shouldGlitch) {
                    this.style.transform = `translate(${(Math.random() - 0.5) * 10}px, ${(Math.random() - 0.5) * 10}px)`;
                    this.style.filter = `hue-rotate(${Math.random() * 360}deg) saturate(${1 + Math.random()})`; 
                    
                    setTimeout(() => {
                        this.style.transform = '';
                        this.style.filter = '';
                    }, 100);
                }
            }, 3000); // Check every 3 seconds
        });
    });
}

/**
 * Apply scanline effect to video containers
 */
function addScanlineEffect() {
    const videoContainers = document.querySelectorAll('.video-container, .character-image-container');
    
    videoContainers.forEach(container => {
        // Create scanline overlay if it doesn't exist
        if (!container.querySelector('.scanline-overlay')) {
            const scanlineOverlay = document.createElement('div');
            scanlineOverlay.classList.add('scanline-overlay');
            container.appendChild(scanlineOverlay);
        }
    });
}

/**
 * Terminal typing effect
 * @param {string} elementSelector - CSS selector for the element to apply typing effect to
 * @param {number} speed - Typing speed in milliseconds
 */
function typeWriterEffect(elementSelector, speed = 50) {
    const element = document.querySelector(elementSelector);
    if (!element) return;
    
    const originalText = element.innerHTML;
    element.innerHTML = '';
    
    let i = 0;
    function typeWriter() {
        if (i < originalText.length) {
            element.innerHTML += originalText.charAt(i);
            i++;
            setTimeout(typeWriter, Math.random() * speed + speed / 2); // Random speed for more realistic typing
        }
    }
    
    typeWriter();
}

/**
 * Adds a visual corruption effect to an element
 * @param {HTMLElement} element - Element to corrupt
 * @param {number} duration - Duration of corruption in ms
 */
function visualCorruption(element, duration = 1000) {
    if (!element) return;
    
    // Save original state
    const originalTransform = element.style.transform;
    const originalFilter = element.style.filter;
    const originalColor = element.style.color;
    
    // Apply corruption
    element.style.transform = `skew(${(Math.random() - 0.5) * 10}deg)`;
    element.style.filter = `blur(${Math.random() * 3}px) hue-rotate(${Math.random() * 360}deg)`;
    element.style.color = '#ff00ff';
    
    // Restore original state after duration
    setTimeout(() => {
        element.style.transform = originalTransform;
        element.style.filter = originalFilter;
        element.style.color = originalColor;
    }, duration);
}
