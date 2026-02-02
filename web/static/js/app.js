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
// INICIALIZAÇÃO
// ========================================

document.addEventListener('DOMContentLoaded', async () => {
    await checkSystemStatus();
    await checkAdmin();
    await carregarUsuario();
    await carregarAvaliacoes();
    inicializarEventos();
    inicializarMapaInterativo();
    aplicarTema();
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
    
    // Avaliação básica
    let avaliacaoBasicaHTML = `
        <div class="grid-item">
            <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--text-primary);">📊 Avaliação Básica</h3>
            <div class="avaliacao-header" style="justify-content: space-between; display: flex; align-items: center; margin-bottom: 1rem;">
                <span class="avaliacao-date">📅 ${data}</span>
                <button class="btn-icon" onclick="deletarAvaliacao('${avaliacao.id}')" title="Deletar">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <polyline points="3 6 5 6 21 6"></polyline>
                        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                </button>
            </div>
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
    
    return `
        <div class="avaliacao-card">
            <div class="avaliacoes-grid">
                ${avaliacaoBasicaHTML}
                ${renderModulosAvancados(avaliacao)}
            </div>
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
                        <div class="legenda-item" data-index="${index}" data-chart="${chartId}" data-label="${item.label}" data-percentual="${item.percentual}">
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
function destacarFatia(index, label, percentual) {
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
    
    // Atualizar centro do gráfico
    const centros = document.querySelectorAll('.grafico-centro');
    centros.forEach(centro => {
        centro.querySelector('.centro-percentual').textContent = `${percentual}%`;
        centro.querySelector('.centro-label').textContent = label;
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
        
        fatia.addEventListener('mouseenter', () => destacarFatia(index, label, percentual));
        fatia.addEventListener('mouseleave', () => resetarGrafico());
    });
    
    // Eventos para itens da legenda
    document.querySelectorAll('.legenda-item').forEach(item => {
        const index = parseInt(item.getAttribute('data-index'));
        const label = item.getAttribute('data-label');
        const percentual = parseFloat(item.getAttribute('data-percentual'));
        
        item.addEventListener('mouseenter', () => destacarFatia(index, label, percentual));
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
                <div class="regiao-item" style="border-color: ${config.cor};">
                    <div class="regiao-titulo">${nome}</div>
                    
                    <div class="regiao-medidas-row">
                        <div class="medida-col">
                            <span class="medida-label">Atual</span>
                            <span class="medida-valor-destaque" style="color: ${config.cor};">${valorAtual} cm</span>
                        </div>
                        <div class="medida-col">
                            <span class="medida-label">Ideal</span>
                            <span class="medida-valor-destaque">${valorIdeal} cm</span>
                        </div>
                        <div class="medida-col">
                            <span class="medida-label">Diferença</span>
                            <span class="medida-valor-destaque ${diferenca > 0 ? 'positivo' : 'negativo'}">${diferenca > 0 ? '+' : ''}${diferenca.toFixed(1)} cm</span>
                        </div>
                    </div>
                    
                    <div class="regiao-status-final" style="background: ${config.bg};">
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
            <div class="mapa-grid-2col">
                ${regioesHTML}
            </div>
            
            ${gordura ? `
            <div class="gordura-central-card">
                <div class="gordura-header">
                    <span class="gordura-titulo">📊 Indicadores de Gordura Central</span>
                </div>
                <div class="gordura-indices">
                    <div class="indice-item">
                        <span class="indice-label">RCQ (Relação Cintura/Quadril)</span>
                        <span class="indice-valor">${gordura.rcq}</span>
                        <span class="indice-risco">${gordura.rcq_descricao}</span>
                    </div>
                    <div class="indice-item">
                        <span class="indice-label">RCA (Relação Cintura/Altura)</span>
                        <span class="indice-valor">${gordura.rca}</span>
                        <span class="indice-risco">${gordura.rca_descricao}</span>
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
            <div class="score-primeira-linha">
                <div class="score-grafico-box">
                    <svg width="200" height="200" viewBox="0 0 200 200">
                        <path d="M 30 170 A 90 90 0 0 1 170 170" 
                              fill="none" 
                              stroke="#e9ecef" 
                              stroke-width="25"
                              stroke-linecap="round"/>
                        <path d="M 30 170 A 90 90 0 0 1 170 170" 
                              fill="none" 
                              stroke="${score.cor}" 
                              stroke-width="25"
                              stroke-linecap="round"
                              stroke-dasharray="${(score.score_total / 100) * 283} 283"
                              style="transition: stroke-dasharray 1s ease;"/>
                    </svg>
                    <div class="score-centro-box">
                        <div class="score-numero-box" style="color: ${score.cor}">${score.score_total}</div>
                        <div class="score-de-100">/100</div>
                    </div>
                </div>
                
                <div class="score-info-box">
                    <div class="score-titulo-box">Pontuação Estética</div>
                    <div class="score-valor-box" style="color: ${score.cor}">${score.score_total}<span class="score-max">/100</span></div>
                    <div class="score-classificacao-box">${score.classificacao}</div>
                    <div class="score-descricao-box">
                        Avaliação baseada em percentual de gordura, proporções corporais, simetria e distribuição de massa.
                    </div>
                </div>
            </div>
            
            <!-- Segunda linha: 5 critérios -->
            <div class="score-criterios-grid">
                <div class="criterio-card">
                    <div class="criterio-icon">🎯</div>
                    <div class="criterio-nome">% Gordura</div>
                    <div class="criterio-pontos">${breakdown.gordura || 0}<span>/100</span></div>
                    <div class="criterio-peso">Peso ${pesos.gordura || '30%'}</div>
                </div>
                
                <div class="criterio-card">
                    <div class="criterio-icon">💪</div>
                    <div class="criterio-nome">Ombro/Cintura</div>
                    <div class="criterio-pontos">${breakdown.ombro_cintura || 0}<span>/100</span></div>
                    <div class="criterio-peso">Peso ${pesos.ombro_cintura || '25%'}</div>
                </div>
                
                <div class="criterio-card">
                    <div class="criterio-icon">🏋️</div>
                    <div class="criterio-nome">Peitoral/Cintura</div>
                    <div class="criterio-pontos">${breakdown.peitoral_cintura || 0}<span>/100</span></div>
                    <div class="criterio-peso">Peso ${pesos.peitoral_cintura || '20%'}</div>
                </div>
                
                <div class="criterio-card">
                    <div class="criterio-icon">⚖️</div>
                    <div class="criterio-nome">Simetria</div>
                    <div class="criterio-pontos">${breakdown.simetria || 0}<span>/100</span></div>
                    <div class="criterio-peso">Peso ${pesos.simetria || '15%'}</div>
                </div>
                
                <div class="criterio-card">
                    <div class="criterio-icon">📊</div>
                    <div class="criterio-nome">Gordura Central</div>
                    <div class="criterio-pontos">${breakdown.gordura_central || 0}<span>/100</span></div>
                    <div class="criterio-peso">Peso ${pesos.gordura_central || '10%'}</div>
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
    
    // Setup admin tabs
    if (adminModal) {
        setupAdminTabs();
    }
    
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
    container.textContent = 'Carregando...';
    
    try {
        const response = await fetch('/api/admin/database');
        if (response.ok) {
            const data = await response.json();
            container.textContent = JSON.stringify(data, null, 2);
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
