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
import axios from 'axios'

import CabecalhoAdmin from '../components/Admin/CabecalhoAdmin.vue'
import MenuLateral from '../components/Admin/MenuLateral.vue'
import GerenciamentoAlunos from '../components/Admin/GerenciamentoAlunos.vue'
import GerenciamentoProfessores from '../components/Admin/GerenciamentoProfessores.vue'
import GerenciamentoTurmas from '../components/Admin/GerenciamentoTurmas.vue'
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
    ModalAluno,
    ModalProfessor,
    ModalTurma,
    ModalConfirmacao
  },
  data() {
    return {
      abaAtiva: 'alunos',
      alunos: [
        { id: '2023001', matricula: '2023001', periodo_ingresso: '2023.1', nome: 'Ana Clara Souza' },
        { id: '2023002', matricula: '2023002', periodo_ingresso: '2023.1', nome: 'Bruno Oliveira' },
        { id: '2023003', matricula: '2023003', periodo_ingresso: '2023.2', nome: 'Carla Mendes' }
      ],
      professores: [], // Vazio, será carregado via API
      turmas: [
        { 
          id: 1,
          codigo: 'MAT-2023-1A', 
          nome: 'Matemática Avançada', 
          professor_id: 't001',
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
    async salvarAluno(aluno) {
      try {
        const token = '039158ff2f7056df4a2d999c925afb79ee3cc8e0'
        const url = 'http://localhost:8000/api/alunos/'

        if (aluno.id && this.alunos.some(a => a.id === aluno.id)) {
          // Atualizar aluno (PUT)
          await axios.put(`${url}${aluno.id}`, aluno, {
            headers: { Authorization: `Bearer ${token}` }
          })

          // Atualiza lista local
          const index = this.alunos.findIndex(a => a.id === aluno.id)
          if (index >= 0) this.alunos.splice(index, 1, aluno)

          alert('Aluno atualizado com sucesso!')
        } else {
          // Criar novo aluno (POST)
          await axios.post(url, aluno, {
            headers: { Authorization: `Bearer ${token}` }
          })

          this.alunos.push(aluno)
          alert('Aluno cadastrado com sucesso!')
        }

        this.mostrarModalAluno = false
      } catch (error) {
        console.error('Erro ao salvar aluno:', error)
        alert('Falha ao salvar aluno. Veja o console para mais detalhes.')
      }
    },
    abrirModalProfessor(professor) {
      this.professorEditando = professor ? { ...professor } : null
      this.mostrarModalProfessor = true
    },
    fecharModalProfessor() {
      this.mostrarModalProfessor = false
    },
    salvarProfessor(professor) {
      // Implemente lógica para salvar professor
    },
    abrirModalTurma(turma) {
      this.turmaEditando = turma ? { ...turma } : {
        codigo: '',
        nome: '',
        professor_id: '',
        periodo: '',
        horario: '',
        sala: ''
      }
      this.mostrarModalTurma = true
    },
    fecharModalTurma() {
      this.mostrarModalTurma = false
    },
    salvarTurma(turma) {
      if (turma.id) {
        // Editar turma existente
        const index = this.turmas.findIndex(t => t.id === turma.id)
        if (index >= 0) {
          this.turmas.splice(index, 1, turma)
        }
      } else {
        // Criar nova turma - gerar id simples para exemplo
        turma.id = this.turmas.length + 1
        this.turmas.push(turma)
      }
      this.mostrarModalTurma = false
      alert('Turma salva com sucesso!')
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
      // Implementar lógica de exclusão conforme tipo e id
      this.mostrarModalConfirmacao = false
    },

    async carregarProfessores() {
      try {
        const token = '039158ff2f7056df4a2d999c925afb79ee3cc8e0' // ou sem token se não usar
        const url = 'http://localhost:8000/api/usuarios/'

        const response = await axios.get(url, {
          headers: { Authorization: `Bearer ${token}` }
        })
        // Filtra só os professores
        this.professores = response.data.filter(usuario => usuario.tipo === 'professor')
          .map(prof => ({
            id: prof.id,
            nome: prof.nome,
            email: prof.email
          }))
      } catch (error) {
        console.error('Erro ao carregar professores:', error)
        alert('Erro ao carregar lista de professores')
      }
    }
  },
  mounted() {
    this.carregarProfessores()
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
</style>
