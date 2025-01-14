function displayRecommendations(recommendations) {
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '';

    // Criar seção de recomendações AI
    const aiSection = document.createElement('div');
    aiSection.className = 'recommendations-section mb-4';
    aiSection.innerHTML = `
        <h3 class="mb-3">Recomendações Personalizadas</h3>
        <div class="ai-recommendations">
            ${recommendations.ai_recommendations.split('\n').map(line => 
                `<p>${line.trim()}</p>`
            ).join('')}
        </div>
    `;
    recommendationsDiv.appendChild(aiSection);

    // Criar seção de cursos do Coursera
    const courseraSection = document.createElement('div');
    courseraSection.className = 'recommendations-section';
    courseraSection.innerHTML = `
        <h3 class="mb-3">Cursos do Coursera</h3>
        <div class="row">
            ${recommendations.coursera_courses.map(course => `
                <div class="col-md-4 mb-3">
                    <div class="card h-100 d-flex flex-column">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${course.name}</h5>
                            <div class="mt-auto">
                                <a href="${course.link}" target="_blank" class="btn btn-primary">Ver Curso</a>
                            </div>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
    recommendationsDiv.appendChild(courseraSection);

    // Mostrar a seção de recomendações
    recommendationsDiv.style.display = 'block';
    recommendationsDiv.scrollIntoView({ behavior: 'smooth' });
}
