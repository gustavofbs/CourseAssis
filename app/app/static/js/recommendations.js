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

function formatDateBR(dateStr) {
    if (!dateStr) return '';
    const [year, month, day] = dateStr.split('-');
    return `${day}/${month}/${year}`;
}

async function generateStudyPlan(courseName, courseDescription) {
    // Criar modal para coletar informações do plano de estudos
    const planModalHtml = `
        <div class="modal fade" id="studyPlanModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Criar Plano de Estudos - ${courseName}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="studyPlanForm">
                            <div class="mb-3">
                                <label for="weeklyHours" class="form-label">Horas disponíveis por semana:</label>
                                <input type="number" class="form-control" id="weeklyHours" min="1" max="40" value="10" required>
                            </div>
                            <div class="mb-3">
                                <label for="startDate" class="form-label">Data de início:</label>
                                <input type="date" class="form-control" id="startDate" required>
                            </div>
                            <div class="mb-3">
                                <label for="endDate" class="form-label">Data de término:</label>
                                <input type="date" class="form-control" id="endDate" required>
                            </div>
                            
                            <hr>
                            <h6 class="mb-3">Distribuição do Tempo (%)</h6>
                            
                            <div class="mb-3">
                                <label for="fundamentalsSlider" class="form-label d-flex justify-content-between">
                                    <span>Fundamentos:</span>
                                    <span id="fundamentalsValue">30%</span>
                                </label>
                                <input type="range" class="form-range" id="fundamentalsSlider" min="10" max="60" value="30">
                            </div>
                            
                            <div class="mb-3">
                                <label for="developmentSlider" class="form-label d-flex justify-content-between">
                                    <span>Desenvolvimento:</span>
                                    <span id="developmentValue">40%</span>
                                </label>
                                <input type="range" class="form-range" id="developmentSlider" min="20" max="60" value="40">
                            </div>
                            
                            <div class="mb-3">
                                <label for="projectSlider" class="form-label d-flex justify-content-between">
                                    <span>Projeto Final:</span>
                                    <span id="projectValue">30%</span>
                                </label>
                                <input type="range" class="form-range" id="projectSlider" min="10" max="40" value="30">
                            </div>
                            
                            <div class="alert alert-danger d-none" id="sliderAlert">
                                O total deve ser 100%. Ajuste os valores.
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        <button type="button" class="btn btn-primary" id="generatePlan">Gerar Plano</button>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remover modal anterior se existir
    const oldPlanModal = document.getElementById('studyPlanModal');
    if (oldPlanModal) {
        oldPlanModal.remove();
    }

    // Adicionar novo modal ao documento
    document.body.insertAdjacentHTML('beforeend', planModalHtml);

    // Configurar datas mínimas como hoje
    const today = new Date().toISOString().split('T')[0];
    const startDateInput = document.getElementById('startDate');
    const endDateInput = document.getElementById('endDate');
    
    startDateInput.min = today;
    startDateInput.value = today;
    
    // Configurar data mínima de término como a data de início
    startDateInput.addEventListener('change', () => {
        endDateInput.min = startDateInput.value;
        if (endDateInput.value && endDateInput.value < startDateInput.value) {
            endDateInput.value = startDateInput.value;
        }
    });
    
    // Definir data de término padrão como 3 meses após a data de início
    const defaultEndDate = new Date();
    defaultEndDate.setMonth(defaultEndDate.getMonth() + 3);
    endDateInput.value = defaultEndDate.toISOString().split('T')[0];
    endDateInput.min = today;

    // Configurar os sliders
    const fundamentalsSlider = document.getElementById('fundamentalsSlider');
    const developmentSlider = document.getElementById('developmentSlider');
    const projectSlider = document.getElementById('projectSlider');
    const sliderAlert = document.getElementById('sliderAlert');

    function updateSliderValues() {
        document.getElementById('fundamentalsValue').textContent = fundamentalsSlider.value + '%';
        document.getElementById('developmentValue').textContent = developmentSlider.value + '%';
        document.getElementById('projectValue').textContent = projectSlider.value + '%';
        
        const total = parseInt(fundamentalsSlider.value) + 
                     parseInt(developmentSlider.value) + 
                     parseInt(projectSlider.value);
                     
        if (total !== 100) {
            sliderAlert.textContent = `Total atual: ${total}%. Ajuste para 100%.`;
            sliderAlert.classList.remove('d-none');
        } else {
            sliderAlert.classList.add('d-none');
        }
    }

    fundamentalsSlider.addEventListener('input', updateSliderValues);
    developmentSlider.addEventListener('input', updateSliderValues);
    projectSlider.addEventListener('input', updateSliderValues);

    // Mostrar o modal
    const planModal = new bootstrap.Modal(document.getElementById('studyPlanModal'));
    planModal.show();

    // Adicionar evento ao botão de gerar plano
    document.getElementById('generatePlan').addEventListener('click', async () => {
        const weeklyHours = document.getElementById('weeklyHours').value;
        const startDate = document.getElementById('startDate').value;
        const endDate = document.getElementById('endDate').value;
        
        const total = parseInt(fundamentalsSlider.value) + 
                     parseInt(developmentSlider.value) + 
                     parseInt(projectSlider.value);

        if (!weeklyHours || !startDate || !endDate) {
            alert('Por favor, preencha todos os campos.');
            return;
        }

        if (new Date(endDate) <= new Date(startDate)) {
            alert('A data de término deve ser posterior à data de início.');
            return;
        }
        
        if (total !== 100) {
            alert('A distribuição do tempo deve somar 100%.');
            return;
        }

        // Fechar modal de entrada
        planModal.hide();

        const formData = new FormData();
        formData.append('course_name', courseName);
        formData.append('course_description', courseDescription);
        formData.append('weekly_hours', weeklyHours);
        formData.append('start_date', startDate);
        formData.append('end_date', endDate);
        formData.append('fundamentals_percent', fundamentalsSlider.value);
        formData.append('development_percent', developmentSlider.value);
        formData.append('project_percent', projectSlider.value);

        try {
            const response = await fetch('/generate_study_plan', {
                method: 'POST',
                body: formData
            });
            const studyPlan = await response.json();
            
            // Criar e mostrar modal com o plano de estudos
            const planResultModalHtml = `
                <div class="modal fade" id="studyPlanResultModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Seu Plano de Estudos - ${courseName}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="study-plan-details">
                                    <h6>Informações Gerais:</h6>
                                    <ul>
                                        <li>Data de Início: ${studyPlan.start_date}</li>
                                        <li>Data de Término: ${studyPlan.end_date}</li>
                                        <li>Horas por Semana: ${studyPlan.weekly_hours}</li>
                                    </ul>
                                    
                                    <h6 class="mt-4">Cronograma:</h6>
                                    ${studyPlan.schedule.map(module => `
                                        <div class="card mb-3">
                                            <div class="card-header">
                                                <strong>${module.module_name}</strong>
                                                <br>
                                                <small>
                                                    ${module.start_date} até ${module.end_date}
                                                </small>
                                            </div>
                                            <div class="card-body">
                                                <h6>Atividades Semanais (${Math.round(module.weekly_activities.reduce((sum, activity) => sum + activity.hours, 0))}h/semana):</h6>
                                                <ul class="list-unstyled">
                                                    ${module.weekly_activities.map(activity => `
                                                        <li class="mb-2">
                                                            <strong>${activity.topic}</strong> (${activity.hours}h/semana)
                                                            <br>
                                                            <small>Recursos: ${activity.resources.join(', ')}</small>
                                                        </li>
                                                    `).join('')}
                                                </ul>
                                            </div>
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Fechar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior se existir
            const oldResultModal = document.getElementById('studyPlanResultModal');
            if (oldResultModal) {
                oldResultModal.remove();
            }
            
            // Adicionar novo modal ao documento
            document.body.insertAdjacentHTML('beforeend', planResultModalHtml);
            
            // Mostrar o modal
            const resultModal = new bootstrap.Modal(document.getElementById('studyPlanResultModal'));
            resultModal.show();
        } catch (error) {
            console.error('Erro ao gerar plano de estudos:', error);
            alert('Erro ao gerar plano de estudos. Por favor, tente novamente.');
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
                                    <button class="btn btn-outline-success" onclick='generateStudyPlan(${JSON.stringify(course.name)}, ${JSON.stringify(course.description)})'>
                                        Criar Plano de Estudos
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
