/**
 * SPNK - Sissy Punk Unhinged
 * Countdown Timer Functions
 */

/**
 * Initialize a countdown timer to a specific date
 * @param {string} targetDate - Target date in ISO format (e.g. "2024-12-31T00:00:00")
 * @param {string} daysElement - ID of element to display days
 * @param {string} hoursElement - ID of element to display hours
 * @param {string} minutesElement - ID of element to display minutes
 * @param {string} secondsElement - ID of element to display seconds
 */
function initCountdown(targetDate, daysElement, hoursElement, minutesElement, secondsElement) {
    // Get target date
    const targetTime = new Date(targetDate).getTime();
    
    // Get HTML elements
    const daysEl = document.getElementById(daysElement);
    const hoursEl = document.getElementById(hoursElement);
    const minutesEl = document.getElementById(minutesElement);
    const secondsEl = document.getElementById(secondsElement);
    
    if (!daysEl || !hoursEl || !minutesEl || !secondsEl) {
        console.error('Countdown elements not found.');
        return;
    }
    
    // Update the countdown every second
    const countdownTimer = setInterval(function() {
        // Get current date and time
        const now = new Date().getTime();
        
        // Calculate the distance between now and the target date
        const distance = targetTime - now;
        
        // If the countdown is finished, show a message
        if (distance < 0) {
            clearInterval(countdownTimer);
            daysEl.innerHTML = '00';
            hoursEl.innerHTML = '00';
            minutesEl.innerHTML = '00';
            secondsEl.innerHTML = '00';
            
            // Add glitch effect to show completion
            const countdownItems = [daysEl, hoursEl, minutesEl, secondsEl];
            countdownItems.forEach(item => {
                item.classList.add('glitching');
                
                // Add extra visual effect
                item.style.color = 'var(--neon-green)';
                
                // Make parent container glitch if possible
                const container = item.closest('.countdown-container, .main-countdown');
                if (container) {
                    container.classList.add('completed');
                    
                    // Add glitch overlay
                    const overlay = document.createElement('div');
                    overlay.classList.add('glitch-overlay');
                    container.appendChild(overlay);
                }
            });
            
            return;
        }
        
        // Time calculations for days, hours, minutes and seconds
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        // Display the result with leading zeros
        daysEl.innerHTML = days < 10 ? `0${days}` : days;
        hoursEl.innerHTML = hours < 10 ? `0${hours}` : hours;
        minutesEl.innerHTML = minutes < 10 ? `0${minutes}` : minutes;
        secondsEl.innerHTML = seconds < 10 ? `0${seconds}` : seconds;
        
        // Add glitch effect randomly
        if (Math.random() > 0.97) { // 3% chance per second
            const randomElement = [daysEl, hoursEl, minutesEl, secondsEl][Math.floor(Math.random() * 4)];
            
            // Apply quick glitch effect
            randomElement.classList.add('glitching');
            
            // Temporarily change the value for glitch effect
            const originalValue = randomElement.innerHTML;
            const glitchValue = Math.floor(Math.random() * 99).toString().padStart(2, '0');
            randomElement.innerHTML = glitchValue;
            
            // Reset after a short delay
            setTimeout(() => {
                randomElement.innerHTML = originalValue;
                randomElement.classList.remove('glitching');
            }, 150);
        }
        
    }, 1000);
}

/**
 * Create visual glitch effect when countdown is about to end
 * @param {number} timeLeftSeconds - Seconds left until target date
 * @param {Array} elements - Array of elements to apply effect to
 */
function intensifyGlitchEffect(timeLeftSeconds, elements) {
    if (timeLeftSeconds <= 60) { // Last minute
        elements.forEach(element => {
            element.classList.add('intense-glitch');
            
            // Add visual disruption
            const parent = element.parentElement;
            if (parent) {
                parent.style.transform = `translate(${(Math.random() - 0.5) * 5}px, ${(Math.random() - 0.5) * 5}px)`;
                
                setTimeout(() => {
                    parent.style.transform = '';
                }, 100);
            }
        });
    }
    else if (timeLeftSeconds <= 300) { // Last 5 minutes
        // Occasional glitch
        if (Math.random() > 0.7) {
            const randomElement = elements[Math.floor(Math.random() * elements.length)];
            randomElement.classList.add('medium-glitch');
            
            setTimeout(() => {
                randomElement.classList.remove('medium-glitch');
            }, 200);
        }
    }
}

/**
 * Adds a visual flash effect to countdown containers
 * @param {string} containerSelector - CSS selector for container elements
 */
function addCountdownFlashEffect(containerSelector) {
    const containers = document.querySelectorAll(containerSelector);
    
    containers.forEach(container => {
        // Random interval for the effect
        setInterval(() => {
            if (Math.random() > 0.9) { // 10% chance
                container.classList.add('flash-effect');
                
                setTimeout(() => {
                    container.classList.remove('flash-effect');
                }, 100);
            }
        }, 2000);
    });
}
