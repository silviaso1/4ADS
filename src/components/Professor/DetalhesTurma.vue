<template>
  <div class="detalhes-turma-container" v-if="turma">
    <!-- Header com efeito de gradiente -->
    <div class="turma-header">
      <button @click="$emit('voltar')" class="voltar-btn floating-btn">
        <i class="fas fa-arrow-left"></i>
      </button>
      <div class="header-content">
        <h1>{{ turma.nome }}</h1>
        <div class="turma-meta">
          <span class="turma-codigo">{{ turma.codigo }}</span>
          <span class="turma-periodo">{{ turma.periodo }}</span>
        </div>
      </div>
    </div>

    <!-- Cards flutuantes com informações -->
    <div class="info-cards">
      <div class="info-card">
        <i class="fas fa-clock"></i>
        <div>
          <h3>Horário</h3>
          <p>{{ turma.horario || 'Não informado' }}</p>
        </div>
      </div>
      <div class="info-card">
        <i class="fas fa-door-open"></i>
        <div>
          <h3>Sala</h3>
          <p>{{ turma.sala || 'Não informada' }}</p>
        </div>
      </div>
    </div>

    <!-- Atividades -->
    <div class="atividades-section">
      <div class="section-header">
        <h2><i class="fas fa-tasks"></i> Atividades</h2>
        <button @click="abrirModalNotas" class="add-button">
          <i class="fas fa-plus-circle"></i> Lançar Notas
        </button>
      </div>
      <div class="atividades-grid">
        <div v-for="atividade in atividades" :key="atividade.id" class="atividade-card">
          <div class="atividade-icon"><i class="fas fa-clipboard-check"></i></div>
          <h3>{{ atividade.nome }}</h3>
        </div>
      </div>
    </div>

    <!-- Alunos -->
    <div class="alunos-section">
      <h2><i class="fas fa-users"></i> Alunos Matriculados</h2>
      <ul>
        <li v-for="aluno in alunosMatriculados" :key="aluno.id">
          {{ aluno.nome }} ({{ aluno.email }})
        </li>
      </ul>
    </div>

    <!-- Modal -->
    <ModalNotas 
      v-if="exibirModalNotas"
      :alunos="alunosMatriculados"
      :atividades="atividades"
      @fechar="exibirModalNotas = false"
      @salvar="salvarNotas"
    />
  </div>
</template>

<script>
import axios from 'axios'
import ModalNotas from './ModalNotas.vue'

export default {
  name: 'DetalhesTurma',
  components: { ModalNotas },
  props: {
    turmaId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      turma: null,
      atividades: [],
      exibirModalNotas: false,
      usuarios: [],
      matriculas: []
    }
  },
  computed: {
    alunosMatriculados() {
      const alunos = this.usuarios.filter(u => u.tipo === 'aluno')
      const matriculasTurma = this.matriculas.filter(m => m.turma === this.turmaId)

      return alunos.filter(aluno =>
        matriculasTurma.some(m => m.aluno === aluno.id)
      )
    }
  },
  async created() {
    await this.carregarDados()
  },
  methods: {
    async carregarDados() {
      try {
        const [turmaRes, usuariosRes, matriculasRes] = await Promise.all([
          axios.get(`http://localhost:8000/api/turmas/${this.turmaId}/`),
          axios.get('http://localhost:8000/api/usuarios/'),
          axios.get('http://localhost:8000/api/matriculas/')
        ])
        this.turma = turmaRes.data
        this.usuarios = usuariosRes.data
        this.matriculas = matriculasRes.data

        // Simulando atividades fixas
        this.atividades = [
          { id: 1, nome: 'Prova 1' },
          { id: 2, nome: 'Trabalho Final' }
        ]
      } catch (error) {
        console.error('Erro ao carregar dados:', error)
        alert('Erro ao carregar turma ou alunos.')
      }
    },
    abrirModalNotas() {
      this.exibirModalNotas = true
    },
    salvarNotas(dados) {
      console.log('Notas salvas:', dados)
    }
  }
}
</script>




<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.detalhes-turma-container {
  font-family: 'Poppins', sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 40px;
}

/* Header estilizado */
.turma-header {
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  color: white;
  padding: 40px 30px 80px;
  border-radius: 0 0 20px 20px;
  position: relative;
  margin-bottom: 60px;
  box-shadow: 0 10px 30px rgba(41, 128, 185, 0.3);
}

.header-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.turma-header h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  font-weight: 600;
}

.turma-meta {
  display: flex;
  justify-content: center;
  gap: 20px;
  font-size: 1.1rem;
}

.turma-codigo {
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 15px;
  border-radius: 20px;
}

/* Botão voltar flutuante */
.floating-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: white;
  color: #3498db;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s;
}

.floating-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
}

/* Cards de informação */
.info-cards {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-top: -40px;
  margin-bottom: 40px;
}

.info-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  width: 280px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 20px;
  transition: transform 0.3s;
}

.info-card:hover {
  transform: translateY(-5px);
}

.info-card i {
  font-size: 2rem;
  color: #3498db;
}

.info-card h3 {
  font-size: 1rem;
  color: #7f8c8d;
  margin-bottom: 5px;
}

.info-card p {
  font-size: 1.2rem;
  font-weight: 500;
  color: #2c3e50;
}

/* Seção de atividades */
.atividades-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin: 0 20px 40px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.section-header h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-header h2 i {
  color: #3498db;
}

.add-button {
  background: #3498db;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 500;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s;
}

.add-button:hover {
  background: #2980b9;
  transform: translateY(-2px);
}

.atividades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.atividade-card {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  transition: all 0.3s;
  border: 1px solid #e0e0e0;
}

.atividade-card:hover {
  background: white;
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.2);
  border-color: #3498db;
}

.atividade-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 15px;
  color: white;
  font-size: 1.2rem;
}

.atividade-card h3 {
  font-size: 1.1rem;
  color: #2c3e50;
}

/* Seção de alunos */
.alunos-section {
  background: white;
  border-radius: 15px;
  padding: 30px;
  margin: 0 20px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.05);
}

.alunos-section h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.alunos-section h2 i {
  color: #3498db;
}

/* Responsividade */
@media (max-width: 768px) {
  .info-cards {
    flex-direction: column;
    align-items: center;
  }
  
  .turma-header {
    padding: 30px 20px 70px;
  }
  
  .turma-header h1 {
    font-size: 2rem;
  }
  
  .atividades-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
}
</style>