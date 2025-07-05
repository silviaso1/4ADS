<template>
  <div class="cartao-disciplina" :class="{ 'disponivel': tipo === 'disponivel' }">
    <div class="info-disciplina">
      <h3>{{ disciplina.nome }}</h3>
      <p class="codigo-disciplina">{{ disciplina.codigo }}</p>
      <p class="professor-disciplina">
        <i class="fas fa-chalkboard-teacher"></i> {{ disciplina.professor }}
      </p>
      <p v-if="tipo === 'disponivel'" class="horario-disciplina">
        <i class="fas fa-calendar-day"></i> {{ disciplina.horario }}
      </p>
    </div>
    
    <div v-if="tipo === 'andamento'" class="container-notas">
      <div class="linha-nota">
        <span>AV1:</span>
        <span class="badge-nota" :class="classeNota(disciplina.notas.av1)">
          {{ formatarNota(disciplina.notas.av1) }}
        </span>
      </div>
      <div class="linha-nota">
        <span>AV2:</span>
        <span class="badge-nota" :class="classeNota(disciplina.notas.av2)">
          {{ formatarNota(disciplina.notas.av2) }}
        </span>
      </div>
      <div class="linha-nota final">
        <span>Média:</span>
        <span class="badge-nota" :class="classeNota(disciplina.mediaFinal)">
          {{ disciplina.mediaFinal.toFixed(1) }}
        </span>
      </div>
    </div>
    
    <div v-if="tipo === 'concluida'" class="container-status">
      <div class="linha-nota">
        <span>Média Final:</span>
        <span class="badge-nota" :class="classeNota(disciplina.mediaFinal)">
          {{ disciplina.mediaFinal.toFixed(1) }}
        </span>
      </div>
      <div class="badge-status" :class="disciplina.status">
        {{ textoStatus(disciplina.status) }}
      </div>
    </div>
    
    <button 
      v-if="tipo === 'disponivel'" 
      class="botao-matricular" 
      @click="$emit('matricular', disciplina)"
    >
      <i class="fas fa-plus"></i> Matricular
    </button>
  </div>
</template>

<script>
export default {
  name: 'CartaoDisciplina',
  props: {
    disciplina: Object,
    tipo: {
      type: String,
      validator: value => ['andamento', 'concluida', 'disponivel'].includes(value),
      default: 'andamento'
    }
  },
  methods: {
    formatarNota(nota) {
      return nota !== null ? nota.toFixed(1) : '-'
    },
    classeNota(nota) {
      if (nota === null) return 'sem-nota'
      if (nota >= 9) return 'excelente'
      if (nota >= 7) return 'boa'
      if (nota >= 5) return 'media'
      return 'baixa'
    },
    textoStatus(status) {
      const statusMap = {
        'aprovado': 'Aprovado',
        'reprovado': 'Reprovado',
        'cursando': 'Cursando'
      }
      return statusMap[status] || status
    }
  }
}
</script>

<style scoped>
.cartao-disciplina {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  border: 1px solid #eee;
}

.cartao-disciplina.disponivel {
  border: 2px dashed #3498db;
}

.cartao-disciplina:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-disciplina {
  margin-bottom: 15px;
}

.info-disciplina h3 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
}

.codigo-disciplina {
  color: #7f8c8d;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 8px;
}

.professor-disciplina,
.horario-disciplina {
  color: #555;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 5px;
  margin: 3px 0;
}

.professor-disciplina i,
.horario-disciplina i {
  color: #3498db;
  font-size: 14px;
  width: 16px;
  text-align: center;
}

/* Estilos para notas */
.container-notas,
.container-status {
  margin-top: auto;
  padding-top: 15px;
  border-top: 1px solid #eee;
}

.linha-nota {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-size: 13px;
}

.linha-nota.final {
  font-weight: 600;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.badge-nota {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
}

.badge-nota.excelente {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-nota.boa {
  background-color: #e3f2fd;
  color: #1565c0;
}

.badge-nota.media {
  background-color: #fff8e1;
  color: #ff8f00;
}

.badge-nota.baixa {
  background-color: #ffebee;
  color: #c62828;
}

.badge-nota.sem-nota {
  background-color: #f5f5f5;
  color: #757575;
}

/* Estilos para status */
.badge-status {
  margin-top: 10px;
  padding: 6px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
}

.badge-status.aprovado {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-status.reprovado {
  background-color: #ffebee;
  color: #c62828;
}

.badge-status.cursando {
  background-color: #e3f2fd;
  color: #1565c0;
}

/* Botão de matrícula */
.botao-matricular {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background-color: #3498db;
  border: 1px solid #3498db;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: white;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 15px;
  width: 100%;
  justify-content: center;
}

.botao-matricular:hover {
  background-color: #2980b9;
  box-shadow: 0 3px 10px rgba(52, 152, 219, 0.2);
}
</style>