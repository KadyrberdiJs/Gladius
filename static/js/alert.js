document.getElementById('add-to-cart-form').addEventListener('submit', function(event) {
            event.preventDefault();
            let formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    return response.text().then(text => {
                        throw new Error(`Network response was not ok: ${response.status} - ${text}`);
                    });
                }
                return response.json();
            })
            .then(data => {
                // Create alert HTML from message
                const alertClass = data.success ? 'alert-success' : 'alert-error';
                const alertHtml = `
                    <div class="alert-container">
                        <div class="alert ${alertClass}">
                            ${data.message}
                        </div>
                    </div>
                `;
                document.getElementById('alert-placeholder').innerHTML = alertHtml;
                console.log('Response data:', data);
                // Auto-close after 5 seconds
                setTimeout(() => {
                    document.getElementById('alert-placeholder').innerHTML = '';
                }, 5000);
            })
            .catch(error => {
                console.error('Fetch error:', error);
            });

            // Handle close buttons
            // document.addEventListener('click', function(event) {
            //     if (event.target.classList.contains('close-alert')) {
            //         event.target.parentElement.remove();
            //     }
            // });
        });