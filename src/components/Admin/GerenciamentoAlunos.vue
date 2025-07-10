<template>
  <div class="gerenciamento">
    <div class="gerenciamento__cabecalho">
      <button class="botao-primario" @click="abrirModalAluno(null)">
        <i class="fas fa-plus"></i>
        <span>Novo Aluno</span>
      </button>
    </div>
    
    <div class="barra-pesquisa">
      <i class="fas fa-search icone-pesquisa"></i>
      <input
        type="text"
        class="campo-pesquisa"
        placeholder="Pesquisar alunos por nome, matrícula ou período..."
        v-model="termoPesquisa"
      >
      <div class="contador-resultados">
        {{ alunosFiltrados.length }} {{ alunosFiltrados.length === 1 ? 'aluno encontrado' : 'alunos encontrados' }}
      </div>
    </div>
    
    <div class="tabela-wrapper">
      <table class="tabela">
        <thead>
          <tr>
            <th class="coluna-id">Matrícula</th>
            <th class="coluna-nome">Nome Completo</th>
            <th class="coluna-email">Email</th>
            <th class="coluna-acoes">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="aluno in alunosFiltrados" :key="aluno.id">
            <td class="coluna-id">{{ aluno.id }}</td>
            <td class="coluna-nome">{{ aluno.nome }}</td>
            <td class="coluna-email">{{ aluno.email }}</td>
            <td class="coluna-acoes">
              <div class="acoes-wrapper">
                <button class="botao-icone botao-editar" @click="abrirModalAluno(aluno)">
                  <i class="fas fa-edit"></i>
                </button>
                <button class="botao-icone botao-excluir" @click="confirmarExclusao(aluno)">
                  <i class="fas fa-trash-alt"></i>
                </button>
                <button class="botao-icone botao-turmas" @click="selecionarAlunoParaMatricula(aluno)">
                  <i class="fas fa-users-class"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="alunosFiltrados.length === 0" class="sem-resultados">
        <div class="empty-state">
          <i class="fas fa-user-graduate icone-vazio"></i>
          <h3>Nenhum aluno encontrado</h3>
          <p>Não encontramos resultados para sua pesquisa.</p>
          <button class="botao-primario" @click="abrirModalAluno(null)">
            <i class="fas fa-plus"></i>
            Adicionar Aluno
          </button>
        </div>
      </div>
    </div>

    <!-- Seção de Matrículas em Turmas -->
    <div class="secao-matriculas">
      <div class="cabecalho-secao">
        <h3 class="titulo-secao">Matrículas em Turmas</h3>
        <button 
          class="botao-primario" 
          @click="abrirModalMatricula(null)"
          v-if="!alunoSelecionadoParaMatricula"
        >
          <i class="fas fa-plus"></i>
          <span>Nova Matrícula</span>
        </button>
        <button 
          class="botao-secundario" 
          @click="cancelarSelecaoAluno"
          v-else
        >
          <i class="fas fa-times"></i>
          <span>Cancelar seleção</span>
        </button>
      </div>

      <!-- Filtros -->
      <div class="filtros-matriculas">
        <select v-model="filtroTurma" class="campo-selecao">
          <option value="">Todas as turmas</option>
          <option v-for="turma in turmas" :key="turma.id" :value="turma.id">
            {{ turma.codigo }} - {{ turma.nome }}
          </option>
        </select>
        <select v-model="filtroStatus" class="campo-selecao">
          <option value="">Todos os status</option>
          <option value="ativo">Ativo</option>
          <option value="inativo">Inativo</option>
          <option value="trancado">Trancado</option>
        </select>
      </div>

      <!-- Botão especial para vincular aluno selecionado -->
      <div class="aluno-selecionado" v-if="alunoSelecionadoParaMatricula">
        <div class="info-aluno">
          <span class="nome-aluno">{{ alunoSelecionadoParaMatricula.nome }}</span>
          <span class="id-aluno">ID: {{ alunoSelecionadoParaMatricula.id }}</span>
        </div>
        <button 
          class="botao-primario botao-vincular"
          @click="abrirModalMatricula(alunoSelecionadoParaMatricula)"
        >
          <i class="fas fa-link"></i>
          <span>Vincular à Turma</span>
        </button>
      </div>

      <!-- Tabela de matrículas -->
      <div class="tabela-wrapper">
        <table class="tabela">
          <thead>
            <tr>
              <th>Aluno</th>
              <th>Turma</th>
              <th>Status</th>
              <th>Média Final</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="matricula in matriculasFiltradas" :key="matricula.id">
              <td>{{ getNomeAluno(matricula.aluno) }}</td>
              <td>{{ getDescricaoTurma(matricula.turma) }}</td>
              <td>
                <span :class="`status-badge ${matricula.status}`">
                  {{ matricula.status }}
                </span>
              </td>
              <td>{{ matricula.media_final || '-' }}</td>
              <td>
                <div class="acoes-wrapper">
                  <button class="botao-icone botao-editar" @click="abrirModalMatriculaEdicao(matricula)">
                    <i class="fas fa-edit"></i>
                  </button>
                  <button class="botao-icone botao-excluir" @click="confirmarExclusaoMatricula(matricula)">
                    <i class="fas fa-trash-alt"></i>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-if="matriculasFiltradas.length === 0" class="sem-resultados">
          <div class="empty-state">
            <i class="fas fa-users-class icone-vazio"></i>
            <h3>Nenhuma matrícula encontrada</h3>
            <p>Não encontramos resultados para sua pesquisa.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Aluno -->
    <ModalAluno
      v-if="modalAlunoAberto"
      :aluno="alunoEditando"
      @fechar="fecharModalAluno"
      @salvar="salvarAluno"
    />

    <!-- Modal Matrícula -->
    <div v-if="modalMatriculaAberto" class="modal-overlay" @click.self="fecharModalMatricula">
      <div class="modal">
        <div class="modal__cabecalho">
          <h3 class="modal__titulo">
            {{ matriculaEditando ? 'Editar Matrícula' : 'Cadastrar Aluno na Turma' }}
          </h3>
          <button class="modal__fechar" @click="fecharModalMatricula">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <div class="modal__corpo">
          <!-- Aluno (automático quando selecionado da tabela) -->
          <div class="campo-formulario" v-if="alunoSelecionadoParaMatricula">
            <label>Aluno:</label>
            <div class="aluno-info-modal">
              <span class="nome">{{ alunoSelecionadoParaMatricula.nome }}</span>
              <span class="matricula">Matrícula: {{ alunoSelecionadoParaMatricula.id }}</span>
            </div>
            <input type="hidden" v-model="matriculaLocal.aluno">
          </div>

          <!-- Selecione a turma -->
          <div class="campo-formulario">
            <label for="turmaMatricula">Turma *</label>
            <select 
              id="turmaMatricula" 
              v-model="matriculaLocal.turma" 
              class="campo-selecao"
              required
            >
              <option value="">Selecione uma turma</option>
              <option 
                v-for="turma in turmas" 
                :key="turma.id" 
                :value="turma.id"
              >
                {{ turma.codigo }} - {{ turma.nome }} ({{ turma.periodo }})
              </option>
            </select>
          </div>

          <!-- Status -->
          <div class="campo-formulario">
            <label for="statusMatricula">Status *</label>
            <select 
              id="statusMatricula" 
              v-model="matriculaLocal.status" 
              class="campo-selecao"
              required
            >
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
              <option value="trancado">Trancado</option>
            </select>
          </div>

          <!-- Média (opcional) -->
          <div class="campo-formulario">
            <label for="mediaMatricula">Média Final</label>
            <input
              id="mediaMatricula"
              type="number"
              v-model="matriculaLocal.media_final"
              min="0"
              max="10"
              step="0.1"
              placeholder="0.0 a 10.0"
            >
          </div>
        </div>

        <div class="modal__rodape">
          <button class="botao-secundario" @click="fecharModalMatricula">
            Cancelar
          </button>
          <button 
            class="botao-primario" 
            @click="salvarMatricula" 
            :disabled="!matriculaLocal.turma || loadingMatricula"
          >
            <i class="fas fa-save"></i>
            {{ loadingMatricula ? 'Salvando...' : 'Salvar Matrícula' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ModalAluno from './ModalAluno.vue'

export default {
  components: {
    ModalAluno
  },
  data() {
    return {
      termoPesquisa: '',
      alunos: [],
      matriculas: [],
      turmas: [],
      filtroTurma: '',
      filtroStatus: '',
      modalAlunoAberto: false,
      alunoEditando: null,
      modalMatriculaAberto: false,
      matriculaEditando: null,
      alunoSelecionadoParaMatricula: null,
      matriculaLocal: {
        aluno: '',
        turma: '',
        status: 'ativo',
        media_final: null
      },
      loadingMatricula: false
    }
  },
  computed: {
    alunosFiltrados() {
      return this.alunos.filter(aluno => {
        return aluno.tipo === 'aluno' && (
          aluno.id.toString().includes(this.termoPesquisa) ||
          aluno.nome.toLowerCase().includes(this.termoPesquisa.toLowerCase()) ||
          aluno.email.toLowerCase().includes(this.termoPesquisa.toLowerCase())
        )
      })
    },
    matriculasFiltradas() {
      return this.matriculas.filter(matricula => {
        const turmaMatch = this.filtroTurma ? matricula.turma == this.filtroTurma : true
        const statusMatch = this.filtroStatus ? matricula.status === this.filtroStatus : true
        return turmaMatch && statusMatch
      })
    }
  },
  created() {
    this.carregarAlunos()
    this.carregarMatriculas()
    this.carregarTurmas()
  },
  methods: {
    async carregarAlunos() {
      try {
        const response = await axios.get('http://localhost:8000/api/usuarios/')
        this.alunos = response.data
      } catch (error) {
        console.error('Erro ao carregar alunos:', error)
        alert('Erro ao carregar alunos')
      }
    },
    async carregarMatriculas() {
      try {
        const response = await axios.get('http://localhost:8000/api/matriculas/')
        this.matriculas = response.data
      } catch (error) {
        console.error('Erro ao carregar matrículas:', error)
        alert('Erro ao carregar matrículas')
      }
    },
    async carregarTurmas() {
      try {
        const response = await axios.get('http://localhost:8000/api/turmas/')
        this.turmas = response.data
      } catch (error) {
        console.error('Erro ao carregar turmas:', error)
        alert('Erro ao carregar turmas')
      }
    },
    getNomeAluno(id) {
      const aluno = this.alunos.find(a => a.id == id)
      return aluno ? aluno.nome : 'Aluno não encontrado'
    },
    getDescricaoTurma(id) {
      const turma = this.turmas.find(t => t.id == id)
      return turma ? `${turma.codigo} - ${turma.nome}` : 'Turma não encontrada'
    },
    abrirModalAluno(aluno) {
      this.alunoEditando = aluno
      this.modalAlunoAberto = true
    },
    fecharModalAluno() {
      this.modalAlunoAberto = false
      this.alunoEditando = null
    },
    async salvarAluno(aluno) {
      try {
        if (aluno.id) {
          await axios.put(`http://localhost:8000/api/usuarios/${aluno.id}/`, aluno)
        } else {
          await axios.post('http://localhost:8000/api/usuarios/', aluno)
        }
        await this.carregarAlunos()
        this.fecharModalAluno()
      } catch (error) {
        console.error('Erro ao salvar aluno:', error)
        alert('Erro ao salvar aluno')
      }
    },
    confirmarExclusao(aluno) {
      if (confirm(`Excluir aluno ${aluno.nome}?`)) {
        this.excluirAluno(aluno.id)
      }
    },
    async excluirAluno(id) {
      try {
        await axios.delete(`http://localhost:8000/api/usuarios/${id}/`)
        await this.carregarAlunos()
      } catch (error) {
        console.error('Erro ao excluir aluno:', error)
        alert('Erro ao excluir aluno')
      }
    },
    selecionarAlunoParaMatricula(aluno) {
      this.alunoSelecionadoParaMatricula = aluno
      window.scrollTo({
        top: document.querySelector('.secao-matriculas').offsetTop,
        behavior: 'smooth'
      })
    },
    cancelarSelecaoAluno() {
      this.alunoSelecionadoParaMatricula = null
    },
    abrirModalMatricula(aluno = null) {
      if (aluno) {
        this.alunoSelecionadoParaMatricula = aluno
        this.matriculaLocal = {
          aluno: aluno.id,
          turma: '',
          status: 'ativo',
          media_final: null
        }
      }
      this.modalMatriculaAberto = true
      this.matriculaEditando = null
    },
    abrirModalMatriculaEdicao(matricula) {
      this.alunoSelecionadoParaMatricula = this.alunos.find(a => a.id == matricula.aluno)
      this.matriculaEditando = matricula
      this.matriculaLocal = { ...matricula }
      this.modalMatriculaAberto = true
    },
    fecharModalMatricula() {
      this.modalMatriculaAberto = false
      this.matriculaEditando = null
      this.alunoSelecionadoParaMatricula = null
    },
    async salvarMatricula() {
      if (!this.matriculaLocal.turma) {
        alert('Selecione uma turma')
        return
      }

      this.loadingMatricula = true

      try {
        const dados = {
          aluno: this.matriculaLocal.aluno,
          turma: Number(this.matriculaLocal.turma),
          status: this.matriculaLocal.status,
          media_final: this.matriculaLocal.media_final ? 
            parseFloat(this.matriculaLocal.media_final) : null
        }

        if (this.matriculaEditando) {
          await axios.put(`http://localhost:8000/api/matriculas/${this.matriculaEditando.id}/`, dados)
        } else {
          await axios.post('http://localhost:8000/api/matriculas/', dados)
        }

        await this.carregarMatriculas()
        this.fecharModalMatricula()
        alert('Matrícula salva com sucesso!')
      } catch (error) {
        console.error('Erro ao salvar matrícula:', error.response?.data || error)
        alert('Erro ao salvar matrícula: ' + 
          (error.response?.data ? JSON.stringify(error.response.data) : error.message))
      } finally {
        this.loadingMatricula = false
      }
    },
    confirmarExclusaoMatricula(matricula) {
      if (confirm(`Excluir matrícula de ${this.getNomeAluno(matricula.aluno)} na turma ${this.getDescricaoTurma(matricula.turma)}?`)) {
        this.excluirMatricula(matricula.id)
      }
    },
    async excluirMatricula(id) {
      try {
        await axios.delete(`http://localhost:8000/api/matriculas/${id}/`)
        await this.carregarMatriculas()
      } catch (error) {
        console.error('Erro ao excluir matrícula:', error)
        alert('Erro ao excluir matrícula')
      }
    }
  }
}
</script>

<style scoped>
.gerenciamento {
  margin-left: 250px;
  margin-top: 80px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.gerenciamento__cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.barra-pesquisa {
  position: relative;
  margin-bottom: 20px;
}

.icone-pesquisa {
  position: absolute;
  left: 10px;
  top: 10px;
  color: #718096;
}

.campo-pesquisa {
  width: 100%;
  padding: 10px 10px 10px 35px;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 14px;
}

.contador-resultados {
  font-size: 12px;
  color: #718096;
  margin-top: 5px;
}

.tabela-wrapper {
  overflow-x: auto;
  margin-bottom: 30px;
}

.tabela {
  width: 100%;
  border-collapse: collapse;
}

.tabela th {
  background-color: #f8fafc;
  padding: 12px 15px;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  border-bottom: 2px solid #e2e8f0;
}

.tabela td {
  padding: 12px 15px;
  border-bottom: 1px solid #edf2f7;
  color: #4a5568;
}

.tabela tr:hover {
  background-color: #f8fafc;
}

.acoes-wrapper {
  display: flex;
  gap: 8px;
}

.botao-icone {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: none;
  color: white;
}

.botao-editar {
  background-color: #3b82f6;
}

.botao-excluir {
  background-color: #ef4444;
}

.botao-turmas {
  background-color: #8b5cf6;
}

.sem-resultados {
  padding: 30px;
  text-align: center;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
}

.icone-vazio {
  font-size: 50px;
  color: #e2e8f0;
  margin-bottom: 15px;
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

.botao-primario:hover {
  background: #1d4ed8;
}

.botao-secundario {
  background: #e2e8f0;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.botao-secundario:hover {
  background: #cbd5e0;
}

/* Seção de Matrículas */
.secao-matriculas {
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

.filtros-matriculas {
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

.aluno-selecionado {
  background: #f8fafc;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #e2e8f0;
}

.info-aluno {
  display: flex;
  flex-direction: column;
}

.nome-aluno {
  font-weight: 600;
  font-size: 16px;
}

.id-aluno {
  color: #64748b;
  font-size: 14px;
}

.botao-vincular {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-badge {
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  text-transform: capitalize;
}

.status-badge.ativo {
  background-color: #dcfce7;
  color: #166534;
}

.status-badge.inativo {
  background-color: #fee2e2;
  color: #991b1b;
}

.status-badge.trancado {
  background-color: #fef3c7;
  color: #92400e;
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

.aluno-info-modal {
  background: #f8fafc;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

.aluno-info-modal .nome {
  font-weight: 600;
  display: block;
  margin-bottom: 4px;
}

.aluno-info-modal .matricula {
  color: #64748b;
  font-size: 14px;
}

.modal__rodape {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.fa-users-class {
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  content: "\f63d";
}
</style>