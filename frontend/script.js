// Modal functionality
const loginLink = document.getElementById('login-link');
const loginModal = document.getElementById('login-modal');
const registerModal = document.getElementById('register-modal');
const closeLogin = document.getElementById('close-login');
const closeRegister = document.getElementById('close-register');
const switchToRegister = document.getElementById('switch-to-register');
const switchToLogin = document.getElementById('switch-to-login');
const googleRegister = document.getElementById('google-register');

// Open login modal
loginLink.addEventListener('click', (e) => {
    e.preventDefault();
    loginModal.style.display = 'flex';
});

// Close login modal
closeLogin.addEventListener('click', () => {
    loginModal.style.display = 'none';
});

// Close register modal
closeRegister.addEventListener('click', () => {
    registerModal.style.display = 'none';
});

// Switch to register
switchToRegister.addEventListener('click', (e) => {
    e.preventDefault();
    loginModal.style.display = 'none';
    registerModal.style.display = 'flex';
});

// Switch to login
switchToLogin.addEventListener('click', (e) => {
    e.preventDefault();
    registerModal.style.display = 'none';
    loginModal.style.display = 'flex';
});

// Google register (demo)
googleRegister.addEventListener('click', () => {
    console.log('Google registration clicked');
    // Add actual Google OAuth logic here
    registerModal.style.display = 'none';
});

// Close modals when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === loginModal) {
        loginModal.style.display = 'none';
    } else if (e.target === registerModal) {
        registerModal.style.display = 'none';
    }
});

// Form submission
document.getElementById('login-form').addEventListener('submit', (e) => {
    e.preventDefault();
    console.log('Login submitted');
    loginModal.style.display = 'none';
});

document.getElementById('register-form').addEventListener('submit', (e) => {
    e.preventDefault();
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-confirm-password').value;
    if (password !== confirmPassword) {
        alert('Passwords do not match!');
        return;
    }
    console.log('Registration submitted');
    registerModal.style.display = 'none';
});

// Fetch Research Papers
document.addEventListener("DOMContentLoaded", function () {
    fetchPubMedPapers();
});

async function fetchPubMedPapers() {
    const container = document.getElementById("research-papers");
    container.innerHTML = "Loading papers...";

    try {
        const response = await fetch("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=health&retmax=6&retmode=json");
        const data = await response.json();
        const ids = data.esearchresult.idlist;

        if (ids.length === 0) {
            container.innerHTML = "No papers found.";
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
                    <h3 class="paper-title">${paper.title}</h3>
                    <a href="https://pubmed.ncbi.nlm.nih.gov/${id}/" class="paper-link" target="_blank">Read More</a>
                `;
                
                container.appendChild(paperElement);
            }
        });
    } catch (error) {
        container.innerHTML = "Error loading papers.";
        console.error("Error fetching PubMed papers:", error);
    }
}