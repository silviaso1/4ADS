<template>
  <div class="portal-admin">
    <CabecalhoAdmin @logout="logout" />
    
    <div class="conteiner-principal">
      <MenuLateral 
        :aba-ativa="abaAtiva" 
        @mudar-aba="mudarAba"
      />
      
      <main class="conteudo-principal">
        <!-- Gerenciamento de Alunos -->
        <GerenciamentoAlunos 
          v-if="abaAtiva === 'alunos'"
          :alunos="alunos"
          @abrir-modal-aluno="abrirModalAluno"
          @confirmar-exclusao="confirmarExclusao"
        />
        
        <!-- Gerenciamento de Professores -->
        <GerenciamentoProfessores 
          v-if="abaAtiva === 'professores'"
          :professores="professores"
          @abrir-modal-professor="abrirModalProfessor"
          @confirmar-exclusao="confirmarExclusao"
        />
        
        <!-- Gerenciamento de Turmas -->
        <GerenciamentoTurmas 
          v-if="abaAtiva === 'turmas'"
          :turmas="turmas"
          :professores="professores"
          @abrir-modal-turma="abrirModalTurma"
          @confirmar-exclusao="confirmarExclusao"
        />
        
        <!-- Controle de Matrículas -->
        <ControleMatriculas
  v-model:matriculasAbertas="estadoMatriculas"
  :periodo-matriculas="periodoMatriculas"
  @salvar-periodo="salvarPeriodoMatriculas"
  @alternar-status="lidarComAlternanciaStatus"
/>
      </main>
    </div>
    
    <!-- Modais -->
    <ModalAluno
      v-if="mostrarModalAluno"
      :aluno="alunoEditando"
      @fechar="fecharModalAluno"
      @salvar="salvarAluno"
    />
    
    <ModalProfessor
      v-if="mostrarModalProfessor"
      :professor="professorEditando"
      @fechar="fecharModalProfessor"
      @salvar="salvarProfessor"
    />
    
    <ModalTurma
      v-if="mostrarModalTurma"
      :turma="turmaEditando"
      :professores="professores"
      @fechar="fecharModalTurma"
      @salvar="salvarTurma"
    />
    
    <ModalConfirmacao
      v-if="mostrarModalConfirmacao"
      :tipo="tipoExclusao"
      @cancelar="fecharModalConfirmacao"
      @confirmar="executarExclusao"
    />
  </div>
</template>

<script>
import CabecalhoAdmin from '../components/Admin/CabecalhoAdmin.vue'
import MenuLateral from '../components/Admin/MenuLateral.vue'
import GerenciamentoAlunos from '../components/Admin/GerenciamentoAlunos.vue'
import GerenciamentoProfessores from '../components/Admin/GerenciamentoProfessores.vue'
import GerenciamentoTurmas from '../components/Admin/GerenciamentoTurmas.vue'
import ControleMatriculas from '../components/Admin/ControleMatriculas.vue'
import ModalAluno from '../components/Admin/ModalAluno.vue'
import ModalProfessor from '../components/Admin/ModalProfessor.vue'
import ModalTurma from '../components/Admin/ModalTurma.vue'
import ModalConfirmacao from '../components/Admin/ModalConfirmacao.vue'

export default {
  name: 'PortalAdmin',
  components: {
    CabecalhoAdmin,
    MenuLateral,
    GerenciamentoAlunos,
    GerenciamentoProfessores,
    GerenciamentoTurmas,
    ControleMatriculas,
    ModalAluno,
    ModalProfessor,
    ModalTurma,
    ModalConfirmacao
  },
  data() {
    return {
      abaAtiva: 'alunos',
      matriculasAbertas: false,
      periodoMatriculas: {
        inicio: '2023-11-01',
        fim: '2023-11-15'
      },
      alunos: [
        { id: '2023001', nome: 'Ana Clara Souza', periodo: '2023.1' },
        { id: '2023002', nome: 'Bruno Oliveira', periodo: '2023.1' },
        { id: '2023003', nome: 'Carla Mendes', periodo: '2023.2' }
      ],
      professores: [
        { id: 't001', nome: 'Carlos Silva', email: 'carlos.silva@escola.com', senha: 'senha123' },
        { id: 't002', nome: 'Mariana Oliveira', email: 'mariana.oliveira@escola.com', senha: 'senha123' }
      ],
      turmas: [
        { 
          codigo: 'MAT-2023-1A', 
          nome: 'Matemática Avançada', 
          professorId: 't001',
          periodo: '2023.1',
          horario: 'Segunda e Quarta, 14:00-16:00',
          sala: 'Sala 203'
        }
      ],
      mostrarModalAluno: false,
      alunoEditando: null,
      mostrarModalProfessor: false,
      professorEditando: null,
      mostrarModalTurma: false,
      turmaEditando: null,
      mostrarModalConfirmacao: false,
      tipoExclusao: '',
      itemParaExcluir: null
    }
  },
  methods: {
    logout() {
      this.$router.push('/login')
    },
    mudarAba(aba) {
      this.abaAtiva = aba
    },
    abrirModalAluno(aluno) {
      this.alunoEditando = aluno ? { ...aluno } : null
      this.mostrarModalAluno = true
    },
    fecharModalAluno() {
      this.mostrarModalAluno = false
    },
    salvarAluno(aluno) {
      // Lógica para salvar aluno
    },
    abrirModalProfessor(professor) {
      this.professorEditando = professor ? { ...professor } : null
      this.mostrarModalProfessor = true
    },
    fecharModalProfessor() {
      this.mostrarModalProfessor = false
    },
    salvarProfessor(professor) {
      // Lógica para salvar professor
    },
    abrirModalTurma(turma) {
      this.turmaEditando = turma ? { ...turma } : null
      this.mostrarModalTurma = true
    },
    fecharModalTurma() {
      this.mostrarModalTurma = false
    },
    salvarTurma(turma) {
      // Lógica para salvar turma
    },
    confirmarExclusao(tipo, id) {
      this.tipoExclusao = tipo
      this.itemParaExcluir = id
      this.mostrarModalConfirmacao = true
    },
    fecharModalConfirmacao() {
      this.mostrarModalConfirmacao = false
    },
    executarExclusao() {
      // Lógica para exclusão
      this.mostrarModalConfirmacao = false
    },
    salvarPeriodoMatriculas(periodo) {
      this.periodoMatriculas = periodo
      // Lógica para salvar no backend
    },
    alternarStatusMatriculas() {
      this.matriculasAbertas = !this.matriculasAbertas
      // Lógica para atualizar no backend
    }
  }
}
</script>

<style lang="scss">
.portal-admin {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  background-color: #f8fafc;
  color: #2d3748;
  font-family: 'Inter', sans-serif;
}

.conteiner-principal {
  display: flex;
  flex: 1;
}

.conteudo-principal {
  flex: 1;
  padding: 2rem;
  background-color: #f8fafc;
  transition: all 0.3s ease;
}

/* Estilos para cards */
.card {
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  
  &-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #edf2f7;
    
    h2 {
      font-size: 1.25rem;
      font-weight: 600;
      color: #2d3748;
    }
  }
}

/* Botões */
.botao {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
  cursor: pointer;
  font-size: 0.875rem;
  
  &-primario {
    background-color: #3490dc;
    color: white;
    border: 1px solid #3490dc;
    
    &:hover {
      background-color: #2779bd;
    }
  }
  
  &-secundario {
    background-color: white;
    color: #4a5568;
    border: 1px solid #e2e8f0;
    
    &:hover {
      background-color: #f7fafc;
    }
  }
  
  &-perigo {
    background-color: #e3342f;
    color: white;
    border: 1px solid #e3342f;
    
    &:hover {
      background-color: #cc1f1a;
    }
  }
  
  &-icone {
    padding: 0.5rem;
    border-radius: 50%;
    width: 2rem;
    height: 2rem;
  }
}

/* Tabelas */
.tabela {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  
  thead {
    background-color: #f7fafc;
    color: #4a5568;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  
  th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
  }
  
  td {
    padding: 1rem;
    border-top: 1px solid #edf2f7;
    color: #4a5568;
  }
  
  tr:hover {
    background-color: #f8fafc;
  }
}

/* Formulários */
.campo-formulario {
  margin-bottom: 1.25rem;
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    color: #4a5568;
  }
  
  input, select {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #e2e8f0;
    border-radius: 0.5rem;
    background-color: white;
    transition: all 0.2s;
    
    &:focus {
      outline: none;
      border-color: #3490dc;
      box-shadow: 0 0 0 3px rgba(52, 144, 220, 0.1);
    }
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .conteiner-principal {
    flex-direction: column;
  }
  
  .conteudo-principal {
    padding: 1rem;
  }
  
  .tabela {
    display: block;
    overflow-x: auto;
  }
}
</style>