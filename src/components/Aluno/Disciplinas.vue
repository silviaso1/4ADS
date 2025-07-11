<template>
  <section class="disciplina-module">
    <!-- Header do módulo -->
    <div class="module-header">
      <div class="header-left">
        <span class="header-icon">
          <i class="fas fa-book-open"></i>
        </span>
        <h2 class="module-title">Minhas Disciplinas</h2>
      </div>
      <div v-if="disciplinas.length > 0" class="module-counter">
        {{ disciplinas.length }} {{ disciplinas.length === 1 ? 'disciplina' : 'disciplinas' }}
      </div>
    </div>

    <!-- Estado de carregamento -->
    <div v-if="loading" class="loading-state">
      <div class="spinner">
        <i class="fas fa-spinner fa-spin"></i>
      </div>
      <p>Carregando disciplinas...</p>
    </div>

    <!-- Lista de disciplinas -->
    <div v-else-if="disciplinas.length > 0" class="disciplinas-grid">
      <CartaoDisciplina 
        v-for="disciplina in disciplinas" 
        :key="disciplina.id" 
        :disciplina="disciplina"
      />
    </div>

    <!-- Estado vazio -->
    <div v-else class="empty-state">
      <div class="empty-illustration">
        <i class="fas fa-book"></i>
      </div>
      <h3>Nenhuma disciplina matriculada</h3>
      <p>Você não está matriculado em nenhuma disciplina no momento.</p>
      <button class="empty-action">Ver oferta de disciplinas</button>
    </div>
  </section>
</template>

<script>
import axios from 'axios';
import CartaoDisciplina from './CartaoDisciplina.vue';

export default {
  name: 'DisciplinaModule',
  components: {
    CartaoDisciplina
  },
  data() {
    return {
      disciplinas: [],
      loading: true,
      alunoId: null
    }
  },
  async created() {
    const userData = JSON.parse(localStorage.getItem('userData') || sessionStorage.getItem('userData'));
    if (!userData || userData.tipo !== 'student') {
      this.$router.push('/login');
      return;
    }
    
    this.alunoId = userData.id;
    await this.carregarDisciplinas();
  },
  methods: {
    async carregarDisciplinas() {
      try {
        // 1. Buscar todas as notas do aluno
        const notasResponse = await axios.get('http://localhost:8000/api/matriculas/notas/');
        const notasAluno = notasResponse.data.filter(nota => nota.aluno == this.alunoId);
        
        // 2. Buscar informações das atividades
        const atividadesResponse = await axios.get('http://localhost:8000/api/turmas/atividades/');
        
        // 3. Buscar informações das turmas
        const turmasResponse = await axios.get('http://localhost:8000/api/turmas/');
        
        // 4. Organizar as disciplinas por turma
        const disciplinasMap = {};
        
        notasAluno.forEach(nota => {
          const turmaInfo = turmasResponse.data.find(t => t.id == nota.turma);
          const atividadeInfo = atividadesResponse.data.find(a => a.id == nota.atividade);
          
          if (turmaInfo && atividadeInfo) {
            if (!disciplinasMap[nota.turma]) {
              disciplinasMap[nota.turma] = {
                id: nota.turma,
                codigo: turmaInfo.codigo,
                nome: turmaInfo.nome,
                professor: turmaInfo.professor ? `Professor ${turmaInfo.professor}` : 'Professor não definido',
                notas: [],
                somaNotas: 0,
                totalAtividades: 0
              };
            }
            
            disciplinasMap[nota.turma].notas.push({
              atividade: nota.atividade,
              nomeAtividade: atividadeInfo.nome,
              valor: parseFloat(nota.nota)
            });
            
            disciplinasMap[nota.turma].somaNotas += parseFloat(nota.nota);
            disciplinasMap[nota.turma].totalAtividades++;
          }
        });
        
        // 5. Calcular médias e formatar os dados
        this.disciplinas = Object.values(disciplinasMap).map(disciplina => {
          disciplina.mediaFinal = disciplina.totalAtividades > 0 ? 
            disciplina.somaNotas / disciplina.totalAtividades : 0;
          return disciplina;
        });
        
      } catch (error) {
        console.error('Erro ao carregar disciplinas:', error);
      } finally {
        this.loading = false;
      }
    },
    stringToColor(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      const hue = Math.abs(hash % 360);
      return `hsl(${hue}, 80%, 85%)`;
    },
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').slice(0, 3);
    }
  }
}
</script>

<style scoped>
/* Variáveis de design */
:root {
  --primary: #4361ee;
  --primary-light: #eef2ff;
  --secondary: #3f37c9;
  --success: #4cc9f0;
  --warning: #f8961e;
  --danger: #f72585;
  --light: #f8f9fa;
  --dark: #212529;
  --gray: #6c757d;
  --border-radius: 12px;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
}

/* Estilos do módulo principal */
.disciplina-module {
  background: white;
  border-radius: var(--border-radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.header-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: var(--primary-light);
  color: var(--primary);
  border-radius: 50%;
}

.module-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--dark);
}

.module-counter {
  background: var(--light);
  color: var(--gray);
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Estados */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.spinner {
  font-size: 1.8rem;
  color: var(--primary);
  margin-bottom: 1rem;
}

.loading-state p {
  margin: 0;
  color: var(--gray);
}

.empty-state {
  text-align: center;
  padding: 2rem;
}

.empty-illustration {
  width: 80px;
  height: 80px;
  margin: 0 auto 1rem;
  background: var(--primary-light);
  color: var(--primary);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
}

.empty-state h3 {
  margin: 0.5rem 0;
  color: var(--dark);
  font-weight: 600;
}

.empty-state p {
  margin: 0 0 1rem;
  color: var(--gray);
  max-width: 300px;
  margin: 0 auto 1.5rem;
}

.empty-action {
  background: var(--primary);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.empty-action:hover {
  background: var(--secondary);
}

/* Grid de disciplinas */
.disciplinas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

/* Responsividade */
@media (max-width: 768px) {
  .disciplinas-grid {
    grid-template-columns: 1fr;
  }
  
  .module-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
}
</style>