<template>
  <section class="disciplina-module light-theme">
    <div class="module-header">
      <h2 class="module-title">
        <span class="title-decorator"></span>
        Disciplinas em Andamento
      </h2>
      <div class="module-counter" v-if="disciplinas.length > 0">
        {{ disciplinas.length }} {{ disciplinas.length === 1 ? 'disciplina' : 'disciplinas' }}
      </div>
    </div>
    
    <div v-if="disciplinas.length > 0" class="disciplinas-container">
      <div class="disciplina-card" v-for="disciplina in disciplinas" :key="disciplina.codigo">
        <div class="card-header">
          <div class="disciplina-avatar" :style="{ backgroundColor: stringToColor(disciplina.nome) }">
            {{ getInitials(disciplina.nome) }}
          </div>
          <div class="disciplina-info">
            <h3>{{ disciplina.nome }}</h3>
            <p class="disciplina-code">{{ disciplina.codigo }}</p>
          </div>
        </div>
        
        <div class="card-body">
          <div class="professor-info">
            <span class="professor-label">Professor:</span>
            <span class="professor-name">{{ disciplina.professor }}</span>
          </div>
          
          <div class="grades-container">
            <div class="grade-item">
              <div class="grade-label">AV1</div>
              <div class="grade-value" :class="getGradeClass(disciplina.notas.av1)">
                {{ formatGrade(disciplina.notas.av1) }}
              </div>
            </div>
            
            <div class="grade-item">
              <div class="grade-label">AV2</div>
              <div class="grade-value" :class="getGradeClass(disciplina.notas.av2)">
                {{ formatGrade(disciplina.notas.av2) }}
              </div>
            </div>
            
            <div class="grade-item">
              <div class="grade-label">AVF</div>
              <div class="grade-value" :class="getGradeClass(disciplina.notas.avf)">
                {{ formatGrade(disciplina.notas.avf) }}
              </div>
            </div>
            
            <div class="grade-item final">
              <div class="grade-label">MÉDIA</div>
              <div class="grade-value" :class="getGradeClass(disciplina.mediaFinal)">
                {{ disciplina.mediaFinal.toFixed(1) }}
              </div>
            </div>
          </div>
        </div>
        
        <div class="card-progress">
          <div class="progress-bar" :style="{ width: calculateProgress(disciplina) + '%' }"></div>
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <div class="empty-illustration"></div>
      <h3>Nenhuma disciplina em andamento</h3>
      <p>Você não está matriculado em nenhuma disciplina no momento.</p>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    disciplinas: Array
  },
  methods: {
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').slice(0, 3)
    },
    stringToColor(str) {
      let hash = 0;
      for (let i = 0; i < str.length; i++) {
        hash = str.charCodeAt(i) + ((hash << 5) - hash);
      }
      const hue = Math.abs(hash % 360);
      return `hsl(${hue}, 80%, 85%)`;
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
    calculateProgress(disciplina) {
      const total = 3; // AV1, AV2, AVF
      const completed = [disciplina.notas.av1, disciplina.notas.av2, disciplina.notas.avf]
        .filter(n => n !== null).length;
      return (completed / total) * 100;
    }
  }
}
</script>

<style scoped>
.disciplina-module.light-theme {
  background: rgb(255, 255, 255);
  border-radius: 16px;
  padding: 30px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.03);
  margin-bottom: 40px;
  margin-top: 70px;
}

.module-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.module-title {
  font-size: 22px;
  font-weight: 600;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 0;
}

.title-decorator {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 8px;
  background: linear-gradient(135deg, #3498db 0%, #2ecc71 100%);
}

.module-counter {
  background: #f8f9fa;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
  color: #7f8c8d;
}

.disciplinas-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.disciplina-card {
  background: white;
  border-radius: 12px;
  border: 1px solid #f0f0f0;
  overflow: hidden;
  transition: all 0.3s ease;
}


.card-header {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f5f5f5;
}

.disciplina-avatar {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  color: #2c3e50;
  margin-right: 15px;
  font-size: 16px;
}

.disciplina-info h3 {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.disciplina-code {
  font-size: 12px;
  color: #95a5a6;
  margin: 0;
}

.card-body {
  padding: 20px;
}

.professor-info {
  margin-bottom: 20px;
}

.professor-label {
  font-size: 13px;
  color: #95a5a6;
  margin-right: 8px;
}

.professor-name {
  font-size: 14px;
  color: #2c3e50;
  font-weight: 500;
}

.grades-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}

.grade-item {
  text-align: center;
}

.grade-item.final {
  position: relative;
}

.grade-item.final::before {
  content: '';
  position: absolute;
  left: -5px;
  top: 0;
  height: 100%;
  width: 1px;
  background: #f0f0f0;
}

.grade-label {
  font-size: 11px;
  color: #95a5a6;
  text-transform: uppercase;
  margin-bottom: 6px;
  letter-spacing: 0.5px;
}

.grade-value {
  font-size: 16px;
  font-weight: 600;
  padding: 6px;
  border-radius: 6px;
}

.grade-value.empty {
  background: #f5f5f5;
  color: #95a5a6;
}

.grade-value.excellent {
  background: #e8f5e9;
  color: #2e7d32;
}

.grade-value.good {
  background: #e3f2fd;
  color: #1565c0;
}

.grade-value.average {
  background: #fff8e1;
  color: #ff8f00;
}

.grade-value.low {
  background: #ffebee;
  color: #c62828;
}

.card-progress {
  height: 4px;
  background: #f5f5f5;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #3498db 0%, #2ecc71 100%);
  transition: width 0.6s ease;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-illustration {
  width: 120px;
  height: 120px;
  margin: 0 auto 20px;
  background: #f8f9fa;
  border-radius: 50%;
  position: relative;
  overflow: hidden;
}

.empty-illustration::before,
.empty-illustration::after {
  content: '';
  position: absolute;
  background: #e0e0e0;
}

.empty-illustration::before {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  top: 20px;
  left: 20px;
}

.empty-illustration::after {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  top: 40px;
  left: 40px;
  background: #f5f5f5;
}

.empty-state h3 {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.empty-state p {
  color: #95a5a6;
  font-size: 14px;
  margin: 0;
}

@media (max-width: 768px) {
  .disciplinas-container {
    grid-template-columns: 1fr;
  }
  
  .grades-container {
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
  }
  
  .grade-item.final::before {
    display: none;
  }
}
</style>