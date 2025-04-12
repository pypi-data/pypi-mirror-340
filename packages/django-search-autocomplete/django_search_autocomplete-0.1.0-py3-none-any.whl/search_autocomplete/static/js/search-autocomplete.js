class SearchAutocomplete {
    constructor(options) {
        this.options = {
            inputSelector: '#search-input',
            resultsContainerSelector: '#search-results',
            url: '/search/',
            minLength: 2,
            debounceTime: 300,
            ...options
        };
        
        this.input = document.querySelector(this.options.inputSelector);
        this.resultsContainer = document.querySelector(this.options.resultsContainerSelector);
        this.timeout = null;
        
        this.initialize();
    }
    
    initialize() {
        if (!this.input || !this.resultsContainer) {
            console.error('Search input or results container not found');
            return;
        }
        
        this.input.addEventListener('input', this.handleInput.bind(this));
        document.addEventListener('click', this.handleDocumentClick.bind(this));
    }
    
    handleInput(event) {
        const query = event.target.value.trim();
        
        if (query.length < this.options.minLength) {
            this.hideResults();
            return;
        }
        
        clearTimeout(this.timeout);
        this.timeout = setTimeout(() => {
            this.search(query);
        }, this.options.debounceTime);
    }
    
    async search(query) {
        try {
            const response = await fetch(`${this.options.url}?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displayResults(data.results);
        } catch (error) {
            console.error('Search error:', error);
        }
    }
    
    displayResults(results) {
        if (!results || results.length === 0) {
            this.hideResults();
            return;
        }
        
        const html = results.map(result => this.createResultItem(result)).join('');
        this.resultsContainer.innerHTML = html;
        this.resultsContainer.style.display = 'block';
    }
    
    createResultItem(result) {
        return `
            <div class="search-result-item">
                ${result.image ? `<img src="${result.image}" alt="${result.name}" class="search-result-image">` : ''}
                <div class="search-result-content">
                    <div class="search-result-title">${result.name}</div>
                    ${result.price ? `
                        <div class="search-result-price">
                            ${result.discounted_price ? 
                                `<span class="original-price">${result.price}</span>
                                 <span class="discounted-price">${result.discounted_price}</span>` :
                                result.price
                            }
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }
    
    hideResults() {
        this.resultsContainer.style.display = 'none';
    }
    
    handleDocumentClick(event) {
        if (!this.resultsContainer.contains(event.target) && event.target !== this.input) {
            this.hideResults();
        }
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SearchAutocomplete;
} 