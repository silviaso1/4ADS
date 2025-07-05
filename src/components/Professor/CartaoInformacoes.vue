<template>
  <div class="cartao-informacoes">
    <h3>Informações da Turma</h3>
    <div class="lista-informacoes">
      <div class="item-informacao">
        <i class="fas fa-calendar-alt"></i>
        <span><strong>Período:</strong> {{ turma.periodo }}</span>
      </div>
      <div class="item-informacao">
        <i class="fas fa-clock"></i>
        <span><strong>Horário:</strong> {{ turma.horario }}</span>
      </div>
      <div class="item-informacao">
        <i class="fas fa-door-open"></i>
        <span><strong>Sala:</strong> {{ turma.sala }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CartaoInformacoes',
  props: {
    turma: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
.cartao-informacoes {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
}

.cartao-informacoes h3 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.lista-informacoes {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item-informacao {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.item-informacao i {
  color: #3498db;
  width: 20px;
  text-align: center;
}
</style>