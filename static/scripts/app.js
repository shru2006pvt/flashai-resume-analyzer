const analyzeForm = document.getElementById('analyze-form');
const analysisStatus = document.getElementById('analysis-status');
const compareForm = document.getElementById('compare-form');
const compareStatus = document.getElementById('compare-status');

if (analyzeForm) {
  analyzeForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    analysisStatus.textContent = 'Analyzing resume… Please wait.';
    analysisStatus.style.color = '#0f172a';

    const formData = new FormData(analyzeForm);
    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      });
      const payload = await response.json();

      if (!payload.success) {
        analysisStatus.textContent = payload.message || 'Analysis request failed.';
        analysisStatus.style.color = '#dc2626';
        return;
      }

      analysisStatus.textContent = 'Analysis completed. Redirecting to results…';
      analysisStatus.style.color = '#16a34a';
      window.location.href = payload.redirect;
    } catch (error) {
      analysisStatus.textContent = 'Unable to analyze resume. Please try again.';
      analysisStatus.style.color = '#dc2626';
      console.error(error);
    }
  });
}

if (compareForm) {
  compareForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    compareStatus.textContent = 'Comparing resumes… Please wait.';
    compareStatus.style.color = '#0f172a';

    const formData = new FormData(compareForm);
    try {
      const response = await fetch('/api/compare', {
        method: 'POST',
        body: formData,
      });
      const payload = await response.json();

      if (!payload.success) {
        compareStatus.textContent = payload.message || 'Comparison failed.';
        compareStatus.style.color = '#dc2626';
        return;
      }

      const results = payload.comparison.map((item, index) => `#${index + 1} ${item.candidate}: ${item.overall_score}% (${item.fit_level})`).join('\n');
      compareStatus.textContent = `Comparison complete. Top candidate: ${payload.comparison[0]?.candidate || 'N/A'}`;
      compareStatus.style.color = '#16a34a';
      console.log('Comparison results:', payload.comparison);
      alert(`Candidate ranking:\n\n${results}`);
    } catch (error) {
      compareStatus.textContent = 'Unable to compare resumes. Please try again.';
      compareStatus.style.color = '#dc2626';
      console.error(error);
    }
  });
}
