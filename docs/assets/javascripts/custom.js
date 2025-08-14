// Tavily Register Documentation - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all custom functionality
    initializeCodeCopyButtons();
    initializeTabSwitching();
    initializeScrollToTop();
    initializeSearchEnhancements();
    initializeThemeToggle();
    initializeProgressIndicator();
    initializeTooltips();
    initializeAnalytics();
});

// Enhanced code copy functionality
function initializeCodeCopyButtons() {
    const codeBlocks = document.querySelectorAll('pre code');
    
    codeBlocks.forEach(function(codeBlock) {
        const pre = codeBlock.parentElement;
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-button';
        copyButton.innerHTML = '📋';
        copyButton.title = 'Copy to clipboard';
        
        copyButton.addEventListener('click', function() {
            navigator.clipboard.writeText(codeBlock.textContent).then(function() {
                copyButton.innerHTML = '✅';
                copyButton.title = 'Copied!';
                setTimeout(function() {
                    copyButton.innerHTML = '📋';
                    copyButton.title = 'Copy to clipboard';
                }, 2000);
            });
        });
        
        pre.style.position = 'relative';
        pre.appendChild(copyButton);
    });
}

// Enhanced tab switching with URL hash support
function initializeTabSwitching() {
    const tabGroups = document.querySelectorAll('.tabbed-set');
    
    tabGroups.forEach(function(tabGroup) {
        const tabs = tabGroup.querySelectorAll('.tabbed-labels label');
        const contents = tabGroup.querySelectorAll('.tabbed-content');
        
        tabs.forEach(function(tab, index) {
            tab.addEventListener('click', function() {
                // Update URL hash
                const tabId = tab.getAttribute('for');
                if (tabId) {
                    history.replaceState(null, null, '#' + tabId);
                }
                
                // Add analytics tracking
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'tab_switch', {
                        'tab_name': tab.textContent.trim(),
                        'tab_group': index
                    });
                }
            });
        });
    });
    
    // Handle initial hash
    if (window.location.hash) {
        const targetTab = document.querySelector(`label[for="${window.location.hash.slice(1)}"]`);
        if (targetTab) {
            targetTab.click();
        }
    }
}

// Scroll to top functionality
function initializeScrollToTop() {
    const scrollButton = document.createElement('button');
    scrollButton.className = 'scroll-to-top';
    scrollButton.innerHTML = '↑';
    scrollButton.title = 'Scroll to top';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--tr-primary-color);
        color: white;
        border: none;
        cursor: pointer;
        opacity: 0;
        transition: opacity 0.3s ease;
        z-index: 1000;
        font-size: 20px;
    `;
    
    document.body.appendChild(scrollButton);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.opacity = '1';
        } else {
            scrollButton.style.opacity = '0';
        }
    });
    
    scrollButton.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
        
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'scroll_to_top', {
                'scroll_position': window.pageYOffset
            });
        }
    });
}

// Enhanced search functionality
function initializeSearchEnhancements() {
    const searchInput = document.querySelector('.md-search__input');
    if (!searchInput) return;
    
    // Add search suggestions
    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase();
        if (query.length > 2) {
            // Track search queries for analytics
            if (typeof gtag !== 'undefined') {
                gtag('event', 'search', {
                    'search_term': query
                });
            }
        }
    });
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            searchInput.focus();
        }
        
        // Escape to clear search
        if (e.key === 'Escape' && document.activeElement === searchInput) {
            searchInput.value = '';
            searchInput.blur();
        }
    });
}

// Theme toggle enhancements
function initializeThemeToggle() {
    const themeToggle = document.querySelector('[data-md-component="palette"]');
    if (!themeToggle) return;
    
    themeToggle.addEventListener('change', function() {
        const isDark = document.querySelector('[data-md-color-scheme="slate"]');
        
        // Save theme preference
        localStorage.setItem('theme-preference', isDark ? 'dark' : 'light');
        
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'theme_change', {
                'theme': isDark ? 'dark' : 'light'
            });
        }
    });
}

// Reading progress indicator
function initializeProgressIndicator() {
    const progressBar = document.createElement('div');
    progressBar.className = 'reading-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, var(--tr-primary-color), var(--tr-accent-color));
        z-index: 1001;
        transition: width 0.1s ease;
    `;
    
    document.body.appendChild(progressBar);
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrollPercent = (scrollTop / docHeight) * 100;
        
        progressBar.style.width = Math.min(scrollPercent, 100) + '%';
    });
}

// Enhanced tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[title]');
    
    tooltipElements.forEach(function(element) {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'custom-tooltip';
            tooltip.textContent = this.title;
            tooltip.style.cssText = `
                position: absolute;
                background: var(--md-default-bg-color);
                border: 1px solid var(--md-default-fg-color--lightest);
                border-radius: 4px;
                padding: 8px 12px;
                font-size: 14px;
                z-index: 1002;
                box-shadow: var(--tr-box-shadow);
                pointer-events: none;
            `;
            
            document.body.appendChild(tooltip);
            
            // Remove original title to prevent default tooltip
            this.setAttribute('data-original-title', this.title);
            this.removeAttribute('title');
            
            // Position tooltip
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.bottom + 5) + 'px';
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.custom-tooltip');
            if (tooltip) {
                tooltip.remove();
            }
            
            // Restore original title
            const originalTitle = this.getAttribute('data-original-title');
            if (originalTitle) {
                this.title = originalTitle;
                this.removeAttribute('data-original-title');
            }
        });
    });
}

// Analytics and tracking
function initializeAnalytics() {
    // Track page views
    if (typeof gtag !== 'undefined') {
        gtag('config', 'GA_MEASUREMENT_ID', {
            page_title: document.title,
            page_location: window.location.href
        });
    }
    
    // Track external links
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.hostname !== window.location.hostname) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'click', {
                    event_category: 'outbound',
                    event_label: link.href,
                    transport_type: 'beacon'
                });
            }
        }
    });
    
    // Track download links
    document.addEventListener('click', function(e) {
        const link = e.target.closest('a');
        if (link && link.href.match(/\.(pdf|zip|tar|gz|exe|dmg)$/i)) {
            if (typeof gtag !== 'undefined') {
                gtag('event', 'file_download', {
                    file_name: link.href.split('/').pop(),
                    file_url: link.href
                });
            }
        }
    });
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export for use in other scripts
window.TavilyDocs = {
    initializeCodeCopyButtons,
    initializeTabSwitching,
    initializeScrollToTop,
    debounce,
    throttle
};
