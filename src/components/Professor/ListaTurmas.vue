<template>
  <div class="lista-turmas">
    <div class="cabecalho-lista">
      <h2>Minhas Turmas</h2>
      <div class="barra-pesquisa">
        <i class="fas fa-search"></i>
        <input 
          type="text" 
          placeholder="Pesquisar turmas..." 
          v-model="termoPesquisa"
        >
      </div>
    </div>
    
    <div class="grade-turmas">
      <div 
        v-for="turma in turmasFiltradas" 
        :key="turma.codigo" 
        class="cartao-turma"
        @click="$emit('selecionar-turma', turma)"
      >
        <div class="info-turma">
          <h3>{{ turma.nome }}</h3>
          <p class="codigo-turma">{{ turma.codigo }}</p>
          <p class="horario-turma">
            <i class="fas fa-calendar-day"></i> {{ turma.horario }}
          </p>
        </div>
        <div class="estatisticas-turma">
          <div class="item-estatistica">
            <i class="fas fa-users"></i>
            <span>{{ turma.alunos.length }} alunos</span>
          </div>
          <div class="item-estatistica">
            <i class="fas fa-tasks"></i>
            <span>{{ turma.atividades }} atividades</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ListaTurmas',
  props: {
    turmas: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      termoPesquisa: ''
    }
  },
  computed: {
    turmasFiltradas() {
      return this.turmas.filter(turma => {
        return turma.nome.toLowerCase().includes(this.termoPesquisa.toLowerCase()) ||
               turma.codigo.toLowerCase().includes(this.termoPesquisa.toLowerCase())
      })
    }
  },
  emits: ['selecionar-turma']
}
</script>

<style scoped>
.lista-turmas {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 10px;
}

.cabecalho-lista {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cabecalho-lista h2 {
  color: #2c3e50;
  font-size: 22px;
  font-weight: 600;
}

.barra-pesquisa {
  position: relative;
  width: 250px;
}

.barra-pesquisa i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #95a5a6;
}

.barra-pesquisa input {
  width: 100%;
  padding: 10px 15px 10px 35px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
}

.grade-turmas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.cartao-turma {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: all 0.3s;
}

.cartao-turma:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.info-turma h3 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 5px;
}

.codigo-turma {
  color: #7f8c8d;
  font-size: 13px;
  margin-bottom: 8px;
}

.horario-turma {
  color: #555;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.horario-turma i {
  color: #3498db;
}

.estatisticas-turma {
  display: flex;
  gap: 15px;
  padding-top: 10px;
  border-top: 1px solid #eee;
  margin-top: 15px;
}

.item-estatistica {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #7f8c8d;
}

.item-estatistica i {
  color: #3498db;
}
</style>