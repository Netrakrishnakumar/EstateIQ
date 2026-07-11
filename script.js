/**
 * Estate IQ - Frontend JavaScript
 * Handles form submission, validation, and API calls for prediction
 */

document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('predictionForm');
    const predictButton = document.getElementById('predictButton');
    const buttonSpinner = predictButton.querySelector('.spinner-border');
    const buttonText = predictButton.querySelector('.button-text');
    const alertContainer = document.getElementById('alertContainer');
    const resultContainer = document.getElementById('resultContainer');
    const predictionValue = document.getElementById('predictionValue');

    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePrediction);
    }

    /**
     * Handle prediction form submission
     */
    async function handlePrediction(event) {
        event.preventDefault();

        // Reset previous results and alerts
        resetUI();

        // Validate form
        if (!predictionForm.checkValidity()) {
            predictionForm.classList.add('was-validated');
            showAlert('Please fill in all required fields correctly.', 'danger');
            return;
        }

        // Show loading state
        setLoading(true);

        // Gather form data (Updated with uppercase keys to match Flask validation)
        const formData = {
            Id: parseInt(document.getElementById('id').value),
            Area: parseFloat(document.getElementById('area').value),
            Bedrooms: parseInt(document.getElementById('bedrooms').value),
            Bathrooms: parseInt(document.getElementById('bathrooms').value),
            Floors: parseInt(document.getElementById('floors').value),
            YearBuilt: parseInt(document.getElementById('yearbuilt').value),
            Location: document.getElementById('location').value.trim(),
            Condition: document.getElementById('condition').value,
            Garage: document.getElementById('garage').value
        }; // Fixed: Added the missing closing bracket and semicolon here

        try {
            // Call prediction API
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok && data.success) {
                // Show success result
                showResult(data.prediction, data.currency);
                showAlert('Prediction completed successfully!', 'success');
            } else {
                // Show error message
                showAlert(data.error || 'Prediction failed. Please try again.', 'danger');
            }
        } catch (error) {
            console.error('Prediction error:', error);
            showAlert('An error occurred while processing your request. Please try again.', 'danger');
        } finally {
            setLoading(false);
        }
    }

    /**
     * Reset UI to initial state
     */
    function resetUI() {
        alertContainer.innerHTML = '';
        resultContainer.classList.add('d-none');
        if (predictionForm) {
            predictionForm.classList.remove('was-validated');
        }
    }

    /**
     * Set loading state for button
     */
    function setLoading(isLoading) {
        predictButton.disabled = isLoading;
        if (isLoading) {
            buttonSpinner.classList.remove('d-none');
            buttonText.textContent = 'Processing...';
        } else {
            buttonSpinner.classList.add('d-none');
            buttonText.textContent = 'Predict Price';
        }
    }

    /**
     * Show alert message
     */
    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.setAttribute('role', 'alert');
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        alertContainer.appendChild(alertDiv);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    /**
     * Show prediction result
     */
    function showResult(value, currency) {
        const formattedValue = formatCurrency(value, currency);
        predictionValue.textContent = formattedValue;
        resultContainer.classList.remove('d-none');
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    /**
     * Format currency value
     */
    function formatCurrency(value, currency = 'USD') {
        const formatter = new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency,
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });
        return formatter.format(value);
    }

    /**
     * Add input validation feedback
     */
    if (predictionForm) {
        const formInputs = predictionForm.querySelectorAll('input, select');
        formInputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                }
            });

            input.addEventListener('blur', function() {
                if (!this.checkValidity()) {
                    this.classList.add('is-invalid');
                }
            });
        });
    }
});