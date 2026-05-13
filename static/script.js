document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('summarize-form');
    const urlInput = document.getElementById('url-input');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.querySelector('.btn-text');
    const spinner = document.querySelector('.spinner');
    
    const resultContainer = document.getElementById('result-container');
    const summaryContent = document.getElementById('summary-content');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) return;

        // Update UI state
        setLoading(true);
        resultContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || data.error || 'An unexpected error occurred');
            }

            // Show result
            summaryContent.innerHTML = marked.parse(data.summary);
            resultContainer.classList.remove('hidden');

        } catch (error) {
            // Show error
            errorMessage.textContent = error.message;
            errorContainer.classList.remove('hidden');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        urlInput.disabled = isLoading;
        
        if (isLoading) {
            btnText.classList.add('hidden');
            spinner.classList.remove('hidden');
        } else {
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
        }
    }
});
