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
      
      <div class="breadcrumbs">
        <span v-for="(crumb, index) in breadcrumbs" :key="index" 
              :class="{ 'active': index === breadcrumbs.length - 1 }">
          {{ crumb }}
          <i class="fas fa-chevron-right" v-if="index < breadcrumbs.length - 1"></i>
        </span>
      </div>
    </div>
    
    <div class="right-section">
    
      

      
      <div class="user-menu">
        <div class="user-avatar">
          {{ usuarioIniciais }}
        </div>
        <div class="user-info">
          <span class="user-name">{{ nome }}</span>
          <span class="user-role">Aluno</span>
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
  color: white !important;
}

.left-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.botao-menu-mobile {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
  background: white;
}

.hamburger {
  display: flex;
  flex-direction: column;
  gap: 5px;
  width: 24px;
}

.hamburger span {
  height: 2px;
  background: #2c3e50;
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

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: white;
}

.breadcrumbs .active {
  color: white;
  font-weight: 500;
}

.breadcrumbs i {
  font-size: 10px;
  opacity: 0.6;
}

.right-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.search-box {
  position: relative;
  width: 200px;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #95a5a6;
  font-size: 14px;
}

.search-box input {
  width: 100%;
  padding: 10px 15px 10px 35px;
  border: 1px solid #eee;
  border-radius: 8px;
  font-size: 13px;
  transition: all 0.3s ease;
  background: #f9f9f9;
}

.search-box input:focus {
  outline: none;
  border-color: #3498db;
  background: white;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}

.notifications {
  position: relative;
}

.notification-btn {
  background: none;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #2c3e50;
  transition: all 0.3s ease;
  position: relative;
}

.notification-btn:hover {
  background: #f5f7fa;
}

.badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: #e74c3c;
  color: white;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  font-size: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 15px;
  border-left: 1px solid #eee;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3498db 0%, #2ecc71 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
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
  color: #2c3e50;
}

.user-role {
  font-size: 12px;
  color: #95a5a6;
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
  color: #95a5a6;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background: #f5f7fa;
  color: #e74c3c;
}

@media (max-width: 992px) {
  .cabecalho-portal {
    padding: 0 15px;
  }
  
  .search-box {
    display: none;
  }
  
  .user-info {
    display: none;
  }
}
</style>