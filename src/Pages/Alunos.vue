<template>
  <div class="portal-aluno">
    <div class="cabecalho-portal">
      <h1>Portal do Aluno</h1>
      <button @click="logout" class="btn-logout">
        <i class="fas fa-sign-out-alt"></i> Sair
      </button>
    </div>
    
    <div class="container-portal">
      <main class="conteudo-portal">
        <DisciplinaModule />
      </main>
    </div>
  </div>
</template>

<script>
import DisciplinaModule from '../components/Aluno/Disciplinas.vue';

export default {
  name: 'PortalAluno',
  components: {
    DisciplinaModule
  },
  methods: {
    logout() {
      localStorage.removeItem('userData');
      sessionStorage.removeItem('userData');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.portal-aluno {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.cabecalho-portal {
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  color: white;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cabecalho-portal h1 {
  margin: 0;
  font-size: 1.5rem;
}

.btn-logout {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 8px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-logout:hover {
  background: rgba(255, 255, 255, 0.3);
}

.btn-logout i {
  margin-right: 5px;
}

.container-portal {
  padding: 20px;
  max-width: 1450px;
  margin: 0 auto;
}

.conteudo-portal {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 100%;
}
</style>