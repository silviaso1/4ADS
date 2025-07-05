<template>
  <section class="container-secao">
    <div class="cabecalho-secao">
      <h2><i class="fas fa-check-circle"></i> Disciplinas Concluídas</h2>
    </div>
    
    <div v-if="disciplinas.length > 0" class="grade-disciplinas">
      <CartaoDisciplina 
        v-for="disciplina in disciplinas" 
        :key="disciplina.codigo" 
        :disciplina="disciplina"
        tipo="concluida"
      />
    </div>
    <div v-else class="mensagem-vazia">
      <p>Nenhuma disciplina concluída ainda.</p>
    </div>
  </section>
</template>

<script>
import CartaoDisciplina from './CartaoDisciplina.vue'

export default {
  name: 'DisciplinasConcluidas',
  components: { CartaoDisciplina },
  props: {
    disciplinas: Array
  }
}
</script>

<style scoped>
.container-secao {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  margin-top: 70px;
}

.cabecalho-secao h2 {
  color: #2c3e50;
  font-size: 20px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
}

.cabecalho-secao h2 i {
  color: #3498db;
}

.grade-disciplinas {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.mensagem-vazia {
  text-align: center;
  padding: 20px;
  color: #7f8c8d;
  font-style: italic;
}

@media (max-width: 768px) {
  .grade-disciplinas {
    grid-template-columns: 1fr;
  }
}
</style>