const API_URL = "http://127.0.0.1:8000";

let publicMap;
let publicMarker;
let marcadoresEventos = [];

const dicionario = {
    pt: {
        txtHeroTitle: "Explore Torneios Próximos",
        txtHeroDesc: "Encontre campeonatos criados pela comunidade ou registre o seu próprio evento clicando no mapa!",
        txtMapaComunidade: "<i class='fa-solid fa-earth-americas'></i> Mapa de Torneios da Comunidade",
        txtCriarRemoto: "<i class='fa-solid fa-plus'></i> Publicar Meu Torneio",
        lblPubNome: "Nome do Torneio",
        lblPubData: "Data do Evento",
        lblPubLocal: "Coordenadas (Clique no mapa acima)",
        lblPubDesc: "Descrição / Premiação",
        btnEnviarPublico: "Lançar Torneio na Rede",
        txtListaGlobal: "<i class='fa-solid fa-fire'></i> Torneios Ativos na Sua Região"
    },
    en: {
        txtHeroTitle: "Explore Nearby Tournaments",
        txtHeroDesc: "Find championships created by the community or register your own event by clicking on the map!",
        txtMapaComunidade: "<i class='fa-solid fa-earth-americas'></i> Community Tournaments Map",
        txtCriarRemoto: "<i class='fa-solid fa-plus'></i> Publish My Tournament",
        lblPubNome: "Tournament Name",
        lblPubData: "Event Date",
        lblPubLocal: "Coordinates (Click on the map above)",
        lblPubDesc: "Description / Prizes",
        btnEnviarPublico: "Launch Tournament on Network",
        txtListaGlobal: "<i class='fa-solid fa-fire'></i> Active Tournaments in Your Area"
    }
};

document.addEventListener("DOMContentLoaded", () => {
    inicializarPortalPublico();
    configurarNavegacaoLogin();
    configurarTema();
    configurarIdioma();
});

// 🌐 INICIALIZA O PORTAL DA COMUNIDADE COM MAPA INTEGRADO
async function inicializarPortalPublico() {
    publicMap = L.map('public-map').setView([-15.7801, -47.9292], 4);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(publicMap);

    publicMap.on('click', (e) => {
        const { lat, lng } = e.latlng;
        document.getElementById("pub-ev-local").value = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
        
        if (publicMarker) {
            publicMarker.setLatLng(e.latlng);
        } else {
            publicMarker = L.marker(e.latlng).addTo(publicMap);
        }
    });

    await carregarDadosPublicos();
    configurarFormularioPublico();
}

// 📥 TRAZ OS TORNEIOS DA API PARA O MAPA E PARA AS LISTAS
async function carregarDadosPublicos() {
    try {
        const res = await fetch(API_URL + "/eventos/");
        if (!res.ok) return;
        const eventos = await res.json();

        const gridPublico = document.getElementById("lista-eventos-publicos");
        const tabelaAdmin = document.getElementById("tabela-eventos-admin");
        const selectCampeonato = document.getElementById("camp-evento");

        if (gridPublico) gridPublico.innerHTML = "";
        if (tabelaAdmin) tabelaAdmin.innerHTML = "";
        if (selectCampeonato) selectCampeonato.innerHTML = '<option value="">Selecione...</option>';

        marcadoresEventos.forEach(m => publicMap.removeLayer(m));
        marcadoresEventos = [];

        eventos.forEach(ev => {
            // 1. Gera cartões visuais para os visitantes do Portal
            if (gridPublico) {
                gridPublico.innerHTML += `
                    <div class="public-card">
                        <h4>${ev.nome}</h4>
                        <p><i class="fa-solid fa-calendar-day"></i> <strong>Data:</strong> ${new Date(ev.data_inicio).toLocaleDateString('pt-BR')}</p>
                        <p><i class="fa-solid fa-location-dot"></i> <strong>GPS:</strong> ${ev.local_evento}</p>
                        <p class="feed-desc-text">${ev.descricao || 'Sem descrição adicional.'}</p>
                    </div>`;
            }

            // 2. Alimenta a lista de gerenciamento interno do Admin
            if (tabelaAdmin) {
                tabelaAdmin.innerHTML += `<tr>
                    <td><strong>${ev.nome}</strong></td>
                    <td>${ev.local_evento}</td>
                    <td>${new Date(ev.data_inicio).toLocaleDateString('pt-BR')}</td>
                    <td>${ev.descricao || '-'}</td>
                </tr>`;
            }

            if (selectCampeonato) {
                selectCampeonato.innerHTML += `<option value="${ev.id_evento}">${ev.nome}</option>`;
            }

            // 3. Adiciona marcador no mapa
            const coords = ev.local_evento.split(",").map(Number);
            if (coords.length === 2 && !isNaN(coords[0]) && !isNaN(coords[1])) {
                const pino = L.marker([coords[0], coords[1]]).addTo(publicMap)
                    .bindPopup(`<b>${ev.nome}</b><br>${ev.descricao || ''}`);
                marcadoresEventos.push(pino);
            }
        });
    } catch (err) {
        console.error("Erro ao carregar dados da API:", err);
    }
}

// 📤 ENVIO DO FORMULÁRIO COMUNITÁRIO (CRIAÇÃO COMPLETA)
function configurarFormularioPublico() {
    document.getElementById("form-evento-publico").onsubmit = async (e) => {
        e.preventDefault();
        const dados = {
            nome: document.getElementById("pub-ev-nome").value,
            data_inicio: document.getElementById("pub-ev-data").value,
            local_evento: document.getElementById("pub-ev-local").value,
            descricao: document.getElementById("pub-ev-descricao").value
        };

        const res = await fetch(API_URL + "/eventos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });

        if (res.ok) {
            alert("Sucesso! Seu torneio foi publicado no banco de dados.");
            document.getElementById("form-evento-publico").reset();
            if (publicMarker) {
                publicMap.removeLayer(publicMarker);
                publicMarker = null;
            }
            await carregarDadosPublicos();
        } else {
            alert("Erro ao publicar o torneio.");
        }
    };
}

// 🔒 GERENCIAMENTO DE ACESSO AO PAINEL DE CONTROLE
function configurarNavegacaoLogin() {
    const overlay = document.getElementById("login-overlay");
    const portal = document.getElementById("portal-publico");
    const dashboard = document.getElementById("main-dashboard");

    document.getElementById("btn-abrir-login").onclick = () => overlay.style.display = "flex";
    document.getElementById("btn-fechar-login").onclick = () => overlay.style.display = "none";

    document.getElementById("form-login").onsubmit = async (e) => {
        e.preventDefault();
        const email = document.getElementById("login-email").value;
        const senha = document.getElementById("login-senha").value;

        if (email === "admin@eventhub.com" && senha === "123456") {
            overlay.style.display = "none";
            portal.style.display = "none";
            dashboard.style.display = "flex";
            
            const statusDot = document.getElementById("api-status");
            statusDot.innerHTML = '<span class="status-dot online"></span> API Online';
            
            // Carrega de forma segura os dados administrativos nas tabelas
            try { await carregarDadosPublicos(); } catch(e){}
            try { await carregarParticipantes(); } catch(e){}
            try { await carregarCampeonatos(); } catch(e){}
            try { await carregarInscricoes(); } catch(e){}
            
            configurarFormulariosAdmin();
        } else {
            alert("Acesso negado. Credenciais incorretas.");
        }
    };

    document.getElementById("btn-logout").onclick = () => {
        dashboard.style.display = "none";
        portal.style.display = "flex";
        setTimeout(() => publicMap.invalidateSize(), 200);
    };

    // Cliques das abas internas do Admin
    const links = document.querySelectorAll(".menu a");
    links.forEach(link => {
        link.onclick = (e) => {
            e.preventDefault();
            links.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
            document.querySelectorAll(".content-section").forEach(s => s.style.display = "none");
            document.getElementById(link.getAttribute("href").substring(1)).style.display = "block";
        };
    });
}

// FORMULÁRIOS INTERNOS DO CADASTRO ADMIN
function configurarFormulariosAdmin() {
    document.getElementById("form-participante").onsubmit = async (e) => {
        e.preventDefault();
        const dados = {
            nome: document.getElementById("part-nome").value,
            email: document.getElementById("part-email").value,
            telefone: document.getElementById("part-telefone").value
        };
        const res = await fetch(API_URL + "/participantes/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (res.ok) { 
            alert("Atleta Cadastrado com sucesso!"); 
            document.getElementById("form-participante").reset(); 
            await carregarParticipantes(); 
        }
    };

    document.getElementById("form-campeonato").onsubmit = async (e) => {
        e.preventDefault();
        const dados = {
            id_evento: parseInt(document.getElementById("camp-evento").value),
            modalidade: document.getElementById("camp-modalidade").value,
            premiacao: parseFloat(document.getElementById("camp-premiacao").value || 0),
            vagas_limitadas: parseInt(document.getElementById("camp-vagas").value)
        };
        const res = await fetch(API_URL + "/campeonatos/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (res.ok) { 
            alert("Campeonato Criado!"); 
            document.getElementById("form-campeonato").reset(); 
            await carregarCampeonatos(); 
        }
    };

    document.getElementById("form-inscricao").onsubmit = async (e) => {
        e.preventDefault();
        const dados = {
            id_participante: parseInt(document.getElementById("ins-participante").value),
            id_campeonato: parseInt(document.getElementById("ins-campeonato").value)
        };
        const res = await fetch(API_URL + "/inscricoes/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        });
        if (res.ok) { 
            alert("Inscrição Confirmada!"); 
            document.getElementById("form-inscricao").reset(); 
            await carregarInscricoes(); 
        }
    };
}

// TEMA, IDIOMA E LISTAGEM AUXILIAR
function configurarTema() {
    const body = document.body;
    const alternar = (btn) => {
        if (body.classList.contains("dark-theme")) {
            body.className = "light-theme";
            btn.innerHTML = '<i class="fa-solid fa-moon"></i>';
        } else {
            body.className = "dark-theme";
            btn.innerHTML = '<i class="fa-solid fa-sun"></i>';
        }
    };
    document.getElementById("theme-toggle").onclick = () => alternar(document.getElementById("theme-toggle"));
    document.getElementById("theme-toggle-public").onclick = () => alternar(document.getElementById("theme-toggle-public"));
}

function configurarIdioma() {
    const select = document.getElementById("select-language");
    select.onchange = (e) => {
        const lang = e.target.value;
        const termos = dicionario[lang];
        for (const id in termos) {
            const el = document.getElementById(id);
            if (el) el.innerHTML = termos[id];
        }
    };
}

async function carregarParticipantes() {
    const res = await fetch(API_URL + "/participantes/"); if (!res.ok) return;
    const dados = await res.json();
    const t = document.getElementById("tabela-participantes"); const s = document.getElementById("ins-participante");
    if(t) t.innerHTML = ""; if(s) s.innerHTML = '<option value="">Selecione...</option>';
    dados.forEach(p => {
        if(t) t.innerHTML += `<tr><td>#${p.id_participante}</td><td>${p.nome}</td><td>${p.email}</td><td>${p.telefone || '-'}</td></tr>`;
        if(s) s.innerHTML += `<option value="${p.id_participante}">${p.nome}</option>`;
    });
}

async function carregarCampeonatos() {
    const res = await fetch(API_URL + "/campeonatos/"); if (!res.ok) return;
    const dados = await res.json();
    const t = document.getElementById("tabela-campeonatos"); const s = document.getElementById("ins-campeonato");
    if(t) t.innerHTML = ""; if(s) s.innerHTML = '<option value="">Selecione...</option>';
    dados.forEach(c => {
        if(t) t.innerHTML += `<tr><td>${c.nome_evento || 'Evento'}</td><td>${c.modalidade}</td><td>R$ ${c.premiacao}</td><td>${c.vagas_limitadas}</td></tr>`;
        if(s) s.innerHTML += `<option value="${c.id_campeonato}">${c.modalidade}</option>`;
    });
}

async function carregarInscricoes() {
    const res = await fetch(API_URL + "/inscricoes/"); if (!res.ok) return;
    const dados = await res.json();
    const t = document.getElementById("tabela-inscricoes"); if(t) t.innerHTML = "";
    dados.forEach(i => { if(t) t.innerHTML += `<tr><td>${i.nome_participante}</td><td>${i.modalidade_campeonato}</td><td>${i.nome_evento}</td><td>${i.status_inscricao}</td></tr>`; });
}