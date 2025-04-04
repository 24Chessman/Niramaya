// Modal functionality
const loginLink = document.getElementById('login-link');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const closeLogin = document.getElementById('close-login');
const closeRegister = document.getElementById('close-register');
const switchToRegister = document.getElementById('switch-to-register');
const switchToLogin = document.getElementById('switch-to-login');
const googleRegister = document.getElementById('google-register');

// Open login modal with animation
loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    loginModal.style.display = 'flex';
    loginModal.setAttribute('aria-hidden', 'false');
    setTimeout(() => loginModal.classList.add('show'), 10);
});

// Close login modal with animation
closeLogin.addEventListener('click', () => {
    loginModal.classList.remove('show');
    setTimeout(() => {
        loginModal.style.display = 'none';
        loginModal.setAttribute('aria-hidden', 'true');
    }, 300);
});

// Close register modal with animation
closeRegister.addEventListener('click', () => {
    registerModal.classList.remove('show');
    setTimeout(() => {
        registerModal.style.display = 'none';
        registerModal.setAttribute('aria-hidden', 'true');
    }, 300);
});

// Switch to register
switchToRegister.addEventListener('click', (e) => {
    e.preventDefault();
    loginModal.classList.remove('show');
    setTimeout(() => {
        loginModal.style.display = 'none';
        loginModal.setAttribute('aria-hidden', 'true');
        registerModal.style.display = 'flex';
        registerModal.setAttribute('aria-hidden', 'false');
        setTimeout(() => registerModal.classList.add('show'), 10);
    }, 300);
});

// Switch to login
switchToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    registerModal.classList.remove('show');
    setTimeout(() => {
        registerModal.style.display = 'none';
        registerModal.setAttribute('aria-hidden', 'true');
        loginModal.style.display = 'flex';
        loginModal.setAttribute('aria-hidden', 'false');
        setTimeout(() => loginModal.classList.add('show'), 10);
    }, 300);
});

// Google register (demo)
googleRegister.addEventListener('click', () => {
    console.log('Google registration clicked');
    registerModal.classList.remove('show');
    setTimeout(() => {
        registerModal.style.display = 'none';
        registerModal.setAttribute('aria-hidden', 'true');
    }, 300);
});

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.classList.remove('show');
        setTimeout(() => {
            loginModal.style.display = 'none';
            loginModal.setAttribute('aria-hidden', 'true');
        }, 300);
    }
    if (e.target === registerModal) {
        registerModal.classList.remove('show');
        setTimeout(() => {
            registerModal.style.display = 'none';
            registerModal.setAttribute('aria-hidden', 'true');
        }, 300);
    }
});

// Form submission
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    console.log('Login submitted:', { email, password });
    alert('Login successful!');
    loginModal.classList.remove('show');
    setTimeout(() => {
        loginModal.style.display = 'none';
        loginModal.setAttribute('aria-hidden', 'true');
    }, 300);
});

document.getElementById('register-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('register-name').value;
    const email = document.getElementById('register-email').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    console.log('Registration submitted:', { name, email, password });
    alert('Registration successful!');
    registerModal.classList.remove('show');
    setTimeout(() => {
        registerModal.style.display = 'none';
        registerModal.setAttribute('aria-hidden', 'true');
    }, 300);
});

// Fetch Research Papers
document.addEventListener("DOMContentLoaded", function () {
    fetchPubMedPapers();
});

async function fetchPubMedPapers() {
    const container = document.getElementById("research-papers");
    container.innerHTML = '<div class="loading"><span class="spinner"></span>Loading papers...</div>';

    try {
        const response = await fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=health&retmax=6&retmode=json");
        const data = await response.json();
        const ids = data.esearchresult.idlist;

        if (!ids || ids.length === 0) {
            container.innerHTML = '<p>No recent health papers found.</p>';
            return;
        }

        const detailsResponse = await fetch(`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id=${ids.join(",")}&retmode=json`);
        const detailsData = await detailsResponse.json();
        
        container.innerHTML = "";

        ids.forEach(id => {
            const paper = detailsData.result[id];
            if (paper) {
                const paperElement = document.createElement("div");
                paperElement.classList.add("paper-item");
                paperElement.innerHTML = `
                    <a href="https://pubmed.ncbi.nlm.nih.gov/${id}/" target="_blank" class="paper-image-link">
                        <img src="https://via.placeholder.com/150x100.png?text=Research+Paper" alt="${paper.title}" class="paper-image">
                    </a>
                    <div class="paper-content">
                        <a href="https://pubmed.ncbi.nlm.nih.gov/${id}/" target="_blank" class="paper-title-link">
                            <h3 class="paper-title">${paper.title}</h3>
                        </a>
                    </div>
                `;
                container.appendChild(paperElement);
            }
        });
    } catch (error) {
        container.innerHTML = '<p>Error loading papers. Please try again later.</p>';
        console.error("Error fetching PubMed papers:", error);
    }
}