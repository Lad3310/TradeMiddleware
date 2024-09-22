document.addEventListener('DOMContentLoaded', function() {
    const auditTrailTable = document.getElementById('audit-trail-table');
    const fileUploadForm = document.getElementById('file-upload-form');
    const dashboardStats = document.getElementById('dashboard-stats');

    if (auditTrailTable) {
        initializeAuditTrail(auditTrailTable);
    }

    if (fileUploadForm) {
        initializeFileUpload(fileUploadForm);
    }

    if (dashboardStats) {
        fetchDashboardStats();
    }

    // Create persistent message area
    createPersistentMessageArea();
});

function initializeAuditTrail(table) {
    table.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('view-trades-btn')) {
            const auditLogId = e.target.getAttribute('data-audit-log-id');
            fetchProcessedTrades(auditLogId);
        }
    });

    const headers = table.querySelectorAll('th');
    headers.forEach(header => {
        header.addEventListener('click', () => {
            const column = header.dataset.column;
            const order = header.dataset.order = header.dataset.order === 'asc' ? 'desc' : 'asc';
            sortTable(table, column, order);
        });
    });
}

function initializeFileUpload(form) {
    console.log('Initializing file upload form');
    form.addEventListener('submit', function(e) {
        console.log('Form submit event triggered');
        e.preventDefault();
        const formData = new FormData(form);
        const submitButton = form.querySelector('button[type="submit"]');
        
        console.log('Form data:', formData);
        console.log('Submit button:', submitButton);

        // Disable the submit button to prevent multiple submissions
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Uploading...';
        }

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            console.log('Response received:', response);
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            showModal(data.status, data.message, data.details);
            updatePersistentMessage(data.status, data.message);
            if (data.status === 'success' || data.status === 'warning') {
                form.reset();
                fetchDashboardStats();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('error', 'An error occurred while uploading the file.');
            updatePersistentMessage('error', 'An error occurred while uploading the file.');
        })
        .finally(() => {
            // Re-enable the submit button
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Upload and Process';
            }
        });
    });
}

function fetchProcessedTrades(auditLogId) {
    fetch(`/api/trades/${auditLogId}`)
        .then(response => response.json())
        .then(data => {
            displayProcessedTrades(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showModal('error', 'An error occurred while fetching trade data.');
        });
}

function displayProcessedTrades(trades) {
    const modal = createModal('Processed Trades');
    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Trade ID</th>
                <th>Symbol</th>
                <th>Quantity</th>
                <th>Price</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            ${trades.map(trade => `
                <tr>
                    <td>${trade.trade_id}</td>
                    <td>${trade.symbol}</td>
                    <td>${trade.quantity}</td>
                    <td>${trade.price}</td>
                    <td>${trade.status}</td>
                </tr>
            `).join('')}
        </tbody>
    `;
    modal.querySelector('.modal-content').appendChild(table);
    document.body.appendChild(modal);
}

function sortTable(table, column, order) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const sortedRows = rows.sort((a, b) => {
        const aValue = a.querySelector(`td[data-column="${column}"]`).textContent;
        const bValue = b.querySelector(`td[data-column="${column}"]`).textContent;
        return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
    });
    tbody.innerHTML = '';
    sortedRows.forEach(row => tbody.appendChild(row));
}

function showModal(status, message, details = null) {
    const modal = createModal(status === 'success' ? 'Success' : status === 'warning' ? 'Warning' : 'Error');
    modal.classList.add(status);
    const content = document.createElement('div');
    content.innerHTML = `
        <p>${message}</p>
        ${details ? `
            <h4>API Simulation Details:</h4>
            <p>Attempts: ${details.total_attempts}</p>
            <p>Total Delay: ${details.total_delay.toFixed(2)} seconds</p>
            <p>Processed Rows: ${details.processed_rows}</p>
            <p>Failed Rows: ${details.failed_rows}</p>
            <p>Success Rate: ${(details.success_rate * 100).toFixed(2)}%</p>
        ` : ''}
    `;
    modal.querySelector('.modal-content').appendChild(content);
    document.body.appendChild(modal);

    // Add animation
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);

    // Auto-close after 5 seconds
    setTimeout(() => {
        closeModal(modal);
    }, 5000);
}

function createModal(title) {
    const modal = document.createElement('div');
    modal.className = 'modal';
    modal.innerHTML = `
        <div class="modal-content">
            <span class="close">&times;</span>
            <h2>${title}</h2>
        </div>
    `;
    modal.querySelector('.close').onclick = function() {
        closeModal(modal);
    };
    return modal;
}

function closeModal(modal) {
    modal.classList.remove('show');
    setTimeout(() => {
        document.body.removeChild(modal);
    }, 300);
}

function createPersistentMessageArea() {
    const messageArea = document.createElement('div');
    messageArea.id = 'persistent-message';
    messageArea.className = 'persistent-message';
    document.body.insertBefore(messageArea, document.body.firstChild);
}

function updatePersistentMessage(status, message) {
    const messageArea = document.getElementById('persistent-message');
    messageArea.className = `persistent-message ${status}`;
    messageArea.textContent = message;
    messageArea.style.display = 'block';

    // Hide the message after 5 seconds
    setTimeout(() => {
        messageArea.style.display = 'none';
    }, 5000);
}

function fetchDashboardStats() {
    fetch('/api/dashboard_stats')
        .then(response => response.json())
        .then(data => {
            updateDashboardStats(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function updateDashboardStats(data) {
    const statsContainer = document.getElementById('dashboard-stats');
    if (!statsContainer) return;

    statsContainer.innerHTML = `
        <h3>Upload Statistics</h3>
        <p>Total Files: ${data.total_files}</p>
        <p>Successful Uploads: ${data.successful_uploads}</p>
        <p>Failed Uploads: ${data.failed_uploads}</p>
        <h3>Recent Uploads</h3>
        <ul>
            ${data.recent_uploads.map(upload => `
                <li>${upload.filename} - ${upload.status} (${upload.timestamp})</li>
            `).join('')}
        </ul>
        ${data.recent_uploads.length > 0 ? `
            <h3>Latest Upload Status</h3>
            <p class="${data.recent_uploads[0].status.toLowerCase()}">${data.recent_uploads[0].status}: ${data.recent_uploads[0].filename}</p>
        ` : ''}
    `;
}
