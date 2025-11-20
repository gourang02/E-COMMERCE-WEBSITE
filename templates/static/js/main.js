// ==========================================
// OPTICAL SHOP - CUSTOM JAVASCRIPT
// ==========================================

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all features
    initScrollAnimations();
    initFormValidation();
    initQuantityControls();
    initImageZoom();
    initTooltips();
    initSearchFilter();
    initCartCounter();
    initSmoothScroll();
    initBackToTop();
    initAlertAutoClose();
    
    console.log('Optical Shop initialized successfully! 🚀');
});

// ==========================================
// SCROLL ANIMATIONS
// ==========================================
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, {
        threshold: 0.1
    });

    // Observe all cards
    document.querySelectorAll('.card, .product-card').forEach(card => {
        observer.observe(card);
    });
}

// ==========================================
// FORM VALIDATION
// ==========================================
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });

        // Real-time email validation
        const emailInputs = form.querySelectorAll('input[type="email"]');
        emailInputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateEmail(this);
            });
        });

        // Password confirmation validation
        const passwordInput = form.querySelector('input[name="password"]');
        const confirmInput = form.querySelector('input[name="confirm_password"]');
        
        if (passwordInput && confirmInput) {
            confirmInput.addEventListener('input', function() {
                if (this.value !== passwordInput.value) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
    });
}

function validateEmail(input) {
    const email = input.value;
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!regex.test(email)) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else {
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
    }
}

// ==========================================
// QUANTITY CONTROLS
// ==========================================
function initQuantityControls() {
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    
    quantityInputs.forEach(input => {
        // Create + and - buttons if they don't exist
        if (!input.parentElement.classList.contains('quantity-control')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'quantity-control d-flex align-items-center';
            
            const decreaseBtn = document.createElement('button');
            decreaseBtn.type = 'button';
            decreaseBtn.className = 'btn btn-sm btn-outline-secondary';
            decreaseBtn.innerHTML = '<i class="fas fa-minus"></i>';
            decreaseBtn.onclick = () => changeQuantity(input, -1);
            
            const increaseBtn = document.createElement('button');
            increaseBtn.type = 'button';
            increaseBtn.className = 'btn btn-sm btn-outline-secondary';
            increaseBtn.innerHTML = '<i class="fas fa-plus"></i>';
            increaseBtn.onclick = () => changeQuantity(input, 1);
            
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(decreaseBtn);
            wrapper.appendChild(input);
            wrapper.appendChild(increaseBtn);
        }
    });
}

function changeQuantity(input, change) {
    const currentValue = parseInt(input.value) || 0;
    const min = parseInt(input.min) || 1;
    const max = parseInt(input.max) || 999;
    const newValue = Math.max(min, Math.min(max, currentValue + change));
    
    input.value = newValue;
    input.dispatchEvent(new Event('change'));
}

// ==========================================
// IMAGE ZOOM
// ==========================================
function initImageZoom() {
    const productImages = document.querySelectorAll('.product-card img, .card img');
    
    productImages.forEach(img => {
        img.addEventListener('mouseenter', function() {
            this.style.cursor = 'zoom-in';
        });
        
        img.addEventListener('click', function(e) {
            if (this.closest('.product-card') || this.closest('.card-img-top')) {
                showImageModal(this.src, this.alt);
            }
        });
    });
}

function showImageModal(src, alt) {
    const modal = document.createElement('div');
    modal.className = 'modal fade show';
    modal.style.display = 'block';
    modal.style.backgroundColor = 'rgba(0,0,0,0.8)';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content bg-transparent border-0">
                <div class="modal-body p-0 text-center">
                    <img src="${src}" alt="${alt}" class="img-fluid rounded" style="max-height: 80vh;">
                    <button type="button" class="btn btn-light position-absolute top-0 end-0 m-3" onclick="this.closest('.modal').remove()">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    });
}

// ==========================================
// TOOLTIPS INITIALIZATION
// ==========================================
function initTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ==========================================
// SEARCH & FILTER
// ==========================================
function initSearchFilter() {
    const searchInput = document.querySelector('#searchProducts');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const products = document.querySelectorAll('.product-card');
            
            products.forEach(product => {
                const title = product.querySelector('.card-title').textContent.toLowerCase();
                const description = product.querySelector('.card-text')?.textContent.toLowerCase() || '';
                
                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    product.closest('.col-md-3, .col-md-4').style.display = '';
                } else {
                    product.closest('.col-md-3, .col-md-4').style.display = 'none';
                }
            });
        });
    }
}

// ==========================================
// CART COUNTER ANIMATION
// ==========================================
function initCartCounter() {
    const cartBadge = document.querySelector('.cart-badge');
    
    if (cartBadge) {
        // Animate when cart is updated
        const observer = new MutationObserver(() => {
            cartBadge.classList.add('animate__animated', 'animate__bounce');
            setTimeout(() => {
                cartBadge.classList.remove('animate__animated', 'animate__bounce');
            }, 1000);
        });
        
        observer.observe(cartBadge, { childList: true, characterData: true, subtree: true });
    }
}

// ==========================================
// SMOOTH SCROLL
// ==========================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                document.querySelector(href).scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ==========================================
// BACK TO TOP BUTTON
// ==========================================
function initBackToTop() {
    const backToTopBtn = document.createElement('button');
    backToTopBtn.id = 'backToTop';
    backToTopBtn.className = 'btn btn-primary rounded-circle position-fixed';
    backToTopBtn.style.cssText = 'bottom: 20px; right: 20px; width: 50px; height: 50px; display: none; z-index: 999;';
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    document.body.appendChild(backToTopBtn);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });
    
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ==========================================
// AUTO CLOSE ALERTS
// ==========================================
function initAlertAutoClose() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
}

// ==========================================
// SHOW TOAST NOTIFICATION
// ==========================================
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// ==========================================
// ADD TO CART ANIMATION
// ==========================================
function animateAddToCart(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adding...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Added!';
        button.classList.remove('btn-primary');
        button.classList.add('btn-success');
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.classList.remove('btn-success');
            button.classList.add('btn-primary');
            button.disabled = false;
        }, 1000);
    }, 500);
}

// ==========================================
// LOADING OVERLAY
// ==========================================
function showLoading() {
    const overlay = document.createElement('div');
    overlay.id = 'loadingOverlay';
    overlay.className = 'spinner-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loadingOverlay');
    if (overlay) {
        overlay.remove();
    }
}

// ==========================================
// CONFIRM DELETE
// ==========================================
function confirmDelete(message = 'Are you sure you want to delete this item?') {
    return confirm(message);
}

// ==========================================
// FORMAT CURRENCY
// ==========================================
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// ==========================================
// UPDATE CART TOTAL
// ==========================================
function updateCartTotal() {
    const cartItems = document.querySelectorAll('.cart-item');
    let total = 0;
    
    cartItems.forEach(item => {
        const price = parseFloat(item.dataset.price);
        const quantity = parseInt(item.querySelector('input[type="number"]').value);
        total += price * quantity;
    });
    
    const totalElement = document.querySelector('#cartTotal');
    if (totalElement) {
        totalElement.textContent = formatCurrency(total);
    }
}

// ==========================================
// COPY TO CLIPBOARD
// ==========================================
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'danger');
    });
}

// ==========================================
// EXPORT FUNCTIONS FOR GLOBAL USE
// ==========================================
window.OpticalShop = {
    showToast,
    showLoading,
    hideLoading,
    confirmDelete,
    formatCurrency,
    updateCartTotal,
    copyToClipboard,
    animateAddToCart
};

// ==========================================
// KEYBOARD SHORTCUTS
// ==========================================
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + K for search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const searchInput = document.querySelector('#searchProducts');
        if (searchInput) {
            searchInput.focus();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => modal.remove());
    }
});

// ==========================================
// PERFORMANCE MONITORING
// ==========================================
if ('performance' in window) {
    window.addEventListener('load', () => {
        const perfData = performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`Page loaded in ${pageLoadTime}ms`);
    });
}

// ==========================================
// DARK MODE TOGGLE (Optional)
// ==========================================
function initDarkMode() {
    const darkModeToggle = document.querySelector('#darkModeToggle');
    
    if (darkModeToggle) {
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
        }
        
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
        });
    }
}

console.log('%c🛒 Optical Shop Ready! ', 'background: #2563eb; color: white; font-size: 16px; padding: 10px;');