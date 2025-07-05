<template>
  <header class="cabecalho-portal">
    <div class="left-section">
      <button class="botao-menu-mobile" @click="$emit('toggle-menu')">
        <div class="hamburger" :class="{ 'active': menuAberto }">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </button>

    </div>
    
    <div class="right-section">
      <div class="user-menu">
        <div class="user-avatar">
          {{ usuarioIniciais }}
        </div>
        <div class="user-info">
          <span class="user-name">Administrador</span>
          <span class="user-role">admin@escola.com</span>
        </div>
        <button class="logout-btn" @click="$emit('logout')">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
   name: 'CabecalhoPortal',
  props: {
    nome: String,
    matricula: String,
    menuAberto: Boolean
  },
  data() {
    return {
      breadcrumbs: ['Portal', 'Aluno']
    }
  },
  computed: {
    usuarioIniciais() {
      if (!this.nome) return '';
      return this.nome.split(' ').map(n => n[0]).join('').toUpperCase();
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
  justify-content: space-between;
  padding: 0 30px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 900;
  color: white;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cabecalho__logo {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.icone-logo {
  font-size: 1.5rem;
  color: #fff;
}

.cabecalho__titulo {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: white;
}

.botao-menu-mobile {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 24px;
}

.hamburger span {
  height: 2px;
  background: white;
  transition: all 0.3s ease;
  border-radius: 2px;
}

.hamburger span:nth-child(1) {
  width: 100%;
}

.hamburger span:nth-child(2) {
  width: 80%;
}

.hamburger span:nth-child(3) {
  width: 60%;
}

.hamburger.active span:nth-child(1) {
  transform: translateY(7px) rotate(45deg);
  width: 100%;
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: translateY(-7px) rotate(-45deg);
  width: 100%;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 15px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.user-role {
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
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
  
  .user-info {
    display: none;
  }
}

@media (max-width: 768px) {
  .cabecalho__titulo {
    font-size: 1.1rem;
  }
}
</style>