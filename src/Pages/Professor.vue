<template>
  <div class="portal-professor">
    <CabecalhoProfessor @sair="sair" />

    <div class="conteiner-principal">
      <main class="conteudo-principal">
        <div v-if="carregando" class="carregando">
          <i class="fas fa-spinner fa-spin"></i> Carregando turmas...
        </div>

        <div v-else-if="!turmaSelecionada && turmasDoProfessor.length === 0" class="sem-turmas">
          Nenhuma turma encontrada para este professor.
        </div>

        <ListaTurmas 
          v-else-if="!turmaSelecionada"
          :turmas="turmasDoProfessor"
          @selecionar-turma="selecionarTurma"
        />

        <DetalhesTurma 
          v-else 
          :turma-id="turmaSelecionada.id" 
          @voltar="turmaSelecionada = null"
        />
      </main>
    </div>
  </div>
</template>

<script>
import CabecalhoProfessor from '../components/Professor/CabecalhoProfessor.vue'
import ListaTurmas from '../components/Professor/ListaTurmas.vue'
import DetalhesTurma from '../components/Professor/DetalhesTurma.vue'
import axios from 'axios'

export default {
  name: 'PortalProfessor',
  components: {
    CabecalhoProfessor,
    ListaTurmas,
    DetalhesTurma
  },
  data() {
    return {
      professorId: null,
      turmasDoProfessor: [],
      carregando: true,
      turmaSelecionada: null,
      token: '7df63d4afaf58b6290be34677ef7ff7abc21bfff' // token de teste
    }
  },
  created() {
    this.professorId = localStorage.getItem('professorId') || sessionStorage.getItem('professorId')
    if (!this.professorId) {
      alert('Sessão expirada. Faça login novamente.')
      this.$router.push('/login')
      return
    }

    this.carregarTurmasDoProfessor()
  },
  methods: {
    async carregarTurmasDoProfessor() {
      this.carregando = true
      try {
        const response = await axios.get('http://localhost:8000/api/turmas/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        this.turmasDoProfessor = response.data.filter(turma => 
          turma.professor && turma.professor.toString() === this.professorId.toString()
        )
      } catch (error) {
        alert('Erro ao carregar turmas: ' + (error.response?.data?.message || error.message))
      } finally {
        this.carregando = false
      }
    },
    selecionarTurma(turma) {
      this.turmaSelecionada = turma
    },
    sair() {
      localStorage.removeItem('professorId')
      sessionStorage.removeItem('professorId')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.portal-professor {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.conteiner-principal {
  display: flex;
  flex: 1;
}

.conteudo-principal {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}

.carregando, .sem-turmas {
  text-align: center;
  padding: 40px;
  font-size: 18px;
  color: #666;
}

.fa-spinner {
  margin-right: 10px;
}
</style>
