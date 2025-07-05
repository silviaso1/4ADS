<template>
  <section class="container-secao">
    <div class="cabecalho-secao">
      <h2><i class="fas fa-pencil-alt"></i> Matricular em Novas Disciplinas</h2>
      <button class="botao-atualizar" @click="$emit('atualizar')">
        <i class="fas fa-sync-alt"></i> Atualizar
      </button>
    </div>
    
    <div v-if="disciplinasDisponiveis.length > 0" class="grade-disciplinas">
      <CartaoDisciplina 
        v-for="disciplina in disciplinasDisponiveis" 
        :key="disciplina.codigo" 
        :disciplina="disciplina"
        tipo="disponivel"
        @matricular="$emit('matricular', disciplina)"
      />
    </div>
    <div v-else class="mensagem-vazia">
      <p>Nenhuma disciplina disponível para matrícula no momento.</p>
    </div>
  </section>
</template>

<script>
import CartaoDisciplina from './CartaoDisciplina.vue'

export default {
  name: 'MatriculaDisciplinas',
  components: { CartaoDisciplina },
  props: {
    disciplinasDisponiveis: Array
  }
}
</script>

<style scoped>
.botao-atualizar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #555;
  cursor: pointer;
  transition: all 0.2s;

}

.botao-atualizar:hover {
  background-color: #f0f0f0;
}
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