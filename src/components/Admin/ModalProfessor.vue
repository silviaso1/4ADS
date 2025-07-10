<template>
  <div class="modal-overlay" @click.self="fecharModal">
    <div class="modal">
      <div class="modal__cabecalho">
        <h3 class="modal__titulo">
          {{ professor ? 'Editar Professor' : 'Adicionar Novo Professor' }}
        </h3>
        <button class="modal__fechar" @click="fecharModal" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal__corpo">
        <div class="campo-formulario">
          <label for="nomeProfessor">Nome:</label>
          <input
            type="text"
            id="nomeProfessor"
            v-model="professorLocal.nome"
            placeholder="Digite o nome do professor"
            required
          >
        </div>

        <div class="campo-formulario">
          <label for="emailProfessor">Email:</label>
          <input
            type="email"
            id="emailProfessor"
            v-model="professorLocal.email"
            placeholder="Email institucional"
            required
          >
        </div>

        <div class="campo-formulario">
          <label for="senhaProfessor">Senha:</label>
          <input
            type="password"
            id="senhaProfessor"
            v-model="professorLocal.senha"
            :placeholder="professor ? 'Deixe em branco para não alterar' : 'Digite a senha'"
            :required="!professor"
          >
        </div>
      </div>

      <div class="modal__rodape">
        <button class="botao-secundario" @click="fecharModal">
          Cancelar
        </button>
        <button class="botao-primario" @click="salvar" :disabled="loading">
          {{ loading ? 'Salvando...' : (professor ? 'Salvar Alterações' : 'Cadastrar Professor') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModalProfessor',
  props: {
    professor: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      professorLocal: this.professor
        ? { ...this.professor, senha: '' }
        : { nome: '', email: '', senha: '' },
      loading: false
    }
  },
  methods: {
    fecharModal() {
      this.$emit('fechar')
    },

    async salvar() {
      if (!this.professorLocal.nome.trim() || !this.professorLocal.email.trim()) {
        alert('Preencha todos os campos obrigatórios.')
        return
      }

      if (!this.professor && !this.professorLocal.senha.trim()) {
        alert('A senha é obrigatória para novos professores.')
        return
      }

      const token = '52e42938087eea9afd4ec5f4a55de85da5d4d9c9' // token do admin logado
      const urlBase = 'http://localhost:8000/api/usuarios/login/'
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      }

      const payload = {
        nome: this.professorLocal.nome.trim(),
        email: this.professorLocal.email.trim(),
        tipo: 'professor'
      }

      if (this.professorLocal.senha.trim()) {
        payload.senha = this.professorLocal.senha.trim()
      }

      this.loading = true

      try {
        const response = await axios.post(urlBase, payload, { headers })
        alert('Professor cadastrado com sucesso!')
        this.$emit('salvar', response.data)
        this.fecharModal()
      } catch (erro) {
        console.error('Erro ao cadastrar professor:', erro)
        if (erro.response?.data) {
          const mensagens = Object.entries(erro.response.data)
            .map(([campo, erros]) => `${campo}: ${erros.join(', ')}`)
            .join('\n')
          alert(`Erro ao cadastrar professor:\n${mensagens}`)
        } else {
          alert('Erro ao cadastrar professor. Verifique os dados ou permissões.')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background-color: white;
  border-radius: 0.75rem;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: modalEntrada 0.3s ease;
}

@keyframes modalEntrada {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal__cabecalho {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #edf2f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal__titulo {
  font-size: 1.125rem;
  font-weight: 600;
  color: #9f7aea;
  margin: 0;
}

.modal__fechar {
  background: none;
  border: none;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #a0aec0;
  transition: all 0.2s;
}

.modal__fechar:hover {
  background-color: #f8fafc;
  color: #e53e3e;
}

.modal__corpo {
  padding: 1.5rem;
}

.campo-formulario {
  margin-bottom: 1.25rem;
}

.campo-formulario label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4a5568;
}

.campo-formulario input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.campo-formulario input:focus {
  outline: none;
  border-color: #9f7aea;
  box-shadow: 0 0 0 3px rgba(159, 122, 234, 0.2);
}

.modal__rodape {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #edf2f7;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.botao-primario {
  background-color: #9f7aea;
  border: none;
  color: white;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 600;
}

.botao-primario:hover {
  background-color: #805ad5;
}

.botao-secundario {
  background-color: #e2e8f0;
  border: none;
  color: #4a5568;
  padding: 0.6rem 1.2rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: 0.3s;
}

.botao-secundario:hover {
  background-color: #cbd5e0;
}
</style>
