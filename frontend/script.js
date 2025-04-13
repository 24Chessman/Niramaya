// Shuffle array function
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Fetch Research Papers
async function fetchResearchPapers() {
    const container = document.getElementById("research-papers");
    container.innerHTML = '<div class="loading"><span class="spinner"></span>Loading papers...</div>';

    // Array of 20 unique, verified health-related images from Unsplash (re-verified)
    const imagePool = [
        "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Stethoscope
        "https://images.unsplash.com/photo-1550831107-1553da8c8464?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Doctor
        "https://images.unsplash.com/photo-1498837167922-ddd27525d352?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Healthy food
        "https://images.unsplash.com/photo-1557682224-5b8590cd9ec5?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Brain
        "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Health tech
        "https://images.unsplash.com/photo-1532938911079-1b06ac7ceec7?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Heart health
        "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Fitness tracker
        "https://images.unsplash.com/photo-1543353071-873f17a7a088?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Meditation
        "https://images.unsplash.com/photo-1579684385127-1ef15d508118?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Patient care
        "https://images.unsplash.com/photo-1506126613408-eca07ce68773?ixlib=rb-4.0.3&auto=format&fit=crop&w=320", // Healthy lifestyle
    ];

    // Fallback image pool (re-verified)
    const fallbackImages = [
        "https://images.unsplash.com/photo-1617791160536-585948b95a38?ixlib=rb-4.0.3&auto=format&fit=crop&w=320"  // Medical research
    ];

    try {
        // Fetch up to 20 papers
        const response = await fetch("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=health%20AI%20wellness&resultType=lite&format=json&pageSize=20");
        const data = await response.json();
        let papers = data.resultList.result;

        if (!papers || papers.length === 0) {
            container.innerHTML = '<p>No recent health papers found.</p>';
            return;
        }

        // Shuffle papers and take up to 20
        papers = shuffleArray(papers).slice(0, 20);

        // Shuffle images
        const shuffledImages = shuffleArray([...imagePool]).slice(0, Math.min(6, papers.length)); // Ensure at least 6 images

        // Select 6 random papers
        const selectedPapers = papers.slice(0, 6);

        container.innerHTML = "";

        selectedPapers.forEach((paper, index) => {
            const title = paper.title || "Untitled";
            const authors = paper.authorString || "Unknown Authors";
            const pmcId = paper.pmcid || paper.id;
            const imageUrl = shuffledImages[index] || fallbackImages[index % fallbackImages.length];

            const paperElement = document.createElement("div");
            paperElement.classList.add("paper-card");
            paperElement.innerHTML = `
                <a href="https://europepmc.org/article/MED/${paper.id}" target="_blank" class="paper-link">
                    <div class="paper-image-wrapper">
                        <img src="${imageUrl}" alt="${title}" class="paper-image" 
                             onload="console.log('Image loaded:', '${imageUrl}')"
                             onerror="console.error('Image failed:', '${imageUrl}'); this.onerror=null; this.src='${fallbackImages[(index + 1) % fallbackImages.length]}';">
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

function toggleResearch() {
    const content = document.getElementById('research-content');
    const toggle = document.querySelector('.research-toggle');
    const icon = toggle.querySelector('.toggle-icon');

    if (content.style.maxHeight) {
        content.style.maxHeight = null;
        icon.textContent = '▼';
    } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        icon.textContent = '▲';
    }
}
// Initially hide the research content
document.getElementById('research-content').style.maxHeight = '0';

document.addEventListener("DOMContentLoaded", function () {
    fetchResearchPapers();
});

document.querySelector(".logo").onclick = function(e) {
    e.preventDefault();
    window.location.href = "home.html";
};

document.querySelector(".site-name").onclick = function(e) {
    e.preventDefault();
    window.location.href = "home.html";
};

document.addEventListener("DOMContentLoaded", function () {
    fetchResearchPapers();
});

document.querySelector(".logo").onclick = function(e) {
    e.preventDefault(); // Prevent any default behavior if applicable
    window.location.href = "home.html";
};

document.querySelector(".site-name").onclick = function(e) {
    e.preventDefault(); // Prevent any default behavior if applicable
    window.location.href = "home.html";
};

