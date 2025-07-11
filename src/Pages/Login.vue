<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <h1>Bem-vindo</h1>
        <p>Acesse sua conta para continuar</p>
      </div>
      
      <div class="user-type-selector">
        <button 
          v-for="type in userTypes" 
          :key="type.value"
          @click="selectUserType(type.value)"
          :class="{ active: selectedUserType === type.value }"
          class="user-type-btn"
        >
          <i :class="type.icon"></i>
          <span>{{ type.label }}</span>
        </button>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="errorMsg" class="error-message">{{ errorMsg }}</div>

        <div class="form-group">
          <label for="username">Usuário</label>
          <div class="input-with-icon">
            <i class="fas fa-user"></i>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="Digite seu usuário ou e-mail"
              required
            >
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">Senha</label>
          <div class="input-with-icon">
            <i class="fas fa-lock"></i>
            <input 
              :type="showPassword ? 'text' : 'password'"
              id="password" 
              v-model="password" 
              placeholder="Digite sua senha"
              required
            >
            <i class="fas fa-eye toggle-password" @click="togglePasswordVisibility"></i>
          </div>
        </div>
        
        <div class="form-options">
          <label class="remember-me">
            <input type="checkbox" v-model="rememberMe" class="custom-checkbox">
            <span>Manter-me conectado</span>
          </label>
          <router-link to="/recuperar-senha" class="forgot-password">Esqueci minha senha</router-link>
        </div>
        
        <button type="submit" class="login-button">
          <span>Acessar</span>
          <i class="fas fa-sign-in-alt"></i>
        </button>
      </form>
    </div>
    
    <div class="login-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
      <div class="circle circle-3"></div>
      <div class="book-icon"><i class="fas fa-book-open"></i></div>
      <div class="graduate-icon"><i class="fas fa-graduation-cap"></i></div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      rememberMe: false,
      selectedUserType: 'student', // Altere para student como padrão
      showPassword: false,
      userTypes: [
        { value: 'student', label: 'Aluno', icon: 'fas fa-user-graduate' },
        { value: 'teacher', label: 'Professor', icon: 'fas fa-chalkboard-teacher' },
        { value: 'admin', label: 'Administrador', icon: 'fas fa-user-cog' }
      ],
      errorMsg: ''
    }
  },
  methods: {
    selectUserType(type) {
      this.selectedUserType = type
      this.errorMsg = ''
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword
    },
    async handleLogin() {
      this.errorMsg = ''

      if (!this.username || !this.password) {
        this.errorMsg = 'Preencha usuário e senha.'
        return
      }

      try {
        // 1. Autenticação
        const response = await axios.post('http://localhost:8000/api/usuarios/login/', {
          email: this.username,
          senha: this.password,
          tipo: this.selectedUserType === 'teacher' ? 'professor' : 
                this.selectedUserType === 'student' ? 'aluno' : 
                'admin'
        })

        // 2. Busca dados do usuário
        const usuariosResponse = await axios.get('http://localhost:8000/api/usuarios/')
        const usuarioLogado = usuariosResponse.data.find(u =>
          (u.email === this.username || u.usuario === this.username) &&
          (this.selectedUserType === 'teacher' ? u.tipo === 'professor' : 
           this.selectedUserType === 'student' ? u.tipo === 'aluno' : 
           u.tipo === 'admin')
        )

        if (!usuarioLogado) {
          this.errorMsg = 'Usuário não encontrado.'
          return
        }

        // 3. Salva dados do usuário
        const userData = {
          id: usuarioLogado.id,
          nome: usuarioLogado.nome,
          tipo: this.selectedUserType
        }

        if (this.rememberMe) {
          localStorage.setItem('userData', JSON.stringify(userData))
        } else {
          sessionStorage.setItem('userData', JSON.stringify(userData))
        }

        // 4. Redireciona
       // No método handleLogin, modifique apenas a parte do redirecionamento:
if (this.selectedUserType === 'student') {
  this.$router.push('/alunos')
} else if (this.selectedUserType === 'teacher') {
  this.$router.push('/professor')
} else {
  this.$router.push('/admin')
}

      } catch (error) {
        console.error('Erro no login:', error)
        this.errorMsg = error.response?.data?.message || 'Usuário ou senha inválidos'
      }
    }
  }
}
</script>


<style scoped>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
  font-family: 'Poppins', sans-serif;
  position: relative;
  overflow: hidden;
}

.login-card {
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  padding: 40px 50px;
  z-index: 10;
  position: relative;
  animation: fadeInUp 0.6s ease;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h1 {
  color: #2c3e50;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 8px;
}

.login-header p {
  color: #7f8c8d;
  font-size: 14px;
  font-weight: 400;
}

.user-type-selector {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
  gap: 12px;
}

.user-type-btn {
  flex: 1;
  padding: 14px 10px;
  border: none;
  border-radius: 10px;
  background-color: #f8f9fa;
  color: #555;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.user-type-btn i {
  font-size: 20px;
}

.user-type-btn.active {
  background: linear-gradient(135deg, #3498db 0%, #2c3e50 100%);
  color: white;
  box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
  transform: translateY(-2px);
}

.login-form .form-group {
  margin-bottom: 22px;
}

.login-form .form-group label {
  display: block;
  margin-bottom: 8px;
  color: #2c3e50;
  font-weight: 500;
  font-size: 14px;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon i {
  position: absolute;
  left: 15px;
  color: #7f8c8d;
  font-size: 16px;
  z-index: 1;
}

.input-with-icon .toggle-password {
  left: auto;
  right: 15px;
  cursor: pointer;
  color: #95a5a6;
}

.input-with-icon .toggle-password:hover {
  color: #3498db;
}

.login-form .form-group input {
  width: 100%;
  padding: 14px 15px 14px 45px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  font-size: 14px;
  transition: all 0.3s;
  background-color: #f8f9fa;
}

.login-form .form-group input:focus {
  border-color: #3498db;
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.2);
  outline: none;
  background-color: white;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 13px;
}

.remember-me {
  display: flex;
  align-items: center;
  color: #555;
  cursor: pointer;
  gap: 8px;
}

.custom-checkbox {
  appearance: none;
  width: 18px;
  height: 18px;
  border: 2px solid #bdc3c7;
  border-radius: 4px;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
}

.custom-checkbox:checked {
  background-color: #3498db;
  border-color: #3498db;
}

.custom-checkbox:checked::after {
  content: '\f00c';
  font-family: 'Font Awesome 5 Free';
  font-weight: 900;
  position: absolute;
  color: white;
  font-size: 10px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.forgot-password {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.2s;
}

.forgot-password:hover {
  color: #2980b9;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  padding: 16px;
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  box-shadow: 0 4px 10px rgba(52, 152, 219, 0.3);
}

.login-button:hover {
  background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
  box-shadow: 0 6px 15px rgba(52, 152, 219, 0.4);
  transform: translateY(-2px);
}

.login-button:active {
  transform: translateY(0);
}

.error-message {
  color: #e3342f;
  font-weight: 600;
  margin-bottom: 15px;
  text-align: center;
}

.login-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: linear-gradient(135deg, rgba(52, 152, 219, 0.05) 0%, rgba(41, 128, 185, 0.05) 100%);
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -150px;
  left: -150px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -100px;
  right: -100px;
}

.circle-3 {
  width: 200px;
  height: 200px;
  top: 30%;
  right: 15%;
}

.book-icon, .graduate-icon {
  position: absolute;
  font-size: 40px;
  color: rgba(52, 152, 219, 0.1);
}

.book-icon {
  bottom: 20%;
  left: 10%;
}

.graduate-icon {
  top: 20%;
  right: 10%;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 576px) {
  .login-card {
    padding: 30px 20px;
    margin: 0 15px;
  }
  
  .user-type-selector {
    flex-direction: column;
  }
}
</style>