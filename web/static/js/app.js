// ========================================
// SISTEMA DE MEDIDAS CORPORAIS - JAVASCRIPT
// ========================================

// Estado da aplicação
const app = {
    usuario: null,
    avaliacoes: []
};

// ========================================
// INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    await carregarUsuario();
    await carregarAvaliacoes();
    inicializarEventos();
    inicializarMapaInterativo();
    aplicarTema();
});

// ========================================
// GERENCIAMENTO DE USUÁRIO
// ========================================

async function carregarUsuario() {
    try {
        const response = await fetch('/api/usuario');
        if (response.ok) {
            app.usuario = await response.json();
            if (app.usuario) {
                preencherFormularioUsuario();
            } else {
                mostrarModal();
            }
        }
    } catch (error) {
        console.error('Erro ao carregar usuário:', error);
        mostrarToast('Erro ao carregar dados do usuário', 'error');
    }
}

async function salvarUsuario(dados) {
    try {
        const response = await fetch('/api/usuario', {
            method: app.usuario ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });

        if (response.ok) {
            app.usuario = await response.json();
            aplicarTema();
            mostrarToast('Configurações salvas com sucesso!', 'success');
            esconderModal();
            return true;
        } else {
            const erro = await response.json();
            mostrarToast(erro.erro || 'Erro ao salvar', 'error');
            return false;
        }
    } catch (error) {
        console.error('Erro ao salvar usuário:', error);
        mostrarToast('Erro ao salvar configurações', 'error');
        return false;
    }
}

function preencherFormularioUsuario() {
    if (!app.usuario) return;

    document.getElementById('userName').value = app.usuario.nome || '';
    document.getElementById('userBirthdate').value = app.usuario.data_nascimento || '';
    document.getElementById('userAge').value = app.usuario.idade ? `${app.usuario.idade} anos` : '';
    document.getElementById('userSex').value = app.usuario.sexo || '';
    document.getElementById('userEmail').value = app.usuario.email || '';
    document.getElementById('userHeight').value = app.usuario.altura || '';
}

function calcularIdade(dataNascimento) {
    const hoje = new Date();
    const nascimento = new Date(dataNascimento);
    let idade = hoje.getFullYear() - nascimento.getFullYear();
    const mes = hoje.getMonth() - nascimento.getMonth();
    
    if (mes < 0 || (mes === 0 && hoje.getDate() < nascimento.getDate())) {
        idade--;
    }
    
    return idade;
}

// ========================================
// GERENCIAMENTO DE AVALIAÇÕES
// ========================================

async function carregarAvaliacoes() {
    try {
        const response = await fetch('/api/avaliacoes');
        if (response.ok) {
            app.avaliacoes = await response.json();
            renderizarAvaliacoes();
        }
    } catch (error) {
        console.error('Erro ao carregar avaliações:', error);
        mostrarToast('Erro ao carregar avaliações', 'error');
    }
}

async function salvarAvaliacao() {
    // Verificar se usuário está cadastrado
    if (!app.usuario) {
        mostrarToast('Configure seu perfil antes de criar uma avaliação', 'warning');
        mostrarModal();
        return;
    }

    // Coletar dados do formulário
    const medidas = {
        altura: app.usuario.altura,
        peso: parseFloat(document.getElementById('peso').value),
        pescoco: parseFloat(document.getElementById('pescoco').value) || null,
        ombros: parseFloat(document.getElementById('ombros').value) || null,
        peitoral: parseFloat(document.getElementById('peitoral').value) || null,
        cintura: parseFloat(document.getElementById('cintura').value) || null,
        abdomen: parseFloat(document.getElementById('abdomen').value) || null,
        quadril: parseFloat(document.getElementById('quadril').value) || null,
        braco_relaxado: parseFloat(document.getElementById('braco_relaxado').value) || null,
        braco_contraido: parseFloat(document.getElementById('braco_contraido').value) || null,
        antebraco: parseFloat(document.getElementById('antebraco').value) || null,
        coxa: parseFloat(document.getElementById('coxa').value) || null,
        panturrilha: parseFloat(document.getElementById('panturrilha').value) || null
    };

    // Validar campos obrigatórios
    if (!medidas.peso) {
        mostrarToast('Peso é obrigatório', 'warning');
        return;
    }

    if (!medidas.cintura) {
        mostrarToast('Cintura é obrigatória', 'warning');
        return;
    }

    if (!medidas.quadril) {
        mostrarToast('Quadril é obrigatório', 'warning');
        return;
    }

    const objetivo = document.getElementById('objetivo').value;

    try {
        mostrarToast('Processando avaliação...', 'info');
        
        const response = await fetch('/api/avaliacoes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                medidas: medidas,
                objetivo: objetivo
            })
        });

        if (response.ok) {
            const avaliacao = await response.json();
            app.avaliacoes.unshift(avaliacao);
            renderizarAvaliacoes();
            limparFormulario();
            mostrarToast('Avaliação salva com sucesso!', 'success');
        } else {
            const erro = await response.json();
            mostrarToast(erro.erro || 'Erro ao salvar avaliação', 'error');
        }
    } catch (error) {
        console.error('Erro ao salvar avaliação:', error);
        mostrarToast('Erro ao salvar avaliação', 'error');
    }
}

async function deletarAvaliacao(id) {
    if (!confirm('Tem certeza que deseja deletar esta avaliação?')) {
        return;
    }

    try {
        const response = await fetch(`/api/avaliacoes/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            app.avaliacoes = app.avaliacoes.filter(a => a.id !== id);
            renderizarAvaliacoes();
            mostrarToast('Avaliação deletada', 'success');
        }
    } catch (error) {
        console.error('Erro ao deletar avaliação:', error);
        mostrarToast('Erro ao deletar avaliação', 'error');
    }
}

function renderizarAvaliacoes() {
    const container = document.getElementById('avaliacoesContainer');
    
    if (app.avaliacoes.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="9" y1="9" x2="15" y2="9"></line>
                    <line x1="9" y1="15" x2="15" y2="15"></line>
                </svg>
                <h3>Nenhuma avaliação ainda</h3>
                <p>Faça a sua primeira avaliação preenchendo os dados ao lado</p>
            </div>
        `;
        return;
    }

    container.innerHTML = app.avaliacoes.map(av => criarCardAvaliacao(av)).join('');
}

function criarCardAvaliacao(avaliacao) {
    const data = new Date(avaliacao.data).toLocaleDateString('pt-BR');
    const resultados = avaliacao.resultados;
    
    return `
        <div class="avaliacao-card">
            <div class="avaliacao-header">
                <span class="avaliacao-date">📅 ${data}</span>
                <div class="avaliacao-actions">
                    <button class="btn-icon" onclick="deletarAvaliacao('${avaliacao.id}')" title="Deletar">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="3 6 5 6 21 6"></polyline>
                            <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                        </svg>
                    </button>
                </div>
            </div>
            
            <div class="avaliacao-content">
                <div class="result-item">
                    <span class="result-label">Peso</span>
                    <span class="result-value">${avaliacao.medidas.peso} kg</span>
                </div>
                
                ${resultados.imc ? `
                <div class="result-item">
                    <span class="result-label">IMC</span>
                    <span class="result-value">${resultados.imc}</span>
                    <span class="result-desc">${resultados.imc_descricao}</span>
                </div>
                ` : ''}
                
                ${resultados.percentual_gordura ? `
                <div class="result-item">
                    <span class="result-label">% Gordura</span>
                    <span class="result-value">${resultados.percentual_gordura}%</span>
                    <span class="result-desc">${resultados.classificacao_gordura}</span>
                </div>
                ` : ''}
                
                ${resultados.massa_magra_kg ? `
                <div class="result-item">
                    <span class="result-label">Massa Magra</span>
                    <span class="result-value">${resultados.massa_magra_kg} kg</span>
                </div>
                ` : ''}
                
                ${resultados.rcq ? `
                <div class="result-item">
                    <span class="result-label">RCQ</span>
                    <span class="result-value">${resultados.rcq}</span>
                    <span class="result-desc">${resultados.rcq_descricao}</span>
                </div>
                ` : ''}
                
                ${resultados.rca ? `
                <div class="result-item">
                    <span class="result-label">RCA</span>
                    <span class="result-value">${resultados.rca}</span>
                    <span class="result-desc">${resultados.rca_descricao}</span>
                </div>
                ` : ''}
                
                ${resultados.somatotipo ? `
                <div class="result-item">
                    <span class="result-label">Somatotipo</span>
                    <span class="badge badge-info">${resultados.somatotipo}</span>
                </div>
                ` : ''}
                
                ${resultados.pontuacao_estetica ? `
                <div class="result-item">
                    <span class="result-label">Pontuação Estética</span>
                    <span class="result-value">${resultados.pontuacao_estetica}/100</span>
                    <span class="result-desc">${resultados.classificacao_estetica}</span>
                </div>
                ` : ''}
            </div>
            
            ${resultados.analise_simetria && Object.keys(resultados.analise_simetria).length > 0 ? `
                <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid var(--border-color);">
                    <span class="result-label">Análise de Simetria:</span>
                    ${Object.entries(resultados.analise_simetria).map(([key, value]) => `
                        <div style="font-size: 0.85rem; margin-top: 0.5rem; color: var(--text-secondary);">
                            <strong>${key.replace('_', ' ')}:</strong> ${value}
                        </div>
                    `).join('')}
                </div>
            ` : ''}
        </div>
    `;
}

function limparFormulario() {
    document.getElementById('peso').value = '';
    document.getElementById('pescoco').value = '';
    document.getElementById('ombros').value = '';
    document.getElementById('peitoral').value = '';
    document.getElementById('cintura').value = '';
    document.getElementById('abdomen').value = '';
    document.getElementById('quadril').value = '';
    document.getElementById('braco_relaxado').value = '';
    document.getElementById('braco_contraido').value = '';
    document.getElementById('antebraco').value = '';
    document.getElementById('coxa').value = '';
    document.getElementById('panturrilha').value = '';
    document.getElementById('objetivo').value = '';
}

// ========================================
// GERENCIAMENTO DE TEMA
// ========================================

function aplicarTema() {
    const tema = localStorage.getItem('tema') || app.usuario?.tema || 'dark';
    document.body.className = `${tema}-theme`;
    
    // Atualizar estado do switch
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.checked = tema === 'light';
    }
}

function alternarTema() {
    const temaAtual = document.body.classList.contains('dark-theme') ? 'dark' : 'light';
    const novoTema = temaAtual === 'light' ? 'dark' : 'light';
    
    document.body.className = `${novoTema}-theme`;
    
    // Salvar tema no localStorage
    localStorage.setItem('tema', novoTema);
}

// ========================================
// MODAL
// ========================================

function mostrarModal() {
    document.getElementById('userModal').classList.add('active');
}

function esconderModal() {
    document.getElementById('userModal').classList.remove('active');
}

// ========================================
// TOAST NOTIFICATIONS
// ========================================

function mostrarToast(mensagem, tipo = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${tipo}`;
    
    const icon = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ'
    }[tipo] || 'ℹ';
    
    toast.innerHTML = `
        <span style="font-size: 1.5rem;">${icon}</span>
        <span>${mensagem}</span>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ========================================
// EVENT LISTENERS
// ========================================

function inicializarEventos() {
    // Botão de usuário
    document.getElementById('userBtn').addEventListener('click', mostrarModal);
    
    // Theme toggle switch
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', alternarTema);
    }
    
    // Fechar modal
    document.getElementById('closeModal').addEventListener('click', esconderModal);
    
    // Clique fora do modal
    document.getElementById('userModal').addEventListener('click', (e) => {
        if (e.target.id === 'userModal') {
            esconderModal();
        }
    });
    
    // Formulário de usuário
    document.getElementById('userForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const dados = {
            nome: document.getElementById('userName').value,
            data_nascimento: document.getElementById('userBirthdate').value,
            sexo: document.getElementById('userSex').value,
            email: document.getElementById('userEmail').value,
            altura: parseFloat(document.getElementById('userHeight').value)
        };
        
        await salvarUsuario(dados);
    });
    
    // Calcular idade automaticamente
    document.getElementById('userBirthdate').addEventListener('change', (e) => {
        if (e.target.value) {
            const idade = calcularIdade(e.target.value);
            document.getElementById('userAge').value = `${idade} anos`;
        }
    });
    
    // Alteração de tema
    document.getElementById('userTheme').addEventListener('change', (e) => {
        document.body.className = `${e.target.value}-theme`;
    });
    
    // Botão de salvar avaliação
    document.getElementById('saveBtn').addEventListener('click', salvarAvaliacao);
    
    // Interação com pontos do mapa anatômico
    document.querySelectorAll('.measure-point').forEach(point => {
        point.addEventListener('click', function() {
            const fieldId = this.dataset.field;
            const input = document.getElementById(fieldId);
            if (input) {
                input.focus();
                input.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
    });
}

// ========================================
// ANIMAÇÕES E EFEITOS
// ========================================

// Animação de slide out para toast
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);

// ========================================
// MAPA INTERATIVO - HOVER HIGHLIGHTS
// ========================================

function inicializarMapaInterativo() {
    // Pegar todos os inputs com data-body-part
    const inputs = document.querySelectorAll('input[data-body-part]');
    
    inputs.forEach(input => {
        const bodyPart = input.getAttribute('data-body-part');
        
        // Adicionar event listeners para hover
        input.addEventListener('mouseenter', () => {
            highlightBodyPart(bodyPart, true);
        });
        
        input.addEventListener('mouseleave', () => {
            highlightBodyPart(bodyPart, false);
        });
        
        // Também adicionar para focus (quando clica no campo)
        input.addEventListener('focus', () => {
            highlightBodyPart(bodyPart, true);
        });
        
        input.addEventListener('blur', () => {
            highlightBodyPart(bodyPart, false);
        });
    });
}

function highlightBodyPart(bodyPart, show) {
    // Pegar todos os elementos que correspondem à parte do corpo
    const highlights = document.querySelectorAll(`[data-highlight="${bodyPart}"]`);
    
    highlights.forEach(highlight => {
        if (show) {
            highlight.classList.add('active');
        } else {
            highlight.classList.remove('active');
        }
    });
}

function toggleAllHighlights() {
    const allHighlights = document.querySelectorAll('.body-highlight-overlay');
    const btn = document.getElementById('toggle-highlights-btn');
    
    // Verificar se algum está visível
    const isAnyVisible = Array.from(allHighlights).some(h => h.classList.contains('active'));
    
    allHighlights.forEach(highlight => {
        if (isAnyVisible) {
            highlight.classList.remove('active');
        } else {
            highlight.classList.add('active');
        }
    });
    
    // Atualizar texto do botão
    btn.textContent = isAnyVisible ? 'Mostrar grupamentos' : 'Ocultar grupamentos';
}

// ========================================
// LOGOUT
// ========================================

async function fazerLogout() {
    try {
        const response = await fetch('/api/logout', {
            method: 'POST'
        });
        
        if (response.ok) {
            window.location.href = '/login';
        } else {
            mostrarToast('Erro ao fazer logout', 'error');
        }
    } catch (error) {
        console.error('Erro ao fazer logout:', error);
        mostrarToast('Erro ao fazer logout', 'error');
    }
}
