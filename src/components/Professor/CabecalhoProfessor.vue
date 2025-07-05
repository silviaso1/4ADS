<template>
  <header class="cabecalho-professor">
    <div class="conteiner-cabecalho">
     
      
      <div class="menu-usuario">
        <div class="info-usuario">
          <span class="nome-usuario">Prof. Carlos Silva</span>
          <span class="email-usuario">carlos.silva@escola.com</span>
        </div>
        <div class="avatar-usuario">

        </div>
        <button class="botao-sair" @click="$emit('sair')">
          <i class="fas fa-sign-out-alt"></i>
        </button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'CabecalhoProfessor',
  emits: ['sair']
}
</script>

<style scoped>
.cabecalho-professor {
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.conteiner-cabecalho {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 0;
}

.logo-titulo h1 {
  font-size: 20px;
  font-weight: 600;
}

.menu-usuario {
  display: flex;
  align-items: center;
  gap: 20px;
}

.info-usuario {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.nome-usuario {
  font-weight: 500;
  font-size: 14px;
}

.email-usuario {
  font-size: 12px;
  opacity: 0.8;
}

.botao-sair {
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: all 0.2s;
}

.botao-sair:hover {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>