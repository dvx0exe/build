// Dados globais
let currentUser = null;
let characters = [];
let selectedCharacterId = null;

// Classes de personagens com atributos base e equipamentos
const characterClasses = {
    Heroi: {
        baseStats: { vigor: 14, mente: 9, fortitude: 12, forca: 16, destreza: 9, inteligencia: 7, fe: 8, arcano: 11 },
        equipment: ["Machado de batalha", "Escudo de couro"],
        clothes: []
    },
    Bandido: {
        baseStats: { vigor: 10, mente: 11, fortitude: 10, forca: 9, destreza: 13, inteligencia: 9, fe: 8, arcano: 14 },
        equipment: ["Adaga", "Arco curto"],
        clothes: ["Capuz de couro"]
    },
    Astrologo: {
        baseStats: { vigor: 9, mente: 15, fortitude: 8, forca: 8, destreza: 12, inteligencia: 16, fe: 7, arcano: 16 },
        equipment: ["Cajado", "Grimório"],
        clothes: ["Túnica estrelada"]
    },
    Guerreiro: {
        baseStats: { vigor: 15, mente: 10, fortitude: 14, forca: 16, destreza: 12, inteligencia: 8, fe: 9, arcano: 7 },
        equipment: ["Espada longa", "Escudo de metal"],
        clothes: ["Armadura de placas"]
    },
    Prisioneiro: {
        baseStats: { vigor: 11, mente: 12, fortitude: 11, forca: 11, destreza: 14, inteligencia: 14, fe: 6, arcano: 9 },
        equipment: ["Estoque", "Correntes"],
        clothes: ["Trapos de prisioneiro"]
    },
    Confessor: {
        baseStats: { vigor: 10, mente: 13, fortitude: 10, forca: 10, destreza: 12, inteligencia: 13, fe: 16, arcano: 9 },
        equipment: ["Maça", "Tomo sagrado"],
        clothes: ["Vestes clericais"]
    },
    Miseravel: {
        baseStats: { vigor: 10, mente: 10, fortitude: 10, forca: 10, destreza: 10, inteligencia: 10, fe: 10, arcano: 10 },
        equipment: ["Porrete"],
        clothes: ["Trapos"]
    },
    Vagabundo: {
        baseStats: { vigor: 11, mente: 10, fortitude: 10, forca: 10, destreza: 13, inteligencia: 9, fe: 14, arcano: 7 },
        equipment: ["Adaga", "Escudo pequeno"],
        clothes: ["Vestes simples"]
    },
    Profeta: {
        baseStats: { vigor: 10, mente: 14, fortitude: 8, forca: 11, destreza: 10, inteligencia: 7, fe: 16, arcano: 10 },
        equipment: ["Lança", "Talismã"],
        clothes: ["Túnica de oráculo"]
    },
    Samurai: {
        baseStats: { vigor: 12, mente: 11, fortitude: 13, forca: 15, destreza: 15, inteligencia: 9, fe: 8, arcano: 8 },
        equipment: ["Katana", "Arco longo"],
        clothes: ["Armadura de samurai"]
    }
};

// Builds disponíveis para cada classe
const classBuilds = {
    Heroi: [
        { name: "Força do Destino", description: "Build focado em alta força e vigor.", statChanges: { forca: 20, vigor: 18, fortitude: 15 }, equipment: ["Espada Lendária"], clothes: ["Armadura de Cavaleiro"] },
        { name: "Espírito Indomável", description: "Combina força com agilidade.", statChanges: { forca: 18, destreza: 16, vigor: 14 }, equipment: ["Machado de Guerra"], clothes: ["Cota de Malha Real"] },
        { name: "Herói Ancestral", description: "Foco em combate corpo a corpo.", statChanges: { forca: 22, vigor: 16, fortitude: 14 }, equipment: ["Martelo de Guerra"], clothes: ["Túnica do Herói"] }
    ],
    Bandido: [
        { name: "Sombra Ardilosa", description: "Especialista em furtividade.", statChanges: { destreza: 20, arcano: 12, vigor: 10 }, equipment: ["Adaga Silenciosa"], clothes: ["Manto das Sombras"] },
        { name: "Lâmina Veloz", description: "Foco em velocidade e precisão.", statChanges: { destreza: 18, mente: 16, vigor: 12 }, equipment: ["Espada Curta"], clothes: ["Vestimentas Leves"] },
        { name: "Golpe Furtivo", description: "Aproveita ataques críticos.", statChanges: { destreza: 19, arcano: 14, vigor: 11 }, equipment: ["Punhal de Assassino"], clothes: ["Capuz do Ladrão"] }
    ],
    Astrologo: [
        { name: "Visão Estelar", description: "Conjura feitiços devastadores.", statChanges: { inteligencia: 22, mente: 20, arcano: 15 }, equipment: ["Cajado da Aurora"], clothes: ["Robe Celestial"] },
        { name: "Mente Cósmica", description: "Equilíbrio entre magia e defesa.", statChanges: { inteligencia: 20, mente: 18, arcano: 18 }, equipment: ["Vara Arcana"], clothes: ["Manto do Cosmos"] },
        { name: "Conjurador Celestial", description: "Especialista em encantamentos.", statChanges: { inteligencia: 24, arcano: 20, mente: 16 }, equipment: ["Orbe Estelar"], clothes: ["Túnica dos Astros"] }
    ],
    Guerreiro: [
        { name: "Força Brutal", description: "Maximiza força e resistência.", statChanges: { forca: 20, vigor: 18, destreza: 15 }, equipment: ["Espada Grande"], clothes: ["Armadura de Ferro"] },
        { name: "Disciplina de Aço", description: "Técnica e poder equilibrados.", statChanges: { forca: 16, destreza: 18, vigor: 14 }, equipment: ["Sabre de Aço"], clothes: ["Cota de Aço"] },
        { name: "Guardião de Ferro", description: "Foco em defesa robusta.", statChanges: { forca: 17, vigor: 20, fortitude: 15 }, equipment: ["Machado Pesado"], clothes: ["Armadura Pesada"] }
    ],
    Prisioneiro: [
        { name: "Redenção Sombria", description: "Aproveita agilidade e astúcia.", statChanges: { destreza: 18, inteligencia: 14, vigor: 12 }, equipment: ["Estoc Ágil"], clothes: ["Vestimenta de Recluso"] },
        { name: "Liberdade Conquistada", description: "Equilibra força e destreza.", statChanges: { forca: 16, destreza: 16, vigor: 14 }, equipment: ["Espada Curta"], clothes: ["Roupas de Fuga"] },
        { name: "Espírito Rebelde", description: "Foco em ataques rápidos.", statChanges: { destreza: 20, mente: 12, vigor: 12 }, equipment: ["Adaga Rápida"], clothes: ["Manto do Rebelde"] }
    ],
    Confessor: [
        { name: "Devoto da Luz", description: "Foco em fé para curas.", statChanges: { fe: 22, vigor: 16, inteligencia: 10 }, equipment: ["Espada Sagrada"], clothes: ["Vestes Sagradas"] },
        { name: "Guardião da Fé", description: "Equilibra defesa e ataque.", statChanges: { fe: 20, fortitude: 18, vigor: 14 }, equipment: ["Martelo Sagrado"], clothes: ["Armadura do Confessor"] },
        { name: "Redentor Sagrado", description: "Transforma fé em dano.", statChanges: { fe: 24, vigor: 14, inteligencia: 12 }, equipment: ["Cajado Divino"], clothes: ["Manto do Redentor"] }
    ],
    Miseravel: [
        { name: "Renascido na Dor", description: "Transforma adversidade em poder.", statChanges: { forca: 14, vigor: 18, mente: 12 }, equipment: ["Porrete Modificado"], clothes: ["Traje do Renascido"] },
        { name: "Caminho da Adversidade", description: "Resistência e ataques.", statChanges: { forca: 16, vigor: 16, destreza: 12 }, equipment: ["Clava de Adversidade"], clothes: ["Vestimenta do Sobrevivente"] },
        { name: "Espírito Resiliente", description: "Maximiza resistência.", statChanges: { vigor: 20, mente: 14, fortitude: 12 }, equipment: ["Maça Pesada"], clothes: ["Armadura Resiliente"] }
    ],
    Vagabundo: [
        { name: "Sombra Ardilosa", description: "Mobilidade e ataques surpresa.", statChanges: { destreza: 18, vigor: 14, arcano: 12 }, equipment: ["Espada Curta"], clothes: ["Manto do Errante"] },
        { name: "Lâmina Veloz", description: "Velocidade e força combinadas.", statChanges: { destreza: 16, vigor: 16, forca: 14 }, equipment: ["Sabre Tempestuoso"], clothes: ["Capa do Andarilho"] },
        { name: "Golpe Furtivo", description: "Versátil e equilibrado.", statChanges: { destreza: 17, vigor: 15, forca: 13 }, equipment: ["Adaga Versátil"], clothes: ["Traje Errante"] }
    ],
    Profeta: [
        { name: "Voz do Apocalipse", description: "Profecias destrutivas.", statChanges: { fe: 24, mente: 16, arcano: 14 }, equipment: ["Lança Profética"], clothes: ["Vestes do Profeta"] },
        { name: "Visões do Futuro", description: "Manipula o campo de batalha.", statChanges: { fe: 22, arcano: 18, mente: 14 }, equipment: ["Cajado Oracular"], clothes: ["Manto Visionário"] },
        { name: "Selo do Destino", description: "Altera o rumo do combate.", statChanges: { fe: 26, arcano: 16, vigor: 12 }, equipment: ["Espada dos Destinos"], clothes: ["Túnica do Selo"] }
    ],
    Samurai: [
        { name: "Caminho do Samurai", description: "Precisão e disciplina.", statChanges: { destreza: 20, vigor: 16, forca: 14 }, equipment: ["Uchigatana"], clothes: ["Armadura do Samurai"] },
        { name: "Lâmina Veloz", description: "Ataques rápidos e cortes.", statChanges: { destreza: 18, vigor: 14, forca: 13 }, equipment: ["Katana Ligeira"], clothes: ["Vestimenta de Combate"] },
        { name: "Honra Eterna", description: "Defesas sólidas e contra-ataques.", statChanges: { destreza: 17, vigor: 18, forca: 15 }, equipment: ["Katana Ancestral"], clothes: ["Traje do Honorável"] }
    ]
};

// Referências aos elementos do DOM
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const createCharacterSection = document.getElementById('create-character-section');
const viewCharacterSection = document.getElementById('view-character-section');
const charactersList = document.getElementById('characters-list');
const buildOptions = document.getElementById('build-options');
const buildDescription = document.getElementById('build-description');
const buildButtonsContainer = document.getElementById('build-buttons');
const characterStats = document.getElementById('character-stats');
const characterDetails = document.getElementById('character-details');
const toast = document.getElementById('toast');

// Função para exibir mensagens temporárias
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Função para navegar entre seções
function navigateTo(section) {
    [authSection, dashboardSection, createCharacterSection, viewCharacterSection].forEach(s => {
        s.classList.add('hidden');
    });
    section.classList.remove('hidden');
}

// Função para limpar o conteúdo de um elemento
function clearElement(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

// Função para calcular modificador do atributo
function calculateModifier(value) {
    return Math.floor((value - 10) / 2);
}

function formatModifier(mod) {
    return mod >= 0 ? `+${mod}` : mod.toString();
}

// Função para converter nome do atributo para exibição
function statNameToDisplay(stat) {
    const statNames = {
        vigor: 'Vigor',
        mente: 'Mente',
        fortitude: 'Fortitude',
        forca: 'Força',
        destreza: 'Destreza',
        inteligencia: 'Inteligência',
        fe: 'Fé',
        arcano: 'Arcano'
    };
    return statNames[stat] || stat;
}

// Gerenciamento das abas de autenticação
function handleTabClick() {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            const tabId = this.getAttribute('data-tab');
            document.getElementById(`${tabId}-form`).classList.add('active');
        });
    });
}

// Função de login atualizada para usar API
async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (response.ok) {
            const data = await response.json();
            currentUser = { id: data.user_id, username: data.username };
            localStorage.setItem('currentUserId', data.user_id);
            showToast(`Bem-vindo, ${data.username}!`);
            await loadCharacters();
            navigateTo(dashboardSection);
        } else {
            const errorData = await response.json();
            showToast(errorData.message || 'Usuário ou senha inválidos!', 'error');
        }
    } catch (error) {
        showToast('Erro ao fazer login!', 'error');
    }
}

// Função de registro atualizada para usar API
async function handleRegister(event) {
    event.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (response.ok) {
            showToast('Registro concluído com sucesso!');
            document.getElementById('register-form-element').reset();
            document.querySelector('[data-tab="login"]').click();
        } else {
            const errorData = await response.json();
            showToast(errorData.message || 'Erro ao registrar!', 'error');
        }
    } catch (error) {
        showToast('Erro ao registrar!', 'error');
    }
}

// Função de logout
function handleLogout() {
    currentUser = null;
    localStorage.removeItem('currentUserId');
    characters = [];
    navigateTo(authSection);
    showToast('Sessão encerrada com sucesso!');
}

// Carrega personagens do backend
async function loadCharacters() {
    if (!currentUser) return;

    try {
        const response = await fetch(`/api/characters?user_id=${currentUser.id}`);
        if (response.ok) {
            characters = await response.json();
            clearElement(charactersList);
            if (characters.length === 0) {
                const emptyMessage = document.createElement('div');
                emptyMessage.className = 'empty-characters';
                emptyMessage.innerHTML = `
                    <div>
                        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-scroll-text" style="margin: 0 auto; color: #fcd34d50; margin-bottom: 1rem;">
                            <path d="M8 21h12a2 2 0 0 0 2-2v-2H10v2a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v3h4"></path>
                            <path d="M19 17V5a2 2 0 0 0-2-2H4"></path>
                            <path d="M15 8h-5"></path>
                            <path d="M15 12h-5"></path>
                        </svg>
                        <p class="text-lg">Você ainda não tem personagens</p>
                        <p class="text-sm" style="opacity: 0.7; margin-top: 0.5rem;">Crie seu primeiro personagem para começar sua aventura</p>
                    </div>
                `;
                charactersList.appendChild(emptyMessage);
                return;
            }
            characters.forEach(char => {
                const card = document.createElement('div');
                card.className = 'character-card';
                card.innerHTML = `
                    <h3>${char.nome}</h3>
                    <div class="character-info">
                        <span>Classe:</span> ${char.classe}
                    </div>
                    <div class="character-info">
                        <span>Raça:</span> ${char.raca}
                    </div>
                    <div class="character-info">
                        <span> semplanzaIdade:</span> ${char.idade}
                    </div>
                    ${char.build_escolhida ? `<div class="character-info"><span>Build:</span> ${char.build_escolhida}</div>` : ''}
                    ${char.equipamento && char.equipamento.length > 0 ? `<div class="character-extra">
                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sword" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                            <polyline points="14.5 17.5 3 6 6 3 17.5 14.5"></polyline>
                            <line x1="13" y1="19" x2="19" y2="13"></line>
                            <line x1="16" y1="16" x2="20" y2="20"></line>
                            <line x1="19" y1="21" x2="21" y2="19"></line>
                        </svg>
                        ${char.equipamento.slice(0, 2).join(', ')}${char.equipamento.length > 2 ? '...' : ''}
                    </div>` : ''}
                    <div class="character-extra" style="display: flex; align-items: center; justify-content: space-between;">
                        <div>
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar" style="display: inline-block; vertical-align: middle; margin-right: 4px;">
                                <rect width="18" height="18" x="3" y="4" rx="2" ry="2"></rect>
                                <line x1="16" y1="2" x2="16" y2="6"></line>
                                <line x1="8" y1="2" x2="8" y2="6"></line>
                                <line x1="3" y1="10" x2="21" y2="10"></line>
                            </svg>
                            ${new Date(char.created_at).toLocaleDateString()}
                        </div>
                        <span class="character-badge">Nível 1</span>
                    </div>
                `;
                card.addEventListener('click', () => viewCharacter(char.id));
                charactersList.appendChild(card);
            });
        } else {
            showToast('Erro ao carregar personagens!', 'error');
        }
    } catch (error) {
        showToast('Erro ao carregar personagens!', 'error');
    }
}

// Gerencia mudança de classe do personagem (versão corrigida)
function handleClassChange() {
    const selectedClass = document.getElementById('character-class').value;

    clearElement(buildButtonsContainer);
    clearElement(buildDescription);
    document.getElementById('character-build').value = '';

    if (selectedClass && classBuilds[selectedClass]) {
        buildOptions.classList.remove('hidden');

        classBuilds[selectedClass].forEach((build, index) => {
            const buildBtn = document.createElement('button');
            buildBtn.className = 'btn build-btn';
            buildBtn.dataset.buildIndex = index;
            buildBtn.type = 'button'; // Garante que o botão não submeta o formulário

            const btnContent = document.createElement('div');
            btnContent.className = 'build-btn-content';

            const btnTitle = document.createElement('span');
            btnTitle.className = 'build-btn-title';
            btnTitle.textContent = build.name;

            const descContent = document.createElement('div');
            descContent.className = 'build-btn-description';
            descContent.innerHTML = `
                <div><strong>Descrição:</strong> ${build.description}</div>
                <div><strong>Atributos recomendados:</strong> ${Object.entries(build.statChanges).map(([stat, value]) => `${statNameToDisplay(stat)} +${value}`).join(', ')}</div>
                ${build.equipment && build.equipment.length ? `<div><strong>Equipamentos:</strong> ${build.equipment.join(', ')}</div>` : ''}
                ${build.clothes && build.clothes.length ? `<div><strong>Roupas:</strong> ${build.clothes.join(', ')}</div>` : ''}
            `;

            btnContent.appendChild(btnTitle);
            btnContent.appendChild(descContent);
            buildBtn.appendChild(btnContent);

            buildBtn.addEventListener('click', (event) => {
                event.preventDefault(); // Evita qualquer comportamento padrão que possa submeter o formulário
                document.querySelectorAll('.build-btn').forEach(btn => {
                    btn.classList.remove('selected');
                });
                buildBtn.classList.add('selected');
                document.getElementById('character-build').value = index;
                updateCharacterPreview(selectedClass, index);
            });

            buildButtonsContainer.appendChild(buildBtn);
        });

        updateCharacterPreview(selectedClass);
    } else {
        buildOptions.classList.add('hidden');
        clearElement(characterStats);
    }
}

// Atualiza preview do personagem
function updateCharacterPreview(characterClass, buildIndex = null) {
    if (!characterClass || !characterClasses[characterClass]) return;
    clearElement(characterStats);

    const baseStats = { ...characterClasses[characterClass].baseStats };
    if (buildIndex !== null && classBuilds[characterClass][buildIndex]) {
        const build = classBuilds[characterClass][buildIndex];
        Object.entries(build.statChanges).forEach(([stat, value]) => {
            baseStats[stat] = value;
        });
    }

    Object.entries(baseStats).forEach(([stat, value]) => {
        const statBox = document.createElement('div');
        statBox.className = 'stat-box';
        statBox.innerHTML = `
            <span class="stat-name">${statNameToDisplay(stat)}</span>
            <span class="stat-value">${value}</span>
            <span class="stat-modifier">${formatModifier(calculateModifier(value))}</span>
        `;
        characterStats.appendChild(statBox);
    });
}

// Gerencia envio do formulário de criação de personagem
async function handleCharacterFormSubmit(event) {
    event.preventDefault();
    if (!currentUser) {
        showToast('Você precisa estar logado para criar um personagem!', 'error');
        return;
    }

    const name = document.getElementById('character-name').value;
    const age = document.getElementById('character-age').value;
    const race = document.getElementById('character-race').value;
    const sex = document.getElementById('character-sex').value;
    const characterClass = document.getElementById('character-class').value;
    const buildIndex = document.getElementById('character-build').value;

    const character = {
        userId: currentUser.id,
        nome: name,
        idade: parseInt(age),
        raca: race,
        sexo: sex,
        classe: characterClass,
        stats: { ...characterClasses[characterClass].baseStats },
        equipment: [...characterClasses[characterClass].equipment],
        clothes: [...characterClasses[characterClass].clothes],
        build_escolhida: ''
    };

    if (buildIndex !== '') {
        const buildData = classBuilds[characterClass][parseInt(buildIndex)];
        character.build_escolhida = buildData.name;
        Object.entries(buildData.statChanges).forEach(([stat, value]) => {
            character.stats[stat] = value;
        });
        if (buildData.equipment) character.equipment.push(...buildData.equipment);
        if (buildData.clothes) character.clothes.push(...buildData.clothes);
    }

    const characterData = {
        user_id: currentUser.id,
        nome: character.nome,
        idade: character.idade,
        classe: character.classe,
        raca: character.raca,
        sexo: character.sexo,
        vigor: character.stats.vigor,
        mente: character.stats.mente,
        fortitude: character.stats.fortitude,
        forca: character.stats.forca,
        destreza: character.stats.destreza,
        inteligencia: character.stats.inteligencia,
        fe: character.stats.fe,
        arcano: character.stats.arcano,
        build_escolhida: character.build_escolhida,
        equipamento: character.equipment,
        roupas: character.clothes
    };

    try {
        const response = await fetch('/api/characters', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(characterData)
        });
        if (response.ok) {
            showToast('Personagem criado com sucesso!');
            document.getElementById('character-form').reset();
            clearElement(buildButtonsContainer);
            buildOptions.classList.add('hidden');
            await loadCharacters();
            navigateTo(dashboardSection);
        } else {
            const errorData = await response.json();
            showToast(errorData.message || 'Erro ao criar personagem!', 'error');
        }
    } catch (error) {
        showToast('Erro ao criar personagem!', 'error');
    }
}

// Função para visualizar detalhes do personagem
function viewCharacter(id) {
    selectedCharacterId = id;
    const character = characters.find(char => char.id === id);
    if (!character) {
        showToast('Personagem não encontrado!', 'error');
        return;
    }

    document.getElementById('character-view-title').textContent = character.nome;
    clearElement(characterDetails);

    const basicInfo = document.createElement('div');
    basicInfo.className = 'detail-group';
    basicInfo.innerHTML = `
        <h4>Informações Básicas</h4>
        <div class="detail-grid">
            <div class="detail-item">Classe: ${character.classe}</div>
            <div class="detail-item">Raça: ${character.raca}</div>
            <div class="detail-item">Sexo: ${character.sexo}</div>
            <div class="detail-item">Idade: ${character.idade}</div>
            ${character.build_escolhida ? `<div class="detail-item">Build: ${character.build_escolhida}</div>` : ''}
        </div>
    `;
    characterDetails.appendChild(basicInfo);

    const stats = document.createElement('div');
    stats.className = 'detail-group';
    stats.innerHTML = '<h4>Atributos</h4>';
    const statsGrid = document.createElement('div');
    statsGrid.className = 'stats-grid';
    ['vigor', 'mente', 'fortitude', 'forca', 'destreza', 'inteligencia', 'fe', 'arcano'].forEach(stat => {
        const value = character[stat];
        const statBox = document.createElement('div');
        statBox.className = 'stat-box';
        statBox.innerHTML = `
            <span class="stat-name">${statNameToDisplay(stat)}</span>
            <span class="stat-value">${value}</span>
            <span class="stat-modifier">${formatModifier(calculateModifier(value))}</span>
        `;
        statsGrid.appendChild(statBox);
    });
    stats.appendChild(statsGrid);
    characterDetails.appendChild(stats);

    if (character.equipamento && character.equipamento.length) {
        const equipment = document.createElement('div');
        equipment.className = 'detail-group';
        equipment.innerHTML = `
            <h4>Equipamento</h4>
            <div class="detail-grid">
                ${character.equipamento.map(item => `<div class="detail-item">${item}</div>`).join('')}
            </div>
        `;
        characterDetails.appendChild(equipment);
    }

    if (character.roupas && character.roupas.length) {
        const clothes = document.createElement('div');
        clothes.className = 'detail-group';
        clothes.innerHTML = `
            <h4>Vestimentas</h4>
            <div class="detail-grid">
                ${character.roupas.map(item => `<div class="detail-item">${item}</div>`).join('')}
            </div>
        `;
        characterDetails.appendChild(clothes);
    }

    const creationDate = document.createElement('div');
    creationDate.className = 'detail-group';
    creationDate.innerHTML = `
        <div style="color: var(--muted-foreground); font-size: 0.875rem; display: flex; align-items: center;">
            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-scroll" style="margin-right: 0.5rem;">
                <path d="M8 21h12a2 2 0 0 0 2-2v-2H10v2a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v3h4"></path>
                <path d="M19 17V5a2 2 0 0 0-2-2H4"></path>
            </svg>
            Criado em: ${new Date(character.created_at).toLocaleString()}
        </div>
    `;
    characterDetails.appendChild(creationDate);

    navigateTo(viewCharacterSection);
}

// Função para abrir o modal de exclusão
function handleDeleteCharacter() {
    document.getElementById('delete-modal').classList.remove('hidden');
}

// Inicialização
document.addEventListener('DOMContentLoaded', async () => {
    handleTabClick();

    document.getElementById('login-form-element').addEventListener('submit', handleLogin);
    document.getElementById('register-form-element').addEventListener('submit', handleRegister);
    document.getElementById('create-character-btn').addEventListener('click', () => navigateTo(createCharacterSection));
    document.getElementById('logout-btn').addEventListener('click', handleLogout);
    document.getElementById('character-class').addEventListener('change', handleClassChange);
    document.getElementById('character-form').addEventListener('submit', handleCharacterFormSubmit);
    document.getElementById('back-btn').addEventListener('click', () => navigateTo(dashboardSection));
    document.getElementById('view-back-btn').addEventListener('click', () => navigateTo(dashboardSection));
    document.getElementById('delete-character-btn').addEventListener('click', handleDeleteCharacter);
    document.getElementById('modal-cancel').addEventListener('click', () => document.getElementById('delete-modal').classList.add('hidden'));
    document.getElementById('modal-confirm').addEventListener('click', async () => {
        try {
            const response = await fetch(`/api/characters/${selectedCharacterId}`, { method: 'DELETE' });
            if (response.ok) {
                showToast('Personagem excluído com sucesso!');
                document.getElementById('delete-modal').classList.add('hidden');
                await loadCharacters();
                navigateTo(dashboardSection);
                selectedCharacterId = null;
            } else {
                showToast('Erro ao excluir personagem!', 'error');
            }
        } catch (error) {
            showToast('Erro ao excluir personagem!', 'error');
        }
    });

    const storedUserId = localStorage.getItem('currentUserId');
    if (storedUserId) {
        try {
            const response = await fetch(`/api/users/${storedUserId}`);
            if (response.ok) {
                const user = await response.json();
                currentUser = { id: user.id, username: user.login };
                await loadCharacters();
                navigateTo(dashboardSection);
            } else {
                localStorage.removeItem('currentUserId');
                navigateTo(authSection);
            }
        } catch (error) {
            localStorage.removeItem('currentUserId');
            navigateTo(authSection);
        }
    }
});

handleClassChange
