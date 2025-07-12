<template>
  <header class="cabecalho-portal">
  
    
    <div class="right-section">
      <div class="logo-simbolo">
        <i class="fas fa-user-shield"></i>
      </div>
      <button class="logout-btn" @click="irParaInicio">
        <i class="fas fa-sign-out-alt"></i>
      </button>
    </div>
  </header>
</template>

<script>
export default {
  name: 'CabecalhoPortal',
  props: {
    menuAberto: Boolean
  },
  methods: {
    irParaInicio() {
      window.location.href = 'http://localhost:5173';
    }
  }
}
</script>

<style scoped>
.cabecalho-portal {
  background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: right;
  padding: 0 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 900;
  color: white;
}


.right-section {
  display: flex;
  align-items: center;
  justify-content: right;
  gap: 16px;
}

.logo-simbolo {
  font-size: 20px;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logout-btn {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

@media (max-width: 992px) {
  .cabecalho-portal {
    padding: 0 15px;
  }
}
</style>
