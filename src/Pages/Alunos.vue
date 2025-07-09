<template>
  <div class="portal-aluno">
    <CabecalhoPortal 
      :nome="aluno.nome" 
      :matricula="aluno.id" 
      @logout="logout"
      @toggle-menu="toggleBarraLateral"
    />
    
    <div class="container-portal">
      <BarraLateral 
        :selecaoAtual="selecaoAtual"
        :mostrarMobile="mostrarBarraMobile"
        @mudar-selecao="mudarSelecao"
      />
      
      <main class="conteudo-portal" :class="{ 'menu-aberto': mostrarBarraMobile }">
        <DisciplinasAndamento 
          v-if="selecaoAtual === 'andamento'"
          :disciplinas="disciplinasEmAndamento"
        />
        
        <DisciplinasConcluidas 
          v-if="selecaoAtual === 'concluidas'"
          :disciplinas="disciplinasConcluidas"
        />
        
        <MatriculaDisciplinas
          v-if="selecaoAtual === 'matricula' && periodoMatriculaAberto"
          :disciplinasDisponiveis="disciplinasDisponiveis"
          @matricular="abrirModalMatricula"
          @atualizar="carregarDisciplinasDisponiveis"
        />
        
     
      </main>
    </div>
    
 
  </div>
</template>

<script>
import CabecalhoPortal from '../components/Aluno/CabecalhoPortal.vue'
import BarraLateral from '../components/Aluno/BarraLateral.vue'
import DisciplinasAndamento from '../components/Aluno/DisciplinasAndamento.vue'
import DisciplinasConcluidas from '../components/Aluno/DisciplinasConcluidas.vue'
import MatriculaDisciplinas from '../components/Aluno/MatriculaDisciplinas.vue'

export default {
  name: 'PortalAluno',
  components: {
    CabecalhoPortal,
    BarraLateral,
    DisciplinasAndamento,
    DisciplinasConcluidas,
    MatriculaDisciplinas,
  },
  data() {
    return {
      selecaoAtual: 'andamento',
      mostrarBarraMobile: false,
      mostrarModalMatricula: false,
      disciplinaSelecionada: null,
      periodoMatriculaAberto: true,
      aluno: {
        id: '2023001',
        nome: 'Ana Clara Souza',
        email: 'ana.souza@email.com'
      },
      disciplinasMatriculadas: [
        {
          codigo: 'MAT-2023-1A',
          nome: 'Matemática Avançada',
          professor: 'Carlos Silva',
          horario: 'Segunda e Quarta, 14:00-16:00',
          sala: 'Sala 203',
          notas: { av1: 7.5, av2: 8.0, avf: null },
          mediaFinal: 7.8,
          status: 'aprovado'
        },
        {
          codigo: 'FIS-2023-1B',
          nome: 'Física Básica',
          professor: 'Mariana Oliveira',
          horario: 'Terça e Quinta, 10:00-12:00',
          sala: 'Laboratório 105',
          notas: { av1: 5.0, av2: 4.5, avf: 6.0 },
          mediaFinal: 5.2,
          status: 'reprovado'
        },
        {
          codigo: 'PRO-2023-1C',
          nome: 'Programação I',
          professor: 'Ricardo Mendes',
          horario: 'Sexta, 08:00-12:00',
          sala: 'Laboratório 201',
          notas: { av1: 6.5, av2: null, avf: null },
          mediaFinal: 6.5,
          status: 'cursando'
        }
      ],
      disciplinasDisponiveis: []
    }
  },
  computed: {
    disciplinasEmAndamento() {
      return this.disciplinasMatriculadas.filter(d => d.status === 'cursando')
    },
    disciplinasConcluidas() {
      return this.disciplinasMatriculadas.filter(d => d.status !== 'cursando')
    }
  },
  methods: {
    mudarSelecao(novaSelecao) {
      this.selecaoAtual = novaSelecao
      this.mostrarBarraMobile = false
    },
    toggleBarraLateral() {
      this.mostrarBarraMobile = !this.mostrarBarraMobile
    },
    logout() {
      this.$router.push('/login')
    },
    carregarDisciplinasDisponiveis() {
      // Simulação de API
      this.disciplinasDisponiveis = [
        {
          codigo: 'BDA-2023-2A',
          nome: 'Banco de Dados',
          professor: 'Fernanda Costa',
          horario: 'Segunda e Quarta, 14:00-16:00',
          sala: 'Sala 205'
        },
        {
          codigo: 'RED-2023-2B',
          nome: 'Redes de Computadores',
          professor: 'Lucas Pereira',
          horario: 'Terça e Quinta, 16:00-18:00',
          sala: 'Laboratório 107'
        }
      ].filter(disciplina => 
        !this.disciplinasMatriculadas.some(d => 
          d.codigo === disciplina.codigo && d.status === 'aprovado'
        )
      )
    },
    abrirModalMatricula(disciplina) {
      this.disciplinaSelecionada = disciplina
      this.mostrarModalMatricula = true
    },
    fecharModalMatricula() {
      this.mostrarModalMatricula = false
    },
    confirmarMatricula() {
      const novaDisciplina = {
        ...this.disciplinaSelecionada,
        notas: { av1: null, av2: null, avf: null },
        mediaFinal: 0,
        status: 'cursando'
      }
      this.disciplinasMatriculadas.push(novaDisciplina)
      this.mostrarModalMatricula = false
      this.$toast.success(`Matrícula em ${novaDisciplina.nome} realizada!`)
      this.carregarDisciplinasDisponiveis()
    }
  },
  created() {
    this.carregarDisciplinasDisponiveis()
  }
}
</script>

<style scoped>
.portal-aluno {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container-portal {
  display: flex;
  flex: 1;
  width: 100%;
  position: relative;
}

.conteudo-portal {
  flex: 1;
  padding: 30px;
  background-color: #f5f7fa;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
}

.conteudo-portal.menu-aberto {
  margin-left: 250px;
}

@media (max-width: 992px) {
  .conteudo-portal {
    margin-left: 0;
    padding: 20px;
  }
  
  .conteudo-portal.menu-aberto {
    margin-left: 250px;
  }
}

@media (max-width: 768px) {
  .conteudo-portal.menu-aberto {
    margin-left: 0;
    transform: translateX(250px);
  }
}
</style>