const analyzeBtn =
    document.getElementById("analyzeBtn");

const jobContainer =
    document.getElementById("jobContainer");

const resultsContainer =
    document.getElementById("resultsContainer");


/* ================================= */
/* FETCH RESULTS FROM PYTHON BACKEND */
/* ================================= */

async function loadResults() {

    try {

        const response =
            await fetch(
                "http://localhost:8000/api/match"
            );

        const data = await response.json();

        renderJobs(
            data.job_descriptions
        );

        renderResults(
            data.results
        );

    } catch (error) {

        console.log(error);
    }
}


/* ================================= */
/* RENDER JOB DESCRIPTIONS */
/* ================================= */

function renderJobs(jobs) {

    jobContainer.innerHTML = "";

    jobs.forEach(job => {

        const card =
            document.createElement("div");

        card.className = "job-card";

        card.innerHTML = `

            <h3>
                ${job.company} —
                ${job.role}
            </h3>

            <p>
                <strong>
                    Required Skills
                </strong>
            </p>

            <div class="skills">

                ${job.required_skills.map(skill =>

                    `<span class="skill">
                        ${skill}
                    </span>`

                ).join("")}

            </div>

            <p style="margin-top:15px;">
                <strong>
                    Preferred Skills
                </strong>
            </p>

            <div class="skills">

                ${job.preferred_skills.map(skill =>

                    `<span class="skill">
                        ${skill}
                    </span>`

                ).join("")}

            </div>
        `;

        jobContainer.appendChild(card);
    });
}


/* ================================= */
/* RENDER MATCH RESULTS */
/* ================================= */

function renderResults(results) {

    resultsContainer.innerHTML = "";

    results.forEach(result => {

        const block =
            document.createElement("div");

        block.className = "result-block";

        let candidatesHTML = "";

        result.top_candidates.forEach(candidate => {

            candidatesHTML += `

                <div class="candidate-card">

                    <div class="candidate-top">

                        <h3>
                            ${candidate.name}
                        </h3>

                        <div class="score">
                            ${candidate.score}%
                        </div>

                    </div>

                    <div class="progress">

                        <div
                            class="progress-fill"
                            style="
                                width:
                                ${candidate.score}%;
                            "
                        ></div>

                    </div>

                    <p>
                        <strong>
                            Matched Skills
                        </strong>
                    </p>

                    <div class="skills">

                        ${candidate.matched_skills.map(skill =>

                            `<span class="skill">
                                ${skill}
                            </span>`

                        ).join("")}

                    </div>

                </div>
            `;
        });

        block.innerHTML = `

            <h2 class="result-title">

                ${result.jd_id}
                —
                ${result.company}
                (${result.role})

            </h2>

            ${candidatesHTML}
        `;

        resultsContainer.appendChild(block);
    });
}


/* ================================= */
/* BUTTON EVENT */
/* ================================= */

analyzeBtn.addEventListener(
    "click",
    loadResults
);