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
async function fetchResearchPapers() {
    const container = document.getElementById("research-papers");
    container.innerHTML = '<div class="loading"><span class="spinner"></span>Loading papers...</div>';

    // Array of unique, verified health-related images from Pexels
    const imagePool = [
        "https://images.pexels.com/photos/305568/pexels-photo-305568.jpeg?auto=compress&cs=tinysrgb&w=320", // Stethoscope
        "https://images.pexels.com/photos/4021775/pexels-photo-4021775.jpeg?auto=compress&cs=tinysrgb&w=320", // Doctor with tablet
        "https://images.pexels.com/photos/3825586/pexels-photo-3825586.jpeg?auto=compress&cs=tinysrgb&w=320", // Lab research
        "https://images.pexels.com/photos/1640777/pexels-photo-1640777.jpeg?auto=compress&cs=tinysrgb&w=320", // Healthy food
        "https://images.pexels.com/photos/2280547/pexels-photo-2280547.jpeg?auto=compress&cs=tinysrgb&w=320", // Brain model
        "https://images.pexels.com/photos/7659564/pexels-photo-7659564.jpeg?auto=compress&cs=tinysrgb&w=320"  // AI health tech
    ];

    try {
        const response = await fetch("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=health%20AI%20wellness&resultType=lite&format=json");
        const data = await response.json();
        const papers = data.resultList.result.slice(0, 6);

        if (!papers || papers.length === 0) {
            container.innerHTML = '<p>No recent health papers found.</p>';
            return;
        }

        container.innerHTML = "";

        papers.forEach((paper, index) => {
            const title = paper.title || "Untitled";
            const authors = paper.authorString || "Unknown Authors";
            const pmcId = paper.pmcid || paper.id;
            const imageUrl = imagePool[index % imagePool.length];

            const paperElement = document.createElement("div");
            paperElement.classList.add("paper-card");
            paperElement.innerHTML = `
                <a href="https://europepmc.org/article/MED/${paper.id}" target="_blank" class="paper-link">
                    <div class="paper-image-wrapper">
                        <img src="${imageUrl}" alt="${title}" class="paper-image" 
                             onerror="this.onerror=null; this.src='https://via.placeholder.com/320x120?text=Image+Not+Found';">
                        <div class="paper-overlay">
                            <span class="read-more">Read More</span>
                        </div>
                    </div>
                    <div class="paper-details">
                        <h3 class="paper-title">${title}</h3>
                        <p class="paper-authors">${authors}</p>
                    </div>
                </a>
            `;
            container.appendChild(paperElement);
        });
    } catch (error) {
        container.innerHTML = '<p>Error loading papers. Please try again later.</p>';
        console.error("Error fetching research papers:", error);
    }
}

document.addEventListener("DOMContentLoaded", function () {
    fetchResearchPapers();
});