<template>
  <aside 
    class="barra-lateral" 
    :class="{ 'mobile-ativo': mostrarMobile }"
  >
  
    <nav class="menu-navegacao">
      <button 
        class="item-menu"
        :class="{ 'ativo': selecaoAtual === 'andamento' }"
        @click="$emit('mudar-selecao', 'andamento')"
      >
        <i class="fas fa-book-open icone-menu"></i>
        <span>Disciplinas Atuais</span>
      </button>
      
      <button 
        class="item-menu"
        :class="{ 'ativo': selecaoAtual === 'concluidas' }"
        @click="$emit('mudar-selecao', 'concluidas')"
      >
        <i class="fas fa-check-circle icone-menu"></i>
        <span>Disciplinas Concluídas</span>
      </button>
      
      <button 
        v-if="periodoMatriculaAberto"
        class="item-menu"
        :class="{ 'ativo': selecaoAtual === 'matricula' }"
        @click="$emit('mudar-selecao', 'matricula')"
      >
        <i class="fas fa-pencil-alt icone-menu"></i>
        <span>Nova Matrícula</span>
      </button>
      
     
    </nav>
  </aside>
</template>

<script>
export default {
  name: 'BarraLateral',
  props: {
    selecaoAtual: String,
    mostrarMobile: Boolean,
    periodoMatriculaAberto: {
      type: Boolean,
      default: true
    }
  }
}
</script>

<style scoped>
.barra-lateral {
  width: 250px;
  height: calc(100vh - 60px);
  position: fixed;
  left: 0;
  top: 70px;
  background: rgb(255, 255, 255);
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 90;
  transition: transform 0.3s ease;
}

.cabecalho-barra {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  gap: 10px;
}

.cabecalho-barra h3 {
  font-size: 16px;
  color: #2c3e50;
  margin: 0;
}

.icone-aluno {
  font-size: 20px;
  color: #3498db;
}

.menu-navegacao {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
}

.item-menu {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px 20px;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  color: #555;
}

.item-menu:hover {
  background-color: #f8f9fa;
  color: #3498db;
}

.item-menu.ativo {
  background-color: #e3f2fd;
  color: #3498db;
  border-left: 4px solid #3498db;
}

.icone-menu {
  width: 20px;
  text-align: center;
  font-size: 14px;
}

@media (max-width: 992px) {
  .barra-lateral {
    transform: translateX(-100%);
  }
  
  .barra-lateral.mobile-ativo {
    transform: translateX(0);
  }
}
</style>