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
                  <i class="fas fa-chalkboard-teacher"></i>
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
    <div class="secao-matriculas" v-if="alunoSelecionadoParaMatricula">
      <div class="cabecalho-secao">
        <h3 class="titulo-secao">Turmas do Aluno</h3>
        <button 
          class="botao-secundario" 
          @click="cancelarSelecaoAluno"
        >
          <i class="fas fa-times"></i>
          <span>Cancelar seleção</span>
        </button>
      </div>

      <div class="info-aluno">
        <span class="nome-aluno">{{ alunoSelecionadoParaMatricula.nome }}</span>
        <span class="id-aluno">Matrícula: {{ alunoSelecionadoParaMatricula.id }}</span>
      </div>

      <!-- Filtros -->
      <div class="filtros-matriculas">
        <select v-model="filtroPeriodo" class="campo-selecao">
          <option value="">Todos os períodos</option>
          <option v-for="periodo in periodosUnicos" :key="periodo" :value="periodo">
            {{ periodo }}
          </option>
        </select>
      </div>

      <!-- Tabela de matrículas -->
      <div class="tabela-wrapper">
        <table class="tabela">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nome</th>
              <th>Período</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="turma in turmasFiltradas" :key="turma.id">
              <td>{{ turma.codigo }}</td>
              <td>{{ turma.nome }}</td>
              <td>{{ turma.periodo }}</td>
              <td>
                <span :class="`status-badge ${getStatusMatricula(turma.id)}`">
                  {{ getStatusMatricula(turma.id) || 'Não matriculado' }}
                </span>
              </td>
              <td>
                <div class="acoes-wrapper">
                  <button 
                    class="botao-icone botao-desvincular"
                    @click="confirmarDesvincularTurma(turma)"
                    v-if="estaMatriculado(turma.id)"
                  >
                    <i class="fas fa-unlink"></i>
                  </button>
                  <button 
                    class="botao-icone botao-vincular"
                    @click="vincularAlunoATurma(turma)"
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
            <i class="fas fa-users-class icone-vazio"></i>
            <h3>Nenhuma turma encontrada</h3>
            <p v-if="filtroPeriodo">Não há turmas no período selecionado</p>
            <p v-else>Não encontramos turmas disponíveis</p>
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
      filtroPeriodo: '',
      modalAlunoAberto: false,
      alunoEditando: null,
      alunoSelecionadoParaMatricula: null
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
    turmasFiltradas() {
      let turmasFiltradas = this.turmas;
      
      // Filtrar por período se selecionado
      if (this.filtroPeriodo) {
        turmasFiltradas = turmasFiltradas.filter(t => t.periodo === this.filtroPeriodo);
      }
      
      // Ordenar turmas: primeiro as que já estão vinculadas ao aluno
      turmasFiltradas = [...turmasFiltradas].sort((a, b) => {
        const aVinculada = this.estaMatriculado(a.id);
        const bVinculada = this.estaMatriculado(b.id);
        
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
    estaMatriculado(turmaId) {
      return this.matriculas.some(m => 
        m.aluno === this.alunoSelecionadoParaMatricula?.id && 
        m.turma === turmaId
      )
    },
    getStatusMatricula(turmaId) {
      const matricula = this.matriculas.find(m => 
        m.aluno === this.alunoSelecionadoParaMatricula?.id && 
        m.turma === turmaId
      )
      return matricula?.status
    },
    async vincularAlunoATurma(turma) {
      if (!confirm(`Matricular ${this.alunoSelecionadoParaMatricula.nome} na turma ${turma.codigo} - ${turma.nome}?`)) {
        return
      }
      
      try {
        const dados = {
          aluno: this.alunoSelecionadoParaMatricula.id,
          turma: turma.id,
          status: 'ativo'
        }
        
        await axios.post('http://localhost:8000/api/matriculas/', dados)
        await this.carregarMatriculas()
        alert('Aluno matriculado com sucesso!')
      } catch (error) {
        console.error('Erro ao matricular aluno:', error)
        alert('Erro ao matricular aluno na turma')
      }
    },
    async confirmarDesvincularTurma(turma) {
      const matricula = this.matriculas.find(m => 
        m.aluno === this.alunoSelecionadoParaMatricula.id && 
        m.turma === turma.id
      )
      
      if (!matricula) return
      
      if (!confirm(`Remover ${this.alunoSelecionadoParaMatricula.nome} da turma ${turma.codigo} - ${turma.nome}?`)) {
        return
      }
      
      try {
        await axios.delete(`http://localhost:8000/api/matriculas/${matricula.id}/`)
        await this.carregarMatriculas()
        alert('Matrícula removida com sucesso!')
      } catch (error) {
        console.error('Erro ao remover matrícula:', error)
        alert('Erro ao remover matrícula')
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

.botao-vincular {
  background-color: #10b981;
}

.botao-desvincular {
  background-color: #f59e0b;
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

.info-aluno {
  background: #f8fafc;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
}

.nome-aluno {
  font-weight: 600;
  font-size: 16px;
}

.id-aluno {
  color: #64748b;
  font-size: 14px;
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

.fa-users-class {
  font-family: "Font Awesome 5 Free";
  font-weight: 900;
  content: "\f63d";
}

@media (max-width: 768px) {
  .gerenciamento {
    margin-left: 0;
    margin-top: 70px;
    padding: 15px;
  }
  
  .filtros-matriculas {
    flex-direction: column;
  }
  
  .campo-selecao {
    width: 100%;
  }
}
</style>