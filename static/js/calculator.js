class CostCalculator {
    constructor() {
        this.form = document.getElementById('calculatorForm');
        this.serviceSelect = document.getElementById('service');
        this.resultSection = document.getElementById('resultSection');
        this.costChart = null;
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        this.serviceSelect.addEventListener('change', () => this.toggleServiceOptions());
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    toggleServiceOptions() {
        const service = this.serviceSelect.value;
        document.querySelectorAll('.service-options').forEach(el => el.classList.add('d-none'));
        
        if (service) {
            document.getElementById(`${service}Options`)?.classList.remove('d-none');
        }
    }

    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.form);
        const data = Object.fromEntries(formData.entries());
        
        try {
            const response = await fetch('/api/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            
            if (result.success) {
                this.displayResults(result.calculation);
            } else {
                this.showError(result.error);
            }
        } catch (error) {
            this.showError('An error occurred while calculating costs');
        }
    }

    displayResults(calculation) {
        this.resultSection.classList.remove('d-none');
        document.getElementById('totalCost').textContent = 
            `$${calculation.totalCost.toFixed(2)}`;
        
        this.updateCostChart(calculation);
        this.updateCostDetails(calculation);
    }

    updateCostChart(calculation) {
        const ctx = document.getElementById('costChart').getContext('2d');
        
        if (this.costChart) {
            this.costChart.destroy();
        }
        
        this.costChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: ['Service Cost', 'Estimated Tax (10%)'],
                datasets: [{
                    data: [calculation.totalCost, calculation.totalCost * 0.1],
                    backgroundColor: ['#007bff', '#6c757d']
                }]
            },
            options: {
                responsive: true
            }
        });
    }

    updateCostDetails(calculation) {
        const detailsContainer = document.getElementById('costDetails');
        const details = calculation.details;
        
        let html = '<table class="table table-striped">';
        html += '<tbody>';
        
        for (const [key, value] of Object.entries(details)) {
            html += `
                <tr>
                    <td>${this.formatLabel(key)}</td>
                    <td>${this.formatValue(key, value)}</td>
                </tr>
            `;
        }
        
        html += '</tbody></table>';
        detailsContainer.innerHTML = html;
    }

    formatLabel(key) {
        return key.split('_')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }

    formatValue(key, value) {
        if (typeof value === 'number') {
            return key.includes('price') ? `$${value.toFixed(4)}` : value.toFixed(2);
        }
        return value;
    }

    showError(message) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        
        this.resultSection.classList.add('d-none');
        this.form.appendChild(errorDiv);
        
        setTimeout(() => errorDiv.remove(), 5000);
    }
}

// Initialize the calculator when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new CostCalculator();
}); 