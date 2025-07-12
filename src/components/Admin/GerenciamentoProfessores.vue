<template>
  <div class="gerenciamento">
    <!-- Botão e barra de pesquisa -->
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

    <!-- Tabela de professores -->
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
            <td>{{ professor.nome }}</td>
            <td>{{ professor.email }}</td>
            <td>
              <div class="acoes-wrapper">
                <button class="botao-icone botao-editar" @click="abrirModalProfessor(professor)">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="botao-icone botao-excluir" @click="confirmarExclusao(professor)">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button class="botao-icone botao-turmas" @click="selecionarProfessorParaTurma(professor)">
                  <i class="fas fa-chalkboard-teacher"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="loading" class="sem-resultados"><p>Carregando professores...</p></div>
      <div v-if="!loading && professores.length === 0" class="sem-resultados">
        <i class="fas fa-user-tie icone-vazio"></i>
        <p>Nenhum professor cadastrado</p>
      </div>
      <div v-else-if="!loading && professoresFiltrados.length === 0" class="sem-resultados">
        <i class="fas fa-search icone-vazio"></i>
        <p>Nenhum professor encontrado com o termo "{{ termoPesquisa }}"</p>
      </div>
    </div>

    <!-- Seção de turmas -->
    <!-- ... (mantém a mesma lógica da seção de turmas) ... -->

    <!-- Modal separado -->
    <ModalProfessor
      v-if="modalProfessorAberto"
      :professor="professorEditando"
      :visivel="modalProfessorAberto"
      @fechar="fecharModalProfessor"
      @salvar="salvarProfessor"
      v-model:form="professorLocal"
      :loading="loadingProfessor"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ModalProfessor from './ModalProfessor.vue'

export default {
  name: 'GerenciamentoProfessores',
  components: {
    ModalProfessor
  },
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
      return this.professores.filter(professor =>
        professor.nome.toLowerCase().includes(termo) || professor.email.toLowerCase().includes(termo)
      );
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
        const { data } = await axios.get('http://localhost:8000/api/usuarios/');
        this.professores = data.filter(p => p.tipo === 'professor');
      } catch (erro) {
        alert('Erro ao carregar professores');
      } finally {
        this.loading = false;
      }
    },
    async carregarTurmas() {
      try {
        const { data } = await axios.get('http://localhost:8000/api/turmas/');
        this.turmas = data;
      } catch (erro) {
        alert('Erro ao carregar turmas');
      }
    },
    abrirModalProfessor(professor) {
      this.professorEditando = professor;
      this.professorLocal = professor
        ? { nome: professor.nome, email: professor.email, senha: '', tipo: 'professor' }
        : { nome: '', email: '', senha: '', tipo: 'professor' };
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
          await axios.put(`http://localhost:8000/api/usuarios/${this.professorEditando.id}/`, {
            nome: this.professorLocal.nome,
            email: this.professorLocal.email,
            tipo: 'professor'
          });
        } else {
          await axios.post('http://localhost:8000/api/usuarios/', this.professorLocal);
        }
        await this.carregarProfessores();
        this.fecharModalProfessor();
        alert('Professor salvo com sucesso!');
      } catch (erro) {
        alert('Erro ao salvar professor.');
      } finally {
        this.loadingProfessor = false;
      }
    },
    confirmarExclusao(professor) {
      if (confirm(`Excluir professor ${professor.nome}?`)) {
        this.excluirProfessor(professor.id);
      }
    },
    async excluirProfessor(id) {
      try {
        await axios.delete(`http://localhost:8000/api/usuarios/${id}/`);
        await this.carregarProfessores();
        alert('Excluído com sucesso!');
      } catch (erro) {
        alert('Erro ao excluir professor.');
      }
    },
    selecionarProfessorParaTurma(professor) {
      this.professorSelecionadoParaTurma = professor;
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