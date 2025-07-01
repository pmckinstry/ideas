// Main JavaScript file for the web app

// Utility functions
const Utils = {
    // Show notification
    showNotification: function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(alertDiv);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    },

    // Format JSON for display
    formatJSON: function(obj) {
        try {
            return JSON.stringify(obj, null, 2);
        } catch (e) {
            return 'Error formatting JSON: ' + e.message;
        }
    },

    // Validate JSON string
    isValidJSON: function(str) {
        try {
            JSON.parse(str);
            return true;
        } catch (e) {
            return false;
        }
    },

    // Add loading state to element
    setLoading: function(element, loading = true) {
        if (loading) {
            element.classList.add('loading');
            element.disabled = true;
        } else {
            element.classList.remove('loading');
            element.disabled = false;
        }
    }
};

// API functions
const API = {
    // Make API request
    request: async function(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    },

    // Test hello endpoint
    testHello: async function() {
        try {
            const data = await this.request('/api/hello');
            return data;
        } catch (error) {
            throw error;
        }
    },

    // Test data endpoint
    testData: async function(method = 'GET', data = null) {
        try {
            const options = { method };
            if (data && method === 'POST') {
                options.body = JSON.stringify(data);
            }

            const response = await this.request('/api/data', options);
            return response;
        } catch (error) {
            throw error;
        }
    }
};

// Page initialization
document.addEventListener('DOMContentLoaded', function() {
    console.log('Web app initialized');

    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');

            // Skip empty or invalid href attributes
            if (!href || href === '#' || href === '#!') {
                return;
            }

            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading indicators to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('btn-loading')) {
                Utils.setLoading(this, true);
                setTimeout(() => Utils.setLoading(this, false), 2000);
            }
        });
    });

    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe cards for animation
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    Utils.showNotification('An error occurred. Please try again.', 'danger');
});

// Delete confirmation functions
const DeleteConfirm = {
    // Show delete confirmation modal
    showModal: function(thoughtId, thoughtTitle) {
        const modal = document.getElementById('deleteModal');
        const titleSpan = document.getElementById('thoughtTitle');
        const form = document.getElementById('deleteForm');

        if (modal && titleSpan && form) {
            titleSpan.textContent = thoughtTitle;
            form.action = `/thoughts/${thoughtId}/delete`;
            new bootstrap.Modal(modal).show();
        } else {
            console.error('Delete modal elements not found');
        }
    },

    // Confirm delete with custom message
    confirm: function(thoughtId, thoughtTitle, customMessage = null) {
        const message = customMessage || `Are you sure you want to delete "${thoughtTitle}"?`;
        if (confirm(message)) {
            window.location.href = `/thoughts/${thoughtId}/delete`;
        }
    }
};

// Export for use in other scripts
window.Utils = Utils;
window.API = API;
window.DeleteConfirm = DeleteConfirm;
