const userNameElement = document.getElementById('userName');
const logoutBtn = document.getElementById('logoutBtn');
const refreshBtn = document.getElementById('refreshBtn');
const searchInput = document.getElementById('searchInput');
const jobContainer = document.getElementById('jobContainer');
const resultsContainer = document.getElementById('resultsContainer');
const jobCount = document.getElementById('jobCount');
const candidateCount = document.getElementById('candidateCount');
const refreshTime = document.getElementById('refreshTime');

function getStoredUser() {
    try {
        return JSON.parse(localStorage.getItem('flashaiUser'));
    } catch {
        return null;
    }
}

function logout() {
    localStorage.removeItem('flashaiUser');
    window.location.href = 'index.html';
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

async function fetchMatchData() {
    try {
        const response = await fetch('/api/match');
        if (!response.ok) {
            throw new Error(`Server responded with ${response.status}`);
        }
        return await response.json();
    } catch (err) {
        console.error(err);
        return null;
    }
}

function renderJobs(jobs, filter = '') {
    jobContainer.innerHTML = '';

    const normalizedFilter = filter.toLowerCase().trim();
    const filteredJobs = jobs.filter(job => {
        return (
            job.company.toLowerCase().includes(normalizedFilter) ||
            job.role.toLowerCase().includes(normalizedFilter) ||
            job.required_skills.some(skill => skill.toLowerCase().includes(normalizedFilter)) ||
            job.preferred_skills.some(skill => skill.toLowerCase().includes(normalizedFilter))
        );
    });

    if (filteredJobs.length === 0) {
        jobContainer.innerHTML = '<div class="empty-state">No roles matched your search.</div>';
        return;
    }

    filteredJobs.forEach(job => {
        const card = document.createElement('div');
        card.className = 'job-card';
        card.innerHTML = `
            <h3>${job.company} — ${job.role}</h3>
            <p><strong>Required Skills</strong></p>
            <div class="skills">${job.required_skills.map(skill => `<span class="skill">${skill}</span>`).join('')}</div>
            <p style="margin-top:15px;"><strong>Preferred Skills</strong></p>
            <div class="skills">${job.preferred_skills.map(skill => `<span class="skill">${skill}</span>`).join('')}</div>
        `;
        jobContainer.appendChild(card);
    });
}

function renderResults(results) {
    resultsContainer.innerHTML = '';

    if (results.length === 0) {
        resultsContainer.innerHTML = '<div class="empty-state">No candidate matches available yet.</div>';
        return;
    }

    results.forEach(result => {
        const block = document.createElement('div');
        block.className = 'result-block';

        let candidatesHTML = '';
        if (result.top_candidates.length === 0) {
            candidatesHTML = '<p>No candidates scored for this role.</p>';
        } else {
            result.top_candidates.forEach(candidate => {
                candidatesHTML += `
                    <div class="candidate-card">
                        <div class="candidate-top">
                            <h3>${candidate.name}</h3>
                            <div class="score">${candidate.score}%</div>
                        </div>
                        <div class="progress"><div class="progress-fill" style="width:${candidate.score}%;"></div></div>
                        <p><strong>Matched Skills</strong></p>
                        <div class="skills">${candidate.matched_skills.map(skill => `<span class="skill">${skill}</span>`).join('')}</div>
                    </div>
                `;
            });
        }

        block.innerHTML = `
            <h2 class="result-title">${result.jd_id} — ${result.company} (${result.role})</h2>
            ${candidatesHTML}
        `;

        resultsContainer.appendChild(block);
    });
}

async function loadDashboard() {
    const data = await fetchMatchData();
    if (!data) {
        jobContainer.innerHTML = '<div class="empty-state">Unable to load data. Please try again later.</div>';
        resultsContainer.innerHTML = '';
        return;
    }

    renderJobs(data.job_descriptions, searchInput.value);
    renderResults(data.results);

    jobCount.textContent = data.job_descriptions.length;
    candidateCount.textContent = data.results.reduce((sum, item) => sum + item.top_candidates.length, 0);
    refreshTime.textContent = formatTime(new Date());
}

function initialize() {
    const storedUser = getStoredUser();
    if (!storedUser || !storedUser.email) {
        window.location.href = 'index.html';
        return;
    }

    userNameElement.textContent = storedUser.name;
    logoutBtn.addEventListener('click', logout);
    refreshBtn.addEventListener('click', loadDashboard);
    searchInput.addEventListener('input', () => loadDashboard());

    loadDashboard();
}

initialize();
