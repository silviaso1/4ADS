<template>
  <aside 
    class="barra-lateral" 
    :class="{ 'mobile-ativo': mostrarMobile }"
  >
    <nav class="menu-navegacao">
      <button 
        v-for="item in itensMenu"
        :key="item.aba"
        class="item-menu"
        :class="{ 'ativo': abaAtiva === item.aba }"
        @click="$emit('mudar-aba', item.aba)"
      >
        <i :class="item.icone + ' icone-menu'"></i>
        <span>{{ item.texto }}</span>
      </button>
    </nav>
  </aside>
</template>

<script>
export default {
  name: 'MenuLateralAdmin',
  props: {
    abaAtiva: {
      type: String,
      default: 'alunos'
    },
    mostrarMobile: Boolean
  },
  data() {
    return {
      itensMenu: [
        { aba: 'alunos', icone: 'fas fa-users', texto: 'Alunos' },
        { aba: 'professores', icone: 'fas fa-chalkboard-teacher', texto: 'Professores' },
        { aba: 'turmas', icone: 'fas fa-door-open', texto: 'Turmas' },
      ]
    }
  }
}
</script>

<style scoped>
.barra-lateral {
  width: 250px;
  height: calc(100vh - 70px);
  position: fixed;
  left: 0;
  top: 70px;
  background: white;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  z-index: 90;
  transition: transform 0.3s ease;
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

@media (max-width: 768px) {
  .barra-lateral {
    width: 220px;
  }
}
</style>