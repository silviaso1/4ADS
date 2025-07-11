<template>
  <div class="disciplina-card" :style="{'--card-color': stringToDarkColor(disciplina.nome)}">
    <!-- Cabeçalho do card com gradiente dinâmico -->
    <div class="card-header">
      <div class="header-overlay"></div>
      <div class="header-content">
        <div class="disciplina-avatar" :style="{ backgroundColor: stringToColor(disciplina.nome) }">
          {{ getInitials(disciplina.nome) }}
        </div>
        <div class="disciplina-info">
          <h3>{{ disciplina.nome }}</h3>
          <p class="disciplina-code">{{ disciplina.codigo }}</p>
        </div>
        <div class="status-chip" :class="getStatusClass(disciplina.mediaFinal)">
          {{ getStatusText(disciplina.mediaFinal) }}
        </div>
      </div>
    </div>
    
    <!-- Corpo do card -->
    <div class="card-body">
      <div class="professor-info">
        <div class="icon-wrapper">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12 3L1 9l11 6 9-4.91V17h2V9M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82Z"/>
          </svg>
        </div>
        <span>{{ disciplina.professor }}</span>
      </div>
      
      <div class="progress-container">
        <div class="progress-bar">
          <div class="progress-fill" :style="{width: getProgressWidth(disciplina.mediaFinal)}"></div>
          <div class="progress-marker" :style="{left: getProgressWidth(disciplina.mediaFinal)}">
            <span>{{ disciplina.mediaFinal.toFixed(1) }}</span>
          </div>
        </div>
        <div class="progress-labels">
          <span>0</span>
          <span>5</span>
          <span>7</span>
          <span>10</span>
        </div>
      </div>
      
      <div class="grades-grid">
        <div class="grade-item" v-for="nota in disciplina.notas" :key="nota.atividade">
          <div class="grade-circle" :class="getGradeClass(nota.valor)">
            {{ formatGrade(nota.valor) }}
          </div>
          <div class="grade-label">{{ nota.nomeAtividade }}</div>
        </div>
      </div>
    </div>
    
  </div>
</template>

<script>
export default {
  name: 'CartaoDisciplinaModerno',
  props: {
    disciplina: Object
  },
  methods: {
    getInitials(name) {
      if (!name) return '';
      return name.split(' ').map(n => n[0]).join('').slice(0, 3);
    },
    stringToColor(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      const hue = Math.abs(hash % 360);
      return `hsl(${hue}, 80%, 85%)`;
    },
    stringToDarkColor(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      const hue = Math.abs(hash % 360);
      return `hsl(${hue}, 70%, 30%)`;
    },
    formatGrade(grade) {
      return grade !== null ? grade.toFixed(1) : '--';
    },
    getGradeClass(grade) {
      if (grade === null) return 'empty';
      if (grade >= 9) return 'excellent';
      if (grade >= 7) return 'good';
      if (grade >= 5) return 'average';
      return 'low';
    },
    getStatusClass(media) {
      if (media >= 7) return 'aprovado';
      if (media >= 5) return 'recuperacao';
      return 'reprovado';
    },
    getStatusText(media) {
      if (media >= 7) return 'Aprovado';
      if (media >= 5) return 'Recuperação';
      return 'Reprovado';
    },
    getProgressWidth(media) {
      return `${Math.min(100, media * 10)}%`;
    }
  }
}
</script>

<style scoped>
:root {
  --border-radius: 16px;
  --shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  --transition: all 0.3s ease;
  --dark: #2d3748;
  --gray: #718096;
  --light: #f7fafc;
}

/* Estilos do card */
.disciplina-card {
  background: white;
  border-radius: var(--border-radius);
  display: flex;
  flex-direction: column;
  position: relative;
  --card-color: #3b82f6;
  width: 450px;
  border: 2px solid rgba(0, 0, 0, 0.973);

}



.card-header {
  position: relative;
  padding: 1.5rem;
  color: white;
  overflow: hidden;
}

.header-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, var(--card-color), #1e40af);
  z-index: 1;
}

.header-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.disciplina-avatar {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
  color: rgba(0, 0, 0, 0.7);
  flex-shrink: 0;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.disciplina-info {
  flex-grow: 1;
}

.disciplina-info h3 {
  margin: 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: white;
  line-height: 1.3;
}

.disciplina-code {
  margin: 0.3rem 0 0;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
}

.status-chip {
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  color: white;
  align-self: flex-start;
  margin-left: auto;
}

.status-chip.aprovado {
  background: rgba(34, 197, 94, 0.2);
  border: 1px solid rgba(34, 197, 94, 0.3);
}

.status-chip.recuperacao {
  background: rgba(234, 179, 8, 0.2);
  border: 1px solid rgba(234, 179, 8, 0.3);
}

.status-chip.reprovado {
  background: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

/* Corpo do card */
.card-body {
  padding: 1.5rem;
  flex-grow: 1;
}

.professor-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  font-size: 0.95rem;
  color: var(--gray);
}

.icon-wrapper {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(59, 130, 246, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--card-color);
}

/* Barra de progresso */
.progress-container {
  margin-bottom: 1.5rem;
}

.progress-bar {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  position: relative;
  margin-bottom: 0.5rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  background: linear-gradient(90deg, var(--card-color), #60a5fa);
  transition: width 0.6s ease;
}

.progress-marker {
  position: absolute;
  top: -20px;
  transform: translateX(-50%);
  background: rgb(0, 0, 0);
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--card-color);
}

.progress-marker::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 0;
  border-left: 6px solid transparent;
  border-right: 6px solid transparent;
  border-top: 6px solid rgb(0, 0, 0);
}

.progress-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.75rem;
  color: var(--gray);
}

/* Grades grid */
.grades-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}

.grade-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.grade-circle {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.grade-item:hover .grade-circle {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.grade-circle.excellent {
  border-color: #10b981;
  color: #10b981;
  background: rgba(16, 185, 129, 0.1);
}

.grade-circle.good {
  border-color: #3b82f6;
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.1);
}

.grade-circle.average {
  border-color: #f59e0b;
  color: #f59e0b;
  background: rgba(245, 158, 11, 0.1);
}

.grade-circle.low {
  border-color: #ef4444;
  color: #ef4444;
  background: rgba(239, 68, 68, 0.1);
}

.grade-circle.empty {
  border-color: #cbd5e1;
  color: #94a3b8;
}

.grade-label {
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--gray);
  text-align: center;
  line-height: 1.3;
}


</style>