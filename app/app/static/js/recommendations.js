async function askQuestion(courseName, courseDescription) {
    // Criar modal para fazer a pergunta
    const questionModalHtml = `
        <div class="modal fade" id="questionModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Pergunta sobre ${courseName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label for="questionInput" class="form-label">Sua pergunta sobre o curso:</label>
                            <textarea class="form-control" id="questionInput" rows="3" placeholder="Digite sua pergunta aqui..."></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="submitQuestion">Enviar Pergunta</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remover modal anterior se existir
    const oldQuestionModal = document.getElementById('questionModal');
    if (oldQuestionModal) {
        oldQuestionModal.remove();
    }

    // Adicionar novo modal ao documento
    document.body.insertAdjacentHTML('beforeend', questionModalHtml);

    // Mostrar o modal de pergunta
    const questionModal = new bootstrap.Modal(document.getElementById('questionModal'));
    questionModal.show();

    // Adicionar evento ao botão de enviar
    document.getElementById('submitQuestion').addEventListener('click', async () => {
        const question = document.getElementById('questionInput').value.trim();
        if (!question) return;

        // Fechar modal de pergunta
        questionModal.hide();

        const formData = new FormData();
        formData.append('question', question);
        formData.append('course_name', courseName);
        formData.append('course_description', courseDescription);

        try {
            const response = await fetch('/ask_question', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            // Criar e mostrar modal com a resposta
            const answerModalHtml = `
                <div class="modal fade" id="answerModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Resposta sobre ${courseName}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <p><strong>Sua pergunta:</strong> ${question}</p>
                                <hr>
                                <p><strong>Resposta:</strong></p>
                                <p>${data.answer}</p>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Fechar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior se existir
            const oldAnswerModal = document.getElementById('answerModal');
            if (oldAnswerModal) {
                oldAnswerModal.remove();
            }
            
            // Adicionar novo modal ao documento
            document.body.insertAdjacentHTML('beforeend', answerModalHtml);
            
            // Mostrar o modal
            const answerModal = new bootstrap.Modal(document.getElementById('answerModal'));
            answerModal.show();
        } catch (error) {
            console.error('Erro ao fazer pergunta:', error);
            alert('Erro ao processar sua pergunta. Por favor, tente novamente.');
        }
    });
}

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
                    <div class="card h-100">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title">${course.name}</h5>
                            <div class="mt-auto">
                                <div class="d-grid gap-2">
                                    <a href="${course.link}" target="_blank" class="btn btn-primary">Ver Curso</a>
                                    <button class="btn btn-outline-primary" onclick='askQuestion(${JSON.stringify(course.name)}, ${JSON.stringify(course.description)})'>
                                        Fazer Pergunta
                                    </button>
                                </div>
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
