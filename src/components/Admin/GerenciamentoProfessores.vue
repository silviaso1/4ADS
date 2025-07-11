<template>
  <div class="gerenciamento">
    <div class="gerenciamento__cabecalho">
      <button class="botao-primario" @click="abrirModalProfessor(null)">
        <i class="fas fa-plus"></i>
        Novo Professor
      </button>
    </div>
    
    <div class="barra-pesquisa">
      <i class="fas fa-search icone-pesquisa"></i>
      <input
        type="text"
        class="campo-pesquisa"
        placeholder="Pesquisar professores..."
        v-model="termoPesquisa"
      >
    </div>
    
    <div class="tabela-wrapper">
      <table class="tabela" v-if="!loading && professores.length">
        <thead>
          <tr>
            <th class="coluna-nome">Nome</th>
            <th class="coluna-email">Email</th>
            <th class="coluna-acoes">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="professor in professoresFiltrados" :key="professor.id">
            <td class="coluna-nome">{{ professor.nome }}</td>
            <td class="coluna-email">{{ professor.email }}</td>
            <td class="coluna-acoes">
              <div class="acoes-wrapper">
                <button 
                  class="botao-icone botao-editar"
                  @click="abrirModalProfessor(professor)"
                  aria-label="Editar professor"
                >
                  <i class="fas fa-edit"></i>
                </button>
                <button 
                  class="botao-icone botao-excluir"
                  @click="confirmarExclusao(professor)"
                  aria-label="Excluir professor"
                >
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button 
                  class="botao-icone botao-turmas"
                  @click="selecionarProfessorParaTurma(professor)"
                  aria-label="Vincular a turmas"
                >
                  <i class="fas fa-chalkboard-teacher"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="loading" class="sem-resultados">
        <p>Carregando professores...</p>
      </div>
      
      <div v-if="!loading && professores.length === 0" class="sem-resultados">
        <i class="fas fa-user-tie icone-vazio"></i>
        <p>Nenhum professor cadastrado</p>
      </div>

      <div v-else-if="!loading && professoresFiltrados.length === 0" class="sem-resultados">
        <i class="fas fa-search icone-vazio"></i>
        <p>Nenhum professor encontrado com o termo "{{ termoPesquisa }}"</p>
      </div>
    </div>

    <!-- Seção de Turmas Vinculadas -->
    <div class="secao-turmas" v-if="professorSelecionadoParaTurma">
      <div class="cabecalho-secao">
        <h3 class="titulo-secao">Turmas do Professor</h3>
        <button 
          class="botao-secundario" 
          @click="cancelarSelecaoProfessor"
        >
          <i class="fas fa-times"></i>
          <span>Cancelar seleção</span>
        </button>
      </div>

      <div class="info-professor">
        <span class="nome-professor">{{ professorSelecionadoParaTurma.nome }}</span>
        <span class="id-professor">ID: {{ professorSelecionadoParaTurma.id }}</span>
      </div>

      <!-- Filtros -->
      <div class="filtros-turmas">
        <select v-model="filtroPeriodo" class="campo-selecao">
          <option value="">Todos os períodos</option>
          <option v-for="periodo in periodosUnicos" :key="periodo" :value="periodo">
            {{ periodo }}
          </option>
        </select>
      </div>

      <!-- Tabela de turmas -->
      <div class="tabela-wrapper">
        <table class="tabela">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nome</th>
              <th>Período</th>
              <th>Horário</th>
              <th>Sala</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="turma in turmasFiltradas" :key="turma.id">
              <td>{{ turma.codigo }}</td>
              <td>{{ turma.nome }}</td>
              <td>{{ turma.periodo }}</td>
              <td>{{ turma.horario }}</td>
              <td>{{ turma.sala }}</td>
              <td>
                <div class="acoes-wrapper">
                  <button 
                    class="botao-icone botao-desvincular"
                    @click="confirmarDesvincularTurma(turma)"
                    v-if="turma.professor === professorSelecionadoParaTurma.id"
                  >
                    <i class="fas fa-unlink"></i>
                  </button>
                  <button 
                    class="botao-icone botao-vincular"
                    @click="vincularProfessorATurma(turma)"
                    v-else
                  >
                    <i class="fas fa-link"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="turmasFiltradas.length === 0" class="sem-resultados">
          <div class="empty-state">
            <i class="fas fa-chalkboard-teacher icone-vazio"></i>
            <h3>Nenhuma turma encontrada</h3>
            <p v-if="filtroPeriodo">Não há turmas no período selecionado</p>
            <p v-else>Este professor não está vinculado a nenhuma turma</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Professor -->
    <div v-if="modalProfessorAberto" class="modal-overlay" @click.self="fecharModalProfessor">
      <div class="modal">
        <div class="modal__cabecalho">
          <h3 class="modal__titulo">
            {{ professorEditando ? 'Editar Professor' : 'Cadastrar Professor' }}
          </h3>
          <button class="modal__fechar" @click="fecharModalProfessor">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="modal__corpo">
          <div class="campo-formulario">
            <label for="nomeProfessor">Nome *</label>
            <input
              id="nomeProfessor"
              type="text"
              v-model="professorLocal.nome"
              required
              placeholder="Nome completo"
            >
          </div>

          <div class="campo-formulario">
            <label for="emailProfessor">Email *</label>
            <input
              id="emailProfessor"
              type="email"
              v-model="professorLocal.email"
              required
              placeholder="Email institucional"
            >
          </div>

          <div class="campo-formulario" v-if="!professorEditando">
            <label for="senhaProfessor">Senha *</label>
            <input
              id="senhaProfessor"
              type="password"
              v-model="professorLocal.senha"
              required
              placeholder="Senha temporária"
            >
          </div>
        </div>

        <div class="modal__rodape">
          <button class="botao-secundario" @click="fecharModalProfessor">
            Cancelar
          </button>
          <button 
            class="botao-primario" 
            @click="salvarProfessor" 
            :disabled="!professorLocal.nome || !professorLocal.email || (!professorEditando && !professorLocal.senha)"
          >
            <i class="fas fa-save"></i>
            {{ loadingProfessor ? 'Salvando...' : 'Salvar Professor' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GerenciamentoProfessores',
  data() {
    return {
      professores: [],
      turmas: [],
      termoPesquisa: '',
      loading: false,
      loadingProfessor: false,
      modalProfessorAberto: false,
      professorEditando: null,
      professorSelecionadoParaTurma: null,
      filtroPeriodo: '',
      professorLocal: {
        nome: '',
        email: '',
        senha: '',
        tipo: 'professor'
      }
    }
  },
  computed: {
    professoresFiltrados() {
      if (!this.termoPesquisa) return this.professores;

      const termo = this.termoPesquisa.toLowerCase();
      return this.professores.filter(professor => {
        const nome = professor.nome?.toLowerCase() || '';
        const email = professor.email?.toLowerCase() || '';
        return nome.includes(termo) || email.includes(termo);
      });
    },
    turmasFiltradas() {
      let turmasFiltradas = this.turmas;
      
      // Filtrar por período se selecionado
      if (this.filtroPeriodo) {
        turmasFiltradas = turmasFiltradas.filter(t => t.periodo === this.filtroPeriodo);
      }
      
      // Ordenar turmas: primeiro as que já estão vinculadas ao professor
      turmasFiltradas = [...turmasFiltradas].sort((a, b) => {
        const aVinculada = a.professor === this.professorSelecionadoParaTurma?.id;
        const bVinculada = b.professor === this.professorSelecionadoParaTurma?.id;
        
        if (aVinculada && !bVinculada) return -1;
        if (!aVinculada && bVinculada) return 1;
        return 0;
      });
      
      return turmasFiltradas;
    },
    periodosUnicos() {
      const periodos = new Set();
      this.turmas.forEach(turma => periodos.add(turma.periodo));
      return Array.from(periodos).sort().reverse();
    }
  },
  mounted() {
    this.carregarProfessores();
    this.carregarTurmas();
  },
  methods: {
    async carregarProfessores() {
      this.loading = true;
      try {
        const response = await axios.get('http://localhost:8000/api/usuarios/');
        this.professores = response.data.filter(u => u.tipo === 'professor');
      } catch (erro) {
        console.error('Erro ao carregar professores:', erro);
        alert('Erro ao carregar lista de professores.');
      } finally {
        this.loading = false;
      }
    },
    async carregarTurmas() {
      try {
        const response = await axios.get('http://localhost:8000/api/turmas/');
        this.turmas = response.data;
      } catch (erro) {
        console.error('Erro ao carregar turmas:', erro);
        alert('Erro ao carregar lista de turmas.');
      }
    },
    abrirModalProfessor(professor) {
      this.professorEditando = professor;
      if (professor) {
        this.professorLocal = {
          nome: professor.nome,
          email: professor.email,
          senha: '',
          tipo: 'professor'
        };
      } else {
        this.professorLocal = {
          nome: '',
          email: '',
          senha: '',
          tipo: 'professor'
        };
      }
      this.modalProfessorAberto = true;
    },
    fecharModalProfessor() {
      this.modalProfessorAberto = false;
      this.professorEditando = null;
    },
    async salvarProfessor() {
      this.loadingProfessor = true;
      
      try {
        if (this.professorEditando) {
          // Atualizar professor (sem senha)
          const dados = {
            nome: this.professorLocal.nome,
            email: this.professorLocal.email,
            tipo: 'professor'
          };
          await axios.put(`http://localhost:8000/api/usuarios/${this.professorEditando.id}/`, dados);
        } else {
          // Criar novo professor
          await axios.post('http://localhost:8000/api/usuarios/', this.professorLocal);
        }
        
        await this.carregarProfessores();
        this.fecharModalProfessor();
        alert('Professor salvo com sucesso!');
      } catch (erro) {
        console.error('Erro ao salvar professor:', erro);
        alert('Erro ao salvar professor: ' + (erro.response?.data ? JSON.stringify(erro.response.data) : erro.message));
      } finally {
        this.loadingProfessor = false;
      }
    },
    confirmarExclusao(professor) {
      if (confirm(`Tem certeza que deseja excluir o professor ${professor.nome}?`)) {
        this.excluirProfessor(professor.id);
      }
    },
    async excluirProfessor(id) {
      try {
        await axios.delete(`http://localhost:8000/api/usuarios/${id}/`);
        await this.carregarProfessores();
        alert('Professor excluído com sucesso!');
      } catch (erro) {
        console.error('Erro ao excluir professor:', erro);
        alert('Erro ao excluir professor.');
      }
    },
    selecionarProfessorParaTurma(professor) {
      this.professorSelecionadoParaTurma = professor;
      this.filtroPeriodo = '';
      
      // Rolagem suave para a seção de turmas
      setTimeout(() => {
        const elemento = document.querySelector('.secao-turmas');
        if (elemento) {
          elemento.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    },
    cancelarSelecaoProfessor() {
      this.professorSelecionadoParaTurma = null;
    },
    async vincularProfessorATurma(turma) {
      if (!confirm(`Vincular o professor ${this.professorSelecionadoParaTurma.nome} à turma ${turma.codigo} - ${turma.nome}?`)) {
        return;
      }
      
      try {
        const dados = {
          ...turma,
          professor: this.professorSelecionadoParaTurma.id
        };
        
        await axios.put(`http://localhost:8000/api/turmas/${turma.id}/`, dados);
        await this.carregarTurmas();
        alert('Professor vinculado à turma com sucesso!');
      } catch (erro) {
        console.error('Erro ao vincular professor:', erro);
        alert('Erro ao vincular professor à turma.');
      }
    },
    async confirmarDesvincularTurma(turma) {
      if (!confirm(`Desvincular o professor ${this.professorSelecionadoParaTurma.nome} da turma ${turma.codigo} - ${turma.nome}?`)) {
        return;
      }
      
      try {
        const dados = {
          ...turma,
          professor: null
        };
        
        await axios.put(`http://localhost:8000/api/turmas/${turma.id}/`, dados);
        await this.carregarTurmas();
        alert('Professor desvinculado da turma com sucesso!');
      } catch (erro) {
        console.error('Erro ao desvincular professor:', erro);
        alert('Erro ao desvincular professor da turma.');
      }
    }
  }
}
</script>

<style scoped>
.gerenciamento {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  margin: 24px auto;
  max-width: 1400px;
  margin-left: 240px;
  margin-top: 70px;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}

.gerenciamento__cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.barra-pesquisa {
  position: relative;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.icone-pesquisa {
  position: absolute;
  left: 1rem;
  color: #718096;
}

.campo-pesquisa {
  width: 100%;
  padding: 14px 20px 14px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
  background-color: #f8fafc;
}

.campo-pesquisa:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  background-color: white;
}

.tabela-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #edf2f7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.tabela {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.tabela th {
  background-color: #f8fafc;
  color: #4a5568;
  font-weight: 600;
  text-align: left;
  padding: 16px 20px;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #e2e8f0;
}

.tabela td {
  padding: 16px 20px;
  border-bottom: 1px solid #edf2f7;
  color: #4a5568;
  font-size: 0.95rem;
  vertical-align: middle;
}

.tabela tr:last-child td {
  border-bottom: none;
}

.tabela tr:hover {
  background-color: #f8fafc;
}

.botao-primario {
background: #2563eb;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}



.botao-secundario {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.botao-secundario:hover {
  background: #cbd5e0;
}

.acoes-wrapper {
  display: flex;
  gap: 8px;
}

.botao-icone {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  color: white;
}

.botao-editar {
  background-color: #3b82f6;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
}

.botao-editar:hover {
  background-color: #2563eb;
}

.botao-excluir {
  background-color: #ef4444;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

.botao-excluir:hover {
  background-color: #dc2626;
}

.botao-turmas {
  background-color: #8b5cf6;
  box-shadow: 0 2px 6px rgba(139, 92, 246, 0.3);
}

.botao-turmas:hover {
  background-color: #7c3aed;
}

.botao-vincular {
  background-color: #10b981;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
}

.botao-vincular:hover {
  background-color: #059669;
}

.botao-desvincular {
  background-color: #f59e0b;
  box-shadow: 0 2px 6px rgba(245, 158, 11, 0.3);
}

.botao-desvincular:hover {
  background-color: #d97706;
}

.sem-resultados {
  padding: 3rem 1rem;
  text-align: center;
  color: #64748b;
}

.icone-vazio {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #e2e8f0;
  background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Seção de Turmas */
.secao-turmas {
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e2e8f0;
}

.cabecalho-secao {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.titulo-secao {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.info-professor {
  background: #f8fafc;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid #e2e8f0;
}

.nome-professor {
  font-weight: 600;
  font-size: 16px;
  display: block;
  margin-bottom: 5px;
}

.id-professor {
  color: #64748b;
  font-size: 14px;
}

.filtros-turmas {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.campo-selecao {
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  min-width: 200px;
  background-color: #f8fafc;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem 0;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal__cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal__titulo {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
}

.modal__fechar {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #64748b;
}

.modal__corpo {
  margin-bottom: 20px;
}

.campo-formulario {
  margin-bottom: 15px;
}

.campo-formulario label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #4a5568;
}

.campo-formulario input,
.campo-formulario select {
  width: 100%;
  padding: 10px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.campo-formulario input:focus,
.campo-formulario select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

.modal__rodape {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .gerenciamento {
    padding: 1.5rem;
    margin: 16px;
    margin-left: 16px;
    margin-top: 70px;
  }
  
  .gerenciamento__cabecalho {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .barra-pesquisa {
    flex-direction: column;
    align-items: stretch;
  }
  
  .acoes-wrapper {
    flex-wrap: wrap;
  }
}
</style>