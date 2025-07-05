<template>
  <div class="cartao-estatisticas">
    <h3>Estatísticas</h3>
    <div class="grade-estatisticas">
      <div class="item-estatistica">
        <div class="valor-estatistica">{{ mediaTurma.toFixed(1) }}</div>
        <div class="rotulo-estatistica">Média da Turma</div>
      </div>
      <div class="item-estatistica">
        <div class="valor-estatistica">{{ turma.alunos.length }}</div>
        <div class="rotulo-estatistica">Alunos</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CartaoEstatisticas',
  props: {
    turma: {
      type: Object,
      required: true
    }
  },
  computed: {
    mediaTurma() {
      const notasValidas = this.turma.alunos
        .filter(aluno => aluno.nota !== null)
        .map(aluno => aluno.nota)
      
      if (notasValidas.length === 0) return 0
      return notasValidas.reduce((sum, nota) => sum + nota, 0) / notasValidas.length
    }
  }
}
</script>

<style scoped>
.cartao-estatisticas {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.cartao-estatisticas h3 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.grade-estatisticas {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.item-estatistica {
  text-align: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.valor-estatistica {
  font-size: 24px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 5px;
}

.rotulo-estatistica {
  font-size: 12px;
  color: #7f8c8d;
}
</style>