// ========================================
// SISTEMA DE MEDIDAS CORPORAIS - JAVASCRIPT
// ========================================

// Estado da aplicação
const app = {
    usuario: null,
    avaliacoes: [],
    isAdmin: false
};

// ========================================
// LOADING SCREEN
// ========================================

function showLoading() {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        loadingScreen.classList.remove('hidden');
    }
}

function hideLoading() {
    const loadingScreen = document.getElementById('loadingScreen');
    if (loadingScreen) {
        loadingScreen.classList.add('hidden');
    }
}

// ========================================
// INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    showLoading();
    
    try {
        await checkSystemStatus();
        await checkAdmin();
        await carregarUsuario();
        await carregarAvaliacoes();
        inicializarEventos();
        inicializarMapaInterativo();
        aplicarTema();
    } catch (error) {
        console.error('Erro na inicialização:', error);
        mostrarToast('Erro ao carregar aplicação', 'error');
    } finally {
        // Aguardar um pouco para garantir que a página renderizou
        setTimeout(() => {
            hideLoading();
        }, 800);
    }
});

// ========================================
// VERIFICAÇÃO DE STATUS DO SISTEMA
// ========================================

async function checkSystemStatus() {
    try {
        const response = await fetch('/api/status');
        if (response.ok) {
            const status = await response.json();
            
            // Se não estiver usando banco persistente, mostrar aviso
            if (!status.database.persistent && status.environment === 'production') {
                mostrarAvisoBancoDados();
            }
        }
    } catch (error) {
        console.error('Erro ao verificar status:', error);
    }
}

function mostrarAvisoBancoDados() {
    const aviso = document.createElement('div');
    aviso.className = 'database-warning';
    aviso.innerHTML = `
        <div class="warning-content">
            <span class="warning-icon">⚠️</span>
            <div class="warning-text">
                <strong>Banco de dados não configurado</strong>
                <p>Suas avaliações serão perdidas ao recarregar a página. Configure o PostgreSQL no Vercel.</p>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" class="warning-close">✕</button>
        </div>
    `;
    document.body.insertBefore(aviso, document.body.firstChild);
}

// ========================================
// GERENCIAMENTO DE USUÁRIO
// ========================================

async function checkAdmin() {
    try {
        const response = await fetch('/api/admin/check');
        if (response.ok) {
            const data = await response.json();
            app.isAdmin = data.is_admin;
        }
    } catch (error) {
        console.error('Erro ao verificar admin:', error);
    }
}

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
        showLoading();
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
            
            // Log para debug
            console.log('Avaliação recebida:', avaliacao);
            console.log('Resultados:', avaliacao.resultados);
            
            // Verificar se os resultados foram calculados
            if (!avaliacao.resultados || Object.keys(avaliacao.resultados).length === 0) {
                mostrarToast('Avaliação salva, mas sem resultados calculados', 'warning');
            } else {
                mostrarToast('Avaliação salva com sucesso!', 'success');
            }
            
            // Adicionar ao início da lista
            app.avaliacoes.unshift(avaliacao);
            console.log('Total de avaliações:', app.avaliacoes.length);
            
            // Renderizar
            renderizarAvaliacoes();
            limparFormulario();
        } else {
            const erro = await response.json();
            mostrarToast(erro.erro || 'Erro ao salvar avaliação', 'error');
            console.error('Erro detalhado:', erro);
        }
    } catch (error) {
        console.error('Erro ao salvar avaliação:', error);
        mostrarToast('Erro ao salvar avaliação: ' + error.message, 'error');
    } finally {
        hideLoading();
    }
}

async function deletarAvaliacao(id) {
    if (!confirm('Tem certeza que deseja deletar esta avaliação?')) {
        return;
    }

    try {
        showLoading();
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
    } finally {
        hideLoading();
    }
}

function renderizarAvaliacoes() {
    const container = document.getElementById('avaliacoesContainer');
    
    console.log('Renderizando avaliações. Total:', app.avaliacoes.length);
    
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
    console.log('Avaliações renderizadas com sucesso');
    
    // Inicializar eventos dos gráficos circulares após renderização
    setTimeout(() => inicializarEventosGraficos(), 100);
}

function criarCardAvaliacao(avaliacao) {
    const data = new Date(avaliacao.data).toLocaleDateString('pt-BR');
    const resultados = avaliacao.resultados || {};
    const medidas = avaliacao.medidas || {};
    
    console.log('Criando card para avaliação:', avaliacao.id, 'Resultados:', Object.keys(resultados));
    
    // Cabeçalho da avaliação
    const headerHTML = `
        <div class="avaliacao-header-top" style="display: flex; justify-content: space-between; align-items: center; padding: 1.5rem; background: var(--surface); border-radius: 16px 16px 0 0; border-bottom: 2px solid var(--border-color); margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <h2 style="margin: 0; font-size: 1.5rem; font-weight: 700; color: var(--text-primary);">📊 Avaliação - ${data}</h2>
            </div>
            <div style="display: flex; align-items: center; gap: 1rem;">
                <label class="switch-container" style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                    <input type="checkbox" id="publico-${avaliacao.id}" style="display: none;">
                    <div class="switch-toggle" style="position: relative; width: 50px; height: 26px; background: #ccc; border-radius: 13px; transition: background 0.3s;" onclick="togglePublico('${avaliacao.id}', this)">
                        <div class="switch-slider" style="position: absolute; top: 2px; left: 2px; width: 22px; height: 22px; background: white; border-radius: 50%; transition: transform 0.3s;"></div>
                    </div>
                    <span style="font-size: 0.85rem; color: var(--text-secondary); font-weight: 600;">Público</span>
                </label>
                <button class="btn-icon" onclick="downloadAvaliacaoPNG('${avaliacao.id}')" title="Baixar como PNG" style="padding: 0.5rem; background: var(--primary-color); border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; transform: scale(1);" onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 4px 12px rgba(99, 102, 241, 0.4)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';" onmousedown="this.style.transform='scale(0.95)';" onmouseup="this.style.transform='scale(1.1)';">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                </button>
                <button class="btn-icon" onclick="deletarAvaliacao('${avaliacao.id}')" title="Deletar" style="padding: 0.5rem; background: #ff6b6b; border: none; border-radius: 8px; cursor: pointer; transition: all 0.3s; transform: scale(1);" onmouseover="this.style.transform='scale(1.1)'; this.style.boxShadow='0 4px 12px rgba(255, 107, 107, 0.4)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';" onmousedown="this.style.transform='scale(0.95)';" onmouseup="this.style.transform='scale(1.1)';">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>
        </div>
    `;
    
    // Avaliação básica - versão horizontal (minimizada)
    const avaliacaoBasicaMinimizadaHTML = `
        <div class="avaliacao-basica-minimizada" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; padding: 1.5rem; background: var(--surface); border-radius: 12px;">
            ${medidas.peso ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Peso</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${medidas.peso} kg</div>
            </div>
            ` : ''}
            ${resultados && resultados.imc ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">IMC</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${resultados.imc}</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.25rem;">${resultados.imc_descricao || ''}</div>
            </div>
            ` : ''}
            ${resultados && resultados.percentual_gordura ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">% Gordura</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${resultados.percentual_gordura}%</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.25rem;">${resultados.classificacao_gordura || ''}</div>
            </div>
            ` : ''}
            ${resultados && resultados.massa_magra_kg ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">Massa Magra</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${resultados.massa_magra_kg} kg</div>
            </div>
            ` : ''}
            ${resultados && resultados.rcq ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">RCQ</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${resultados.rcq}</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.25rem;">${resultados.rcq_descricao || ''}</div>
            </div>
            ` : ''}
            ${resultados && resultados.rca ? `
            <div class="result-item-mini" style="text-align: center; padding: 1rem; background: var(--bg-secondary); border-radius: 8px; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                <div style="font-size: 0.75rem; color: var(--text-secondary); margin-bottom: 0.25rem;">RCA</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: var(--text-primary);">${resultados.rca}</div>
                <div style="font-size: 0.7rem; color: var(--text-secondary); margin-top: 0.25rem;">${resultados.rca_descricao || ''}</div>
            </div>
            ` : ''}
        </div>
    `;
    
    // Score minimizado
    const scoreMinimizado = resultados.score_estetico_avancado ? `
        <div class="score-minimizado" style="display: flex; align-items: center; justify-content: center; gap: 2rem; padding: 1.5rem; background: var(--surface); border-radius: 12px; margin-top: 1rem; transition: all 0.3s ease; cursor: default;" onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 8px 20px rgba(0,0,0,0.12)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
            <div style="position: relative; width: 150px; height: 150px;">
                <svg width="150" height="150" viewBox="0 0 150 150">
                    <circle cx="75" cy="75" r="65" fill="none" stroke="#e9ecef" stroke-width="16"/>
                    <circle cx="75" cy="75" r="65" fill="none" stroke="${resultados.score_estetico_avancado.cor}" stroke-width="16" stroke-dasharray="${(resultados.score_estetico_avancado.score_total / 100) * 408.41} 408.41" stroke-linecap="round" transform="rotate(-90 75 75)" style="transition: stroke-dasharray 1s ease;"/>
                </svg>
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                    <div style="font-size: 2.5rem; font-weight: 900; color: ${resultados.score_estetico_avancado.cor};">${resultados.score_estetico_avancado.score_total}</div>
                    <div style="font-size: 1rem; color: var(--text-secondary);">/100</div>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 1.2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem;">Score Estético</div>
                <div style="display: inline-block; padding: 0.5rem 1.5rem; background: ${resultados.score_estetico_avancado.cor}; color: white; border-radius: 20px; font-weight: 600;">${resultados.score_estetico_avancado.classificacao}</div>
            </div>
        </div>
    ` : '';
    
    // Avaliação básica expandida (completa)
    let avaliacaoBasicaHTML = `
        <div class="grid-item">
            <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--text-primary);">📊 Avaliação Básica</h3>
            <div style="display: grid; gap: 0.75rem;">
                ${medidas.peso ? `
                <div class="result-item">
                    <span class="result-label">Peso</span>
                    <span class="result-value">${medidas.peso} kg</span>
                </div>
                ` : ''}
                
                ${resultados && resultados.imc ? `
                <div class="result-item">
                    <span class="result-label">IMC</span>
                    <span class="result-value">${resultados.imc}</span>
                    <span class="result-desc">${resultados.imc_descricao || ''}</span>
                </div>
                ` : ''}
                
                ${resultados && resultados.percentual_gordura ? `
                <div class="result-item">
                    <span class="result-label">% Gordura</span>
                    <span class="result-value">${resultados.percentual_gordura}%</span>
                    <span class="result-desc">${resultados.classificacao_gordura || ''}</span>
                </div>
                ` : ''}
                
                ${resultados && resultados.massa_magra_kg ? `
                <div class="result-item">
                    <span class="result-label">Massa Magra</span>
                    <span class="result-value">${resultados.massa_magra_kg} kg</span>
                </div>
                ` : ''}
                
                ${resultados && resultados.rcq ? `
                <div class="result-item">
                    <span class="result-label">RCQ</span>
                    <span class="result-value">${resultados.rcq}</span>
                    <span class="result-desc">${resultados.rcq_descricao || ''}</span>
                </div>
                ` : ''}
                
                ${resultados && resultados.rca ? `
                <div class="result-item">
                    <span class="result-label">RCA</span>
                    <span class="result-value">${resultados.rca}</span>
                    <span class="result-desc">${resultados.rca_descricao || ''}</span>
                </div>
                ` : ''}
            </div>
        </div>
    `;
    
    // Footer com botão de expandir/minimizar
    const footerHTML = `
        <div class="avaliacao-footer" style="padding: 1rem 1.5rem; background: var(--surface); border-radius: 0 0 16px 16px; border-top: 2px solid var(--border-color); margin-top: 1.5rem;">
            <button onclick="toggleAvaliacaoExpansao('${avaliacao.id}')" style="width: 100%; padding: 0.75rem; background: var(--primary-color); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s; display: flex; align-items: center; justify-content: center; gap: 0.5rem; transform: scale(1);" onmouseover="this.style.transform='scale(1.02)'; this.style.boxShadow='0 6px 20px rgba(99, 102, 241, 0.3)';" onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='none';">
                <span id="toggle-text-${avaliacao.id}">Expandir Detalhes</span>
                <svg id="toggle-icon-${avaliacao.id}" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="transition: transform 0.3s ease;">
                    <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
            </button>
        </div>
    `;
    
    return `
        <div class="avaliacao-card" id="avaliacao-${avaliacao.id}" data-expanded="false" style="background: var(--surface); border-radius: 16px; margin-bottom: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.1); animation: fadeInUp 0.5s ease-out; opacity: 0; animation-fill-mode: forwards;">
            ${headerHTML}
            <div class="avaliacao-content-minimizado" id="content-min-${avaliacao.id}" style="padding: 0 1.5rem; transition: opacity 0.4s ease-in-out; opacity: 1;">
                ${avaliacaoBasicaMinimizadaHTML}
                ${scoreMinimizado}
            </div>
            <div class="avaliacao-content-expandido" id="content-exp-${avaliacao.id}" style="display: none; padding: 0 1.5rem; transition: opacity 0.4s ease-in-out; opacity: 0;">
                <div class="avaliacoes-grid">
                    ${avaliacaoBasicaHTML}
                    ${renderModulosAvancados(avaliacao)}
                </div>
            </div>
            ${footerHTML}
        </div>
    `;
}

// ========================================
// MÓDULOS AVANÇADOS
// ========================================

function renderModulosAvancados(avaliacao) {
    const resultados = avaliacao.resultados || {};
    
    // Verificar se há dados suficientes para módulos avançados
    if (!resultados || Object.keys(resultados).length === 0) {
        return '';
    }
    
    let html = '';
    
    // Composição Tecidual
    if (resultados.composicao_tecidual) {
        html += renderComposicaoTecidual(resultados.composicao_tecidual);
    }
    
    // Mapa Corporal
    if (resultados.mapa_corporal) {
        html += renderMapaCorporal(resultados.mapa_corporal);
    }
    
    // Score Estético Avançado
    if (resultados.score_estetico_avancado) {
        html += renderScoreEstetico(resultados.score_estetico_avancado);
    }
    
    return html;
}

function renderComposicaoTecidual(composicao) {
    const cores = {
        muscular: '#51cf66',
        gordura: '#ff6b6b',
        ossea: '#4dabf7',
        outros: '#868e96'
    };
    
    const dados = [
        { label: 'Massa Muscular', percentual: composicao.percentual_muscular, kg: composicao.massa_muscular_kg, cor: cores.muscular },
        { label: 'Gordura Corporal', percentual: composicao.percentual_gordura, kg: composicao.massa_gorda_kg, cor: cores.gordura },
        { label: 'Massa Óssea', percentual: composicao.percentual_osseo, kg: composicao.massa_ossea_kg, cor: cores.ossea },
        { label: 'Outros Tecidos', percentual: composicao.percentual_outros, kg: composicao.outros_tecidos_kg, cor: cores.outros }
    ];
    
    // Criar SVG do gráfico donut (anel)
    let acumulado = 0;
    let fatiasSVG = '';
    const raioExterno = 110;
    const raioInterno = 70;
    const centro = 125;
    
    dados.forEach((item, index) => {
        const angulo = (item.percentual / 100) * 360;
        const anguloInicio = acumulado;
        const anguloFim = acumulado + angulo;
        
        // Pontos do arco externo
        const x1Ext = centro + raioExterno * Math.cos((anguloInicio - 90) * Math.PI / 180);
        const y1Ext = centro + raioExterno * Math.sin((anguloInicio - 90) * Math.PI / 180);
        const x2Ext = centro + raioExterno * Math.cos((anguloFim - 90) * Math.PI / 180);
        const y2Ext = centro + raioExterno * Math.sin((anguloFim - 90) * Math.PI / 180);
        
        // Pontos do arco interno (sentido reverso)
        const x1Int = centro + raioInterno * Math.cos((anguloFim - 90) * Math.PI / 180);
        const y1Int = centro + raioInterno * Math.sin((anguloFim - 90) * Math.PI / 180);
        const x2Int = centro + raioInterno * Math.cos((anguloInicio - 90) * Math.PI / 180);
        const y2Int = centro + raioInterno * Math.sin((anguloInicio - 90) * Math.PI / 180);
        
        const largeArc = angulo > 180 ? 1 : 0;
        
        fatiasSVG += `
            <path class="fatia-grafico" 
                  data-index="${index}"
                  data-label="${item.label}"
                  data-percentual="${item.percentual}"
                  data-kg="${item.kg}"
                  d="M ${x1Ext},${y1Ext} A ${raioExterno},${raioExterno} 0 ${largeArc},1 ${x2Ext},${y2Ext} L ${x1Int},${y1Int} A ${raioInterno},${raioInterno} 0 ${largeArc},0 ${x2Int},${y2Int} Z" 
                  fill="${item.cor}"/>
        `;
        
        acumulado += angulo;
    });
    
    // ID único para evitar conflitos
    const chartId = `chart-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    
    return `
        <div class="grid-item">
            <div class="modulo-titulo">💪 Composição Tecidual</div>
            <div class="composicao-container">
                <div class="composicao-legenda" id="legenda-${chartId}">
                    ${dados.map((item, index) => `
                        <div class="legenda-item" data-index="${index}" data-chart="${chartId}" data-label="${item.label}" data-percentual="${item.percentual}" data-kg="${item.kg}">
                            <div class="legenda-cor" style="background: ${item.cor}"></div>
                            <div class="legenda-info">
                                <span class="legenda-label">${item.label}</span>
                                <span class="legenda-percentual">${item.percentual}% (${item.kg} kg)</span>
                            </div>
                        </div>
                    `).join('')}
                </div>
                <div class="grafico-circular-container">
                    <svg class="grafico-circular" id="svg-${chartId}" viewBox="0 0 250 250">
                        ${fatiasSVG}
                    </svg>
                    <div class="grafico-centro" id="centro-${chartId}" data-peso="${composicao.peso_total}">
                        <div class="centro-percentual">${composicao.peso_total}</div>
                        <div class="centro-label">kg Total</div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Funções auxiliares para o gráfico circular interativo
function destacarFatia(index, label, percentual, kg) {
    const fatias = document.querySelectorAll('.fatia-grafico');
    fatias.forEach((fatia, i) => {
        if (i === index) {
            fatia.style.opacity = '1';
            fatia.style.transform = 'scale(1.05)';
            fatia.style.filter = 'brightness(1.2)';
        } else {
            fatia.style.opacity = '0.6';
        }
    });
    
    // Atualizar centro do gráfico com kg
    const centros = document.querySelectorAll('.grafico-centro');
    centros.forEach(centro => {
        const percentualEl = centro.querySelector('.centro-percentual');
        const labelEl = centro.querySelector('.centro-label');
        
        // Separar número e "kg"
        const kgNum = kg.toString().split('.')[0];
        const kgDec = kg.toString().split('.')[1] || '0';
        
        percentualEl.innerHTML = `${kg}<span style="font-size: 0.5em; font-weight: 400; margin-left: 4px;">kg</span>`;
        labelEl.textContent = label;
    });
}

function resetarGrafico() {
    const fatias = document.querySelectorAll('.fatia-grafico');
    fatias.forEach(fatia => {
        fatia.style.opacity = '1';
        fatia.style.transform = 'scale(1)';
        fatia.style.filter = 'none';
    });
    
    // Restaurar peso total
    const centros = document.querySelectorAll('.grafico-centro');
    centros.forEach(centro => {
        const pesoTotal = centro.getAttribute('data-peso');
        if (pesoTotal) {
            centro.querySelector('.centro-percentual').textContent = pesoTotal;
            centro.querySelector('.centro-label').textContent = 'kg Total';
        }
    });
}

// Inicializar eventos de hover nos gráficos após renderização
function inicializarEventosGraficos() {
    // Eventos para fatias SVG
    document.querySelectorAll('.fatia-grafico').forEach(fatia => {
        const index = parseInt(fatia.getAttribute('data-index'));
        const label = fatia.getAttribute('data-label');
        const percentual = parseFloat(fatia.getAttribute('data-percentual'));
        const kg = parseFloat(fatia.getAttribute('data-kg'));
        
        fatia.addEventListener('mouseenter', () => destacarFatia(index, label, percentual, kg));
        fatia.addEventListener('mouseleave', () => resetarGrafico());
    });
    
    // Eventos para itens da legenda
    document.querySelectorAll('.legenda-item').forEach(item => {
        const index = parseInt(item.getAttribute('data-index'));
        const label = item.getAttribute('data-label');
        const percentual = parseFloat(item.getAttribute('data-percentual'));
        const kg = parseFloat(item.getAttribute('data-kg'));
        
        item.addEventListener('mouseenter', () => destacarFatia(index, label, percentual, kg));
        item.addEventListener('mouseleave', () => resetarGrafico());
    });
}

function renderMapaCorporal(mapa) {
    console.log('renderMapaCorporal chamado com:', mapa);
    
    const regioes = mapa.regioes || {};
    const gordura = mapa.gordura_central;
    
    // Verificar se regioes está vazio
    if (Object.keys(regioes).length === 0) {
        console.warn('Mapa corporal sem regiões. Dados recebidos:', mapa);
        return '<div class="grid-item-full"><p style="color: var(--text-secondary); text-align: center; padding: 2rem;">Mapa corporal não disponível para esta avaliação.</p></div>';
    }
    
    const statusConfig = {
        'Subdesenvolvido': { emoji: '⚠️', cor: '#ff6b6b', bg: '#ff6b6b' },
        'Equilibrado': { emoji: '✅', cor: '#51cf66', bg: '#51cf66' },
        'Excesso': { emoji: '🔴', cor: '#ffa94d', bg: '#ffa94d' }
    };
    
    let regioesHTML = '';
    let regioesRenderizadas = 0;
    
    for (const [nome, dados] of Object.entries(regioes)) {
        console.log(`Processando região ${nome}:`, dados);
        
        if (dados && (dados.real || dados.atual)) {
            const valorAtual = dados.real || dados.atual;
            const valorIdeal = dados.ideal;
            const diferenca = dados.diferenca_cm || dados.diferenca || (valorAtual - valorIdeal);
            const descricao = dados.descricao || dados.status || 'Normal';
            
            const config = statusConfig[descricao] || { emoji: '📏', cor: '#868e96', bg: '#868e96' };
            regioesHTML += `
                <div class="regiao-item" style="border-color: ${config.cor}; background: var(--surface); border-radius: 16px; padding: 1.5rem; border-width: 2px; border-style: solid; display: flex !important; flex-direction: column !important; gap: 1rem;">
                    <div class="regiao-titulo" style="font-size: 1.3rem; font-weight: 700; text-align: center; padding-bottom: 0.75rem; border-bottom: 2px solid var(--border-color); margin: 0;">${nome}</div>
                    
                    <div class="regiao-medidas-row" style="display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 1rem !important;">
                        <div class="medida-col" style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: 12px;">
                            <span class="medida-label" style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600;">Atual</span>
                            <span class="medida-valor-destaque" style="font-size: 1.4rem; font-weight: 800; color: ${config.cor};">${valorAtual} cm</span>
                        </div>
                        <div class="medida-col" style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: 12px;">
                            <span class="medida-label" style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600;">Ideal</span>
                            <span class="medida-valor-destaque" style="font-size: 1.4rem; font-weight: 800; color: var(--text-primary);">${valorIdeal} cm</span>
                        </div>
                        <div class="medida-col" style="display: flex; flex-direction: column; align-items: center; gap: 0.5rem; padding: 1rem; background: var(--bg-secondary); border-radius: 12px;">
                            <span class="medida-label" style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary); font-weight: 600;">Diferença</span>
                            <span class="medida-valor-destaque" style="font-size: 1.4rem; font-weight: 800; color: ${diferenca > 0 ? '#51cf66' : '#ff6b6b'};">${diferenca > 0 ? '+' : ''}${diferenca.toFixed(1)} cm</span>
                        </div>
                    </div>
                    
                    <div class="regiao-status-final" style="display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 1rem; border-radius: 12px; background: ${config.bg}; color: white; font-weight: 700; font-size: 1.1rem; text-transform: uppercase;">
                        <span class="status-emoji">${config.emoji}</span>
                        <span class="status-texto">${descricao}</span>
                    </div>
                </div>
            `;
            regioesRenderizadas++;
        }
    }
    
    console.log(`${regioesRenderizadas} regiões renderizadas no layout de cards`);
    
    if (regioesRenderizadas === 0) {
        return '<div class="grid-item-full"><p style="color: var(--text-secondary); text-align: center; padding: 2rem;">Nenhuma região válida encontrada no mapa corporal.</p></div>';
    }
    
    return `
        <div class="grid-item-full">
            <div class="modulo-titulo">🗺️ Mapa de Distribuição Corporal</div>
            <div class="mapa-grid-2col" style="display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1.5rem !important; width: 100% !important; margin: 1.5rem 0 !important;">
                ${regioesHTML}
            </div>
            
            ${gordura ? `
            <div class="gordura-central-card" style="background: var(--surface); padding: 2rem; border-radius: 16px; margin-top: 1.5rem;">
                <div class="gordura-header" style="margin-bottom: 1.5rem;">
                    <span class="gordura-titulo" style="font-size: 1.1rem; font-weight: 700; color: var(--text-primary);">📊 Indicadores de Gordura Central</span>
                </div>
                <div class="gordura-indices" style="display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 1.5rem !important;">
                    <div class="indice-item" style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                        <span class="indice-label" style="display: block; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">RCQ (Relação Cintura/Quadril)</span>
                        <span class="indice-valor" style="display: block; font-size: 2rem; font-weight: 800; color: var(--text-primary); margin: 0.5rem 0;">${gordura.rcq}</span>
                        <span class="indice-risco" style="display: block; font-size: 0.8rem; color: var(--text-secondary);">${gordura.rcq_descricao}</span>
                    </div>
                    <div class="indice-item" style="background: var(--bg-secondary); padding: 1.5rem; border-radius: 12px; text-align: center; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-4px)'; this.style.boxShadow='0 8px 16px rgba(0,0,0,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='none';">
                        <span class="indice-label" style="display: block; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 0.5rem;">RCA (Relação Cintura/Altura)</span>
                        <span class="indice-valor" style="display: block; font-size: 2rem; font-weight: 800; color: var(--text-primary); margin: 0.5rem 0;">${gordura.rca}</span>
                        <span class="indice-risco" style="display: block; font-size: 0.8rem; color: var(--text-secondary);">${gordura.rca_descricao}</span>
                    </div>
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

function renderScoreEstetico(score) {
    const breakdown = score.breakdown || {};
    const pesos = score.pesos || {};
    
    return `
        <div class="grid-item-full">
            <div class="modulo-titulo">⭐ Score Estético Corporal</div>
            
            <!-- Primeira linha: Gráfico + Score -->
            <div class="score-primeira-linha" style="display: grid !important; grid-template-columns: auto 1fr !important; gap: 2rem !important; align-items: center !important; margin-bottom: 2rem !important; background: var(--surface); padding: 2rem; border-radius: 16px;">
                <div class="score-grafico-box" style="position: relative; width: 200px; height: 200px;">
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        <circle cx="100" cy="100" r="85" fill="none" stroke="#e9ecef" stroke-width="20"/>
                        <circle cx="100" cy="100" r="85" fill="none" stroke="${score.cor}" stroke-width="20" stroke-dasharray="${(score.score_total / 100) * 534.07} 534.07" stroke-linecap="round" transform="rotate(-90 100 100)" style="transition: stroke-dasharray 1s ease;"/>
                    </svg>
                    <div class="score-centro-box" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                        <div class="score-numero-box" style="font-size: 3rem; font-weight: 900; color: ${score.cor};">${score.score_total}</div>
                        <div class="score-de-100" style="font-size: 1.2rem; color: var(--text-secondary); margin-top: -0.5rem;">/100</div>
                    </div>
                </div>
                
                <div class="score-info-box" style="display: flex; flex-direction: column; gap: 1rem;">
                    <div class="score-titulo-box" style="font-size: 1.8rem; font-weight: 700; color: var(--text-primary);">Pontuação Estética</div>
                    <div class="score-valor-box" style="font-size: 2.5rem; font-weight: 900; color: ${score.cor};">${score.score_total}<span class="score-max" style="font-size: 1.5rem; color: var(--text-secondary);">/100</span></div>
                    <div class="score-classificacao-box" style="display: inline-block; padding: 0.5rem 1.5rem; background: ${score.cor}; color: white; border-radius: 20px; font-weight: 600; font-size: 1.1rem; width: fit-content;">${score.classificacao}</div>
                    <div class="score-descricao-box" style="color: var(--text-secondary); line-height: 1.6; font-size: 0.95rem;">
                        Avaliação baseada em percentual de gordura, proporções corporais, simetria e distribuição de massa.
                    </div>
                </div>
            </div>
            
            <!-- Segunda linha: 5 critérios -->
            <div class="score-criterios-grid" style="display: grid !important; grid-template-columns: repeat(5, 1fr) !important; gap: 1rem !important;">
                <div class="criterio-card" style="background: var(--surface); padding: 1.5rem; border-radius: 12px; text-align: center; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.3s ease;">
                    <div class="criterio-icon" style="font-size: 2.5rem;">🎯</div>
                    <div class="criterio-nome" style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">% Gordura</div>
                    <div style="position: relative; width: 80px; height: 80px; margin: 0 auto;">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="30" fill="none" stroke="#e9ecef" stroke-width="8"/>
                            <circle cx="40" cy="40" r="30" fill="none" stroke="var(--primary-color)" stroke-width="8" stroke-dasharray="${(breakdown.gordura || 0) / 20 * 188.4} 188.4" stroke-linecap="round" transform="rotate(-90 40 40)" style="transition: stroke-dasharray 1s ease;"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.3rem; font-weight: 800; color: var(--primary-color);">${breakdown.gordura || 0}</div>
                    </div>
                    <div class="criterio-pontos" style="font-size: 0.85rem; color: var(--text-secondary);">de 20 pontos</div>
                    <div class="criterio-peso" style="font-size: 0.8rem; color: var(--text-secondary);">Peso ${pesos.gordura || '30%'}</div>
                </div>
                
                <div class="criterio-card" style="background: var(--surface); padding: 1.5rem; border-radius: 12px; text-align: center; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.3s ease;">
                    <div class="criterio-icon" style="font-size: 2.5rem;">💪</div>
                    <div class="criterio-nome" style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">Ombro/Cintura</div>
                    <div style="position: relative; width: 80px; height: 80px; margin: 0 auto;">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="30" fill="none" stroke="#e9ecef" stroke-width="8"/>
                            <circle cx="40" cy="40" r="30" fill="none" stroke="var(--primary-color)" stroke-width="8" stroke-dasharray="${(breakdown.ombro_cintura || 0) / 20 * 188.4} 188.4" stroke-linecap="round" transform="rotate(-90 40 40)" style="transition: stroke-dasharray 1s ease;"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.3rem; font-weight: 800; color: var(--primary-color);">${breakdown.ombro_cintura || 0}</div>
                    </div>
                    <div class="criterio-pontos" style="font-size: 0.85rem; color: var(--text-secondary);">de 20 pontos</div>
                    <div class="criterio-peso" style="font-size: 0.8rem; color: var(--text-secondary);">Peso ${pesos.ombro_cintura || '25%'}</div>
                </div>
                
                <div class="criterio-card" style="background: var(--surface); padding: 1.5rem; border-radius: 12px; text-align: center; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.3s ease;">
                    <div class="criterio-icon" style="font-size: 2.5rem;">🏋️</div>
                    <div class="criterio-nome" style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">Peitoral/Cintura</div>
                    <div style="position: relative; width: 80px; height: 80px; margin: 0 auto;">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="30" fill="none" stroke="#e9ecef" stroke-width="8"/>
                            <circle cx="40" cy="40" r="30" fill="none" stroke="var(--primary-color)" stroke-width="8" stroke-dasharray="${(breakdown.peitoral_cintura || 0) / 20 * 188.4} 188.4" stroke-linecap="round" transform="rotate(-90 40 40)" style="transition: stroke-dasharray 1s ease;"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.3rem; font-weight: 800; color: var(--primary-color);">${breakdown.peitoral_cintura || 0}</div>
                    </div>
                    <div class="criterio-pontos" style="font-size: 0.85rem; color: var(--text-secondary);">de 20 pontos</div>
                    <div class="criterio-peso" style="font-size: 0.8rem; color: var(--text-secondary);">Peso ${pesos.peitoral_cintura || '20%'}</div>
                </div>
                
                <div class="criterio-card" style="background: var(--surface); padding: 1.5rem; border-radius: 12px; text-align: center; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.3s ease;">
                    <div class="criterio-icon" style="font-size: 2.5rem;">⚖️</div>
                    <div class="criterio-nome" style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">Simetria</div>
                    <div style="position: relative; width: 80px; height: 80px; margin: 0 auto;">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="30" fill="none" stroke="#e9ecef" stroke-width="8"/>
                            <circle cx="40" cy="40" r="30" fill="none" stroke="var(--primary-color)" stroke-width="8" stroke-dasharray="${(breakdown.simetria || 0) / 20 * 188.4} 188.4" stroke-linecap="round" transform="rotate(-90 40 40)" style="transition: stroke-dasharray 1s ease;"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.3rem; font-weight: 800; color: var(--primary-color);">${breakdown.simetria || 0}</div>
                    </div>
                    <div class="criterio-pontos" style="font-size: 0.85rem; color: var(--text-secondary);">de 20 pontos</div>
                    <div class="criterio-peso" style="font-size: 0.8rem; color: var(--text-secondary);">Peso ${pesos.simetria || '15%'}</div>
                </div>
                
                <div class="criterio-card" style="background: var(--surface); padding: 1.5rem; border-radius: 12px; text-align: center; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.3s ease;">
                    <div class="criterio-icon" style="font-size: 2.5rem;">📊</div>
                    <div class="criterio-nome" style="font-size: 0.9rem; color: var(--text-secondary); font-weight: 600;">Gordura Central</div>
                    <div style="position: relative; width: 80px; height: 80px; margin: 0 auto;">
                        <svg width="80" height="80" viewBox="0 0 80 80">
                            <circle cx="40" cy="40" r="30" fill="none" stroke="#e9ecef" stroke-width="8"/>
                            <circle cx="40" cy="40" r="30" fill="none" stroke="var(--primary-color)" stroke-width="8" stroke-dasharray="${(breakdown.gordura_central || 0) / 20 * 188.4} 188.4" stroke-linecap="round" transform="rotate(-90 40 40)" style="transition: stroke-dasharray 1s ease;"/>
                        </svg>
                        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 1.3rem; font-weight: 800; color: var(--primary-color);">${breakdown.gordura_central || 0}</div>
                    </div>
                    <div class="criterio-pontos" style="font-size: 0.85rem; color: var(--text-secondary);">de 20 pontos</div>
                    <div class="criterio-peso" style="font-size: 0.8rem; color: var(--text-secondary);">Peso ${pesos.gordura_central || '10%'}</div>
                </div>
            </div>
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
// FUNÇÕES DE AVALIAÇÃO - HEADER
// ========================================

// Toggle de expansão da avaliação
function toggleAvaliacaoExpansao(avaliacaoId) {
    const card = document.getElementById(`avaliacao-${avaliacaoId}`);
    const contentMin = document.getElementById(`content-min-${avaliacaoId}`);
    const contentExp = document.getElementById(`content-exp-${avaliacaoId}`);
    const toggleText = document.getElementById(`toggle-text-${avaliacaoId}`);
    const toggleIcon = document.getElementById(`toggle-icon-${avaliacaoId}`);
    
    const isExpanded = card.dataset.expanded === 'true';
    
    if (isExpanded) {
        // Minimizar com fade out/in
        contentExp.style.opacity = '0';
        setTimeout(() => {
            contentExp.style.display = 'none';
            contentMin.style.display = 'block';
            setTimeout(() => {
                contentMin.style.opacity = '1';
            }, 50);
        }, 300);
        
        card.dataset.expanded = 'false';
        toggleText.textContent = 'Expandir Detalhes';
        toggleIcon.style.transform = 'rotate(0deg)';
        
        // Salvar preferência
        localStorage.setItem(`avaliacao-${avaliacaoId}-expanded`, 'false');
    } else {
        // Expandir com fade out/in
        contentMin.style.opacity = '0';
        setTimeout(() => {
            contentMin.style.display = 'none';
            contentExp.style.display = 'block';
            setTimeout(() => {
                contentExp.style.opacity = '1';
            }, 50);
        }, 300);
        
        card.dataset.expanded = 'true';
        toggleText.textContent = 'Minimizar';
        toggleIcon.style.transform = 'rotate(180deg)';
        
        // Salvar preferência
        localStorage.setItem(`avaliacao-${avaliacaoId}-expanded`, 'true');
    }
}

function togglePublico(avaliacaoId, toggleElement) {
    const checkbox = document.getElementById(`publico-${avaliacaoId}`);
    const slider = toggleElement.querySelector('.switch-slider');
    const isPublic = !checkbox.checked;
    
    checkbox.checked = isPublic;
    
    if (isPublic) {
        toggleElement.style.background = 'var(--primary-color)';
        slider.style.transform = 'translateX(24px)';
        mostrarToast('Avaliação marcada como pública', 'success');
    } else {
        toggleElement.style.background = '#ccc';
        slider.style.transform = 'translateX(0)';
        mostrarToast('Avaliação marcada como privada', 'info');
    }
    
    // TODO: Salvar estado no backend quando a funcionalidade de rede social for implementada
    console.log(`Avaliação ${avaliacaoId} definida como ${isPublic ? 'pública' : 'privada'}`);
}

async function downloadAvaliacaoPNG(avaliacaoId) {
    mostrarToast('Preparando download...', 'info');
    
    try {
        // Verificar se o elemento existe
        const avaliacaoElement = document.getElementById(`avaliacao-${avaliacaoId}`);
        
        if (!avaliacaoElement) {
            mostrarToast('Erro: Avaliação não encontrada', 'error');
            console.error('Elemento não encontrado:', `avaliacao-${avaliacaoId}`);
            return;
        }
        
        // Guardar estado original da avaliação
        const card = document.getElementById(`avaliacao-${avaliacaoId}`);
        const contentMin = document.getElementById(`content-min-${avaliacaoId}`);
        const contentExp = document.getElementById(`content-exp-${avaliacaoId}`);
        const wasExpanded = card.dataset.expanded === 'true';
        
        // Expandir temporariamente se estiver minimizada
        if (!wasExpanded) {
            contentMin.style.display = 'none';
            contentExp.style.display = 'block';
            contentExp.style.opacity = '1';
            card.dataset.expanded = 'true';
            
            // Aguardar renderização
            await new Promise(resolve => setTimeout(resolve, 100));
        }
        
        // Importar html2canvas se não estiver carregado
        if (typeof html2canvas === 'undefined') {
            mostrarToast('Carregando biblioteca...', 'info');
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js';
            script.crossOrigin = 'anonymous';
            document.head.appendChild(script);
            
            await new Promise((resolve, reject) => {
                script.onload = () => {
                    console.log('html2canvas carregado com sucesso');
                    resolve();
                };
                script.onerror = () => {
                    console.error('Erro ao carregar html2canvas');
                    reject(new Error('Falha ao carregar biblioteca'));
                };
                setTimeout(() => reject(new Error('Timeout ao carregar biblioteca')), 10000);
            });
        }
        
        console.log('Iniciando captura da avaliação...');
        
        // Clonar elemento para evitar problemas com CSS inline
        const clone = avaliacaoElement.cloneNode(true);
        clone.style.position = 'absolute';
        clone.style.left = '-9999px';
        clone.style.top = '0';
        
        // Remover footer do clone (botão de expandir/minimizar)
        const footer = clone.querySelector('.avaliacao-footer');
        if (footer) {
            footer.remove();
        }
        
        document.body.appendChild(clone);
        
        // Definir background baseado no tema
        const isDark = document.body.classList.contains('dark-theme');
        const bgColor = isDark ? '#1a1a1a' : '#ffffff';
        
        // Capturar o elemento clonado como imagem
        const canvas = await html2canvas(clone, {
            backgroundColor: bgColor,
            scale: 2,
            logging: false,
            useCORS: true,
            allowTaint: true,
            foreignObjectRendering: false,
            ignoreElements: (element) => {
                // Ignorar elementos que podem causar problemas
                return element.tagName === 'SCRIPT' || element.tagName === 'STYLE';
            }
        });
        
        // Remover clone
        document.body.removeChild(clone);
        
        // Restaurar estado original
        if (!wasExpanded) {
            contentExp.style.opacity = '0';
            setTimeout(() => {
                contentExp.style.display = 'none';
                contentMin.style.display = 'block';
                setTimeout(() => {
                    contentMin.style.opacity = '1';
                }, 50);
            }, 300);
            card.dataset.expanded = 'false';
        }
        
        console.log('Canvas gerado, criando download...');
        
        // Converter para blob e baixar
        canvas.toBlob((blob) => {
            if (!blob) {
                mostrarToast('Erro ao gerar imagem', 'error');
                return;
            }
            
            const url = URL.createObjectURL(blob);
            const link = document.createElement('a');
            const data = new Date().toISOString().split('T')[0];
            link.download = `avaliacao-bodyxp-${data}.png`;
            link.href = url;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
            mostrarToast('Download concluído!', 'success');
        }, 'image/png');
        
    } catch (error) {
        console.error('Erro detalhado ao gerar PNG:', error);
        mostrarToast(`Erro: ${error.message}`, 'error');
    }
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

function mostrarModalSenha() {
    document.getElementById('passwordModal').classList.add('active');
}

function esconderModalSenha() {
    document.getElementById('passwordModal').classList.remove('active');
    document.getElementById('passwordForm').reset();
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
    
    // Botão de admin (se existir)
    const adminBtn = document.getElementById('adminBtn');
    if (adminBtn) {
        adminBtn.addEventListener('click', mostrarAdminModal);
    }
    
    // Theme toggle switch
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.addEventListener('change', alternarTema);
    }
    
    // Fechar modal
    document.getElementById('closeModal').addEventListener('click', esconderModal);
    
    // Fechar modal de senha
    document.getElementById('closePasswordModal').addEventListener('click', esconderModalSenha);
    
    // Fechar modal admin
    const closeAdminModal = document.getElementById('closeAdminModal');
    if (closeAdminModal) {
        closeAdminModal.addEventListener('click', esconderAdminModal);
    }
    
    // Clique fora do modal
    document.getElementById('userModal').addEventListener('click', (e) => {
        if (e.target.id === 'userModal') {
            esconderModal();
        }
    });
    
    // Clique fora do modal de senha
    document.getElementById('passwordModal').addEventListener('click', (e) => {
        if (e.target.id === 'passwordModal') {
            esconderModalSenha();
        }
    });
    
    // Clique fora do modal admin
    const adminModal = document.getElementById('adminModal');
    if (adminModal) {
        adminModal.addEventListener('click', (e) => {
            if (e.target.id === 'adminModal') {
                esconderAdminModal();
            }
        });
    }
    
    // Botão de carregar database
    const loadDbBtn = document.getElementById('loadDbBtn');
    if (loadDbBtn) {
        loadDbBtn.addEventListener('click', carregarDatabase);
    }
    
    // Navegação por tabelas do BD
    const dbTableBtns = document.querySelectorAll('.db-table-btn');
    dbTableBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active de todos
            dbTableBtns.forEach(b => {
                b.classList.remove('active');
                b.style.background = 'var(--bg-secondary)';
                b.style.color = 'var(--text-primary)';
            });
            
            // Adiciona active no clicado
            this.classList.add('active');
            this.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
            this.style.color = 'white';
            
            // Limpar conteúdo anterior
            document.getElementById('databaseContent').textContent = 'Clique em "Carregar Dados" para visualizar';
            document.getElementById('dbRecordCount').textContent = '';
        });
    });
    
    // Setup admin tabs
    if (adminModal) {
        setupAdminTabs();
    }
    
    // Formulário de usuário
    document.getElementById('userForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const altura = parseFloat(document.getElementById('userHeight').value);
        
        // Validar altura
        if (isNaN(altura) || altura <= 0) {
            mostrarToast('Por favor, insira uma altura válida', 'erro');
            return;
        }
        
        const dados = {
            nome: document.getElementById('userName').value,
            data_nascimento: document.getElementById('userBirthdate').value,
            sexo: document.getElementById('userSex').value,
            email: document.getElementById('userEmail').value,
            altura: altura
        };
        
        await salvarUsuario(dados);
    });
    
    // Formulário de mudança de senha
    document.getElementById('passwordForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const senhaAtual = document.getElementById('currentPassword').value;
        const novaSenha = document.getElementById('newPassword').value;
        const confirmarSenha = document.getElementById('confirmPassword').value;
        
        // Validar senhas
        if (novaSenha !== confirmarSenha) {
            mostrarToast('As senhas não coincidem', 'error');
            return;
        }
        
        if (novaSenha.length < 6) {
            mostrarToast('A senha deve ter pelo menos 6 caracteres', 'error');
            return;
        }
        
        await mudarSenha(senhaAtual, novaSenha);
    });
    
    // Calcular idade automaticamente
    document.getElementById('userBirthdate').addEventListener('change', (e) => {
        if (e.target.value) {
            const idade = calcularIdade(e.target.value);
            document.getElementById('userAge').value = `${idade} anos`;
        }
    });
    
    // Botão de salvar avaliação
    document.getElementById('saveBtn').addEventListener('click', salvarAvaliacao);
    
    // Navegação com Enter nos formulários
    setupEnterNavigation();
    
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
// MUDANÇA DE SENHA
// ========================================

async function mudarSenha(senhaAtual, novaSenha) {
    try {
        showLoading();
        
        const response = await fetch('/api/mudar-senha', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                senha_atual: senhaAtual,
                nova_senha: novaSenha
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            mostrarToast('Senha alterada com sucesso!', 'success');
            esconderModalSenha();
            document.getElementById('passwordForm').reset();
        } else {
            mostrarToast(data.erro || 'Erro ao mudar senha', 'error');
        }
    } catch (error) {
        console.error('Erro ao mudar senha:', error);
        mostrarToast('Erro ao mudar senha', 'error');
    } finally {
        hideLoading();
    }
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

// ========================================
// NAVEGAÇÃO COM ENTER
// ========================================

function setupEnterNavigation() {
    // Formulário de medidas (avaliação)
    const medidasInputs = [
        'pescoco', 'ombros', 'peitoral', 'cintura', 
        'abdomen', 'quadril', 'braco_relaxado', 'braco_contraido',
        'antebraco', 'coxa', 'panturrilha', 'peso', 'objetivo'
    ];
    
    medidasInputs.forEach((id, index) => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    
                    // Se for o último campo, salvar
                    if (index === medidasInputs.length - 1) {
                        document.getElementById('saveBtn').click();
                    } else {
                        // Ir para o próximo campo
                        let nextIndex = index + 1;
                        while (nextIndex < medidasInputs.length) {
                            const nextInput = document.getElementById(medidasInputs[nextIndex]);
                            if (nextInput) {
                                nextInput.focus();
                                break;
                            }
                            nextIndex++;
                        }
                    }
                }
            });
        }
    });
    
    // Formulário de usuário
    const userInputs = [
        'userName', 'userBirthdate', 'userSex', 
        'userEmail', 'userHeight'
    ];
    
    userInputs.forEach((id, index) => {
        const input = document.getElementById(id);
        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    
                    // Se for o último campo, submeter formulário
                    if (index === userInputs.length - 1) {
                        document.getElementById('userForm').dispatchEvent(new Event('submit'));
                    } else {
                        // Ir para o próximo campo
                        let nextIndex = index + 1;
                        while (nextIndex < userInputs.length) {
                            const nextInput = document.getElementById(userInputs[nextIndex]);
                            if (nextInput) {
                                nextInput.focus();
                                // Se for select, abrir o dropdown
                                if (nextInput.tagName === 'SELECT') {
                                    nextInput.click();
                                }
                                break;
                            }
                            nextIndex++;
                        }
                    }
                }
            });
        }
    });
}

// ========================================
// ADMIN PANEL
// ========================================

function mostrarAdminModal() {
    document.getElementById('adminModal').classList.add('active');
    carregarEstatisticas();
}

function esconderAdminModal() {
    document.getElementById('adminModal').classList.remove('active');
}

async function carregarEstatisticas() {
    try {
        const response = await fetch('/api/admin/stats');
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('statContas').textContent = stats.total_contas;
            document.getElementById('statAvaliacoes').textContent = stats.total_avaliacoes;
            document.getElementById('statModo').textContent = stats.modo;
        } else {
            mostrarToast('Erro ao carregar estatísticas', 'error');
        }
    } catch (error) {
        console.error('Erro ao carregar estatísticas:', error);
        mostrarToast('Erro ao carregar estatísticas', 'error');
    }
}

async function carregarDatabase() {
    const container = document.getElementById('databaseContent');
    const countSpan = document.getElementById('dbRecordCount');
    const activeBtn = document.querySelector('.db-table-btn.active');
    const table = activeBtn ? activeBtn.dataset.table : 'all';
    
    container.textContent = 'Carregando...';
    countSpan.textContent = '';
    
    try {
        const url = table === 'all' ? '/api/admin/database' : `/api/admin/database?table=${table}`;
        const response = await fetch(url);
        
        if (response.ok) {
            const data = await response.json();
            container.textContent = JSON.stringify(data, null, 2);
            
            // Contar registros
            let count = 0;
            if (table === 'all') {
                count = Object.values(data).reduce((sum, arr) => {
                    return sum + (Array.isArray(arr) ? arr.length : 0);
                }, 0);
                countSpan.textContent = `${count} registros no total`;
            } else {
                count = Array.isArray(data) ? data.length : 0;
                countSpan.textContent = `${count} registro${count !== 1 ? 's' : ''}`;
            }
        } else {
            const erro = await response.json();
            container.textContent = `Erro: ${erro.erro}`;
            mostrarToast('Erro ao carregar dados', 'error');
        }
    } catch (error) {
        console.error('Erro ao carregar database:', error);
        container.textContent = `Erro: ${error.message}`;
        mostrarToast('Erro ao carregar dados', 'error');
    }
}

function setupAdminTabs() {
    const tabs = document.querySelectorAll('.admin-tab');
    const contents = document.querySelectorAll('.admin-tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.getAttribute('data-tab');
            
            // Remove active from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            
            // Add active to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(targetTab + 'Tab').classList.add('active');
        });
    });
}
