class SearchAutocomplete {
    constructor(options) {
        this.input = document.querySelector(options.inputSelector);
        this.resultsContainer = document.querySelector(options.resultsContainerSelector);
        this.url = options.url;
        this.minLength = options.minLength || 2;
        this.debounceTime = options.debounceTime || 300;
        this.timeout = null;

        this.init();
    }

    init() {
        this.input.addEventListener('input', () => {
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => this.search(), this.debounceTime);
        });

        this.input.addEventListener('blur', () => {
            setTimeout(() => {
                this.resultsContainer.style.display = 'none';
            }, 200);
        });

        // Close results when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.input.contains(e.target) && !this.resultsContainer.contains(e.target)) {
                this.resultsContainer.style.display = 'none';
            }
        });
    }

    async search() {
        const query = this.input.value.trim();
        if (query.length < this.minLength) {
            this.resultsContainer.style.display = 'none';
            return;
        }

        try {
            const response = await fetch(`${this.url}?query=${encodeURIComponent(query)}`);
            const data = await response.json();
            this.displayResults(data.results);
        } catch (error) {
            console.error('Error fetching search results:', error);
        }
    }

    displayResults(results) {
        if (!results.length) {
            this.resultsContainer.style.display = 'none';
            return;
        }

        this.resultsContainer.innerHTML = results.map(result => this.createResultItem(result)).join('');
        this.resultsContainer.style.display = 'block';
    }

    createResultItem(result) {
        const imageHtml = result.image ? 
            `<img src="${result.image}" alt="${result.name}" class="search-result-image">` : 
            '';

        const priceHtml = this.formatPrice(result);

        return `
            <div class="search-result-item">
                ${imageHtml}
                <div class="search-result-info">
                    <div class="search-result-name">${result.name}</div>
                    <div class="search-result-description">${result.description}</div>
                    ${priceHtml}
                </div>
            </div>
        `;
    }

    formatPrice(result) {
        if (!result.price) return '';

        if (result.discounted_price) {
            return `
                <div class="search-result-price-container">
                    <span class="search-result-original-price">$${result.price}</span>
                    <span class="search-result-price discounted">$${result.discounted_price}</span>
                </div>
            `;
        }

        return `<div class="search-result-price">$${result.price}</div>`;
    }
} 