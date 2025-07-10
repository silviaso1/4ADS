<template>
  <div class="modal-overlay" @click.self="fecharModal">
    <div class="modal">
      <div class="modal__cabecalho">
        <h3 class="modal__titulo">
          {{ aluno ? 'Editar Aluno' : 'Adicionar Novo Aluno' }}
        </h3>
        <button class="modal__fechar" @click="fecharModal" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <div class="modal__corpo">
        <div class="campo-formulario" v-if="aluno">
          <label for="idAluno">ID (Gerado pelo sistema):</label>
          <input
            type="text"
            id="idAluno"
            v-model="alunoLocal.id"
            readonly
          >
        </div>

        <div class="campo-formulario" v-if="aluno">
          <label for="matriculaAluno">Matrícula (Gerada pelo sistema):</label>
          <input
            type="text"
            id="matriculaAluno"
            v-model="alunoLocal.matricula"
            readonly
          >
        </div>

        <div class="campo-formulario" v-else>
          <!-- Quando não existe aluno, não mostra id nem matrícula pois são gerados no backend -->
          <p><em>ID e Matrícula serão gerados automaticamente pelo sistema após o cadastro.</em></p>
        </div>

        <div class="campo-formulario">
          <label for="nomeAluno">Nome:</label>
          <input
            type="text"
            id="nomeAluno"
            v-model="alunoLocal.nome"
            placeholder="Digite o nome do aluno"
            required
          >
        </div>

        <div class="campo-formulario">
          <label for="emailAluno">Email:</label>
          <input
            type="email"
            id="emailAluno"
            v-model="alunoLocal.email"
            placeholder="Email institucional"
            required
          >
        </div>

        <div class="campo-formulario">
          <label for="periodoAluno">Período de Ingresso:</label>
          <input
            type="text"
            id="periodoAluno"
            v-model="alunoLocal.periodo_ingresso"
            placeholder="Ex: 2024.1"
            required
          >
        </div>

        <div class="campo-formulario">
          <label for="senhaAluno">Senha:</label>
          <input
            type="password"
            id="senhaAluno"
            v-model="alunoLocal.senha"
            :placeholder="aluno ? 'Deixe em branco para não alterar' : 'Digite a senha'"
            :required="!aluno"
          >
        </div>

        <div class="campo-formulario">
          <label for="tipoAluno">Tipo:</label>
          <input
            type="text"
            id="tipoAluno"
            v-model="alunoLocal.tipo"
            readonly
          >
        </div>
      </div>

      <div class="modal__rodape">
        <button class="botao-secundario" @click="fecharModal">
          Cancelar
        </button>
        <button class="botao-primario" @click="salvar" :disabled="loading">
          {{ aluno ? (loading ? 'Salvando...' : 'Salvar Alterações') : (loading ? 'Cadastrando...' : 'Cadastrar Aluno') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModalAluno',
  props: {
    aluno: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      alunoLocal: this.aluno
        ? { ...this.aluno, senha: '' }
        : { nome: '', email: '', periodo_ingresso: '', senha: '', tipo: 'aluno' },
      loading: false,
      errorMsg: ''
    }
  },
  methods: {
    fecharModal() {
      this.$emit('fechar')
    },

    async salvar() {
      // validação dos campos obrigatórios
      if (
        !this.alunoLocal.nome.trim() ||
        !this.alunoLocal.email.trim() ||
        !this.alunoLocal.periodo_ingresso.trim() ||
        (!this.aluno && !this.alunoLocal.senha.trim())
      ) {
        alert('Preencha todos os campos obrigatórios')
        return
      }

      this.loading = true
      this.errorMsg = ''

      try {
        const urlBase = 'http://localhost:8000/api/usuarios/'

        // Monta os dados para envio
        const dados = {
          nome: this.alunoLocal.nome.trim(),
          email: this.alunoLocal.email.trim(),
          periodo_ingresso: this.alunoLocal.periodo_ingresso.trim(),
          tipo: 'aluno'
        }
        if (!this.aluno || this.alunoLocal.senha.trim() !== '') {
          dados.senha = this.alunoLocal.senha.trim()
        }

        let response

        if (this.aluno) {
          // PUT para editar aluno (usa o id no endpoint)
          response = await axios.put(`${urlBase}${this.alunoLocal.id}/`, dados, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          alert('Aluno atualizado com sucesso!')
        } else {
          // POST para criar aluno, sem id e matrícula no corpo (gerados backend)
          response = await axios.post(urlBase, dados, {
            headers: {
              'Content-Type': 'application/json'
            }
          })
          alert('Aluno cadastrado com sucesso!')
        }

        this.$emit('salvar', response.data)
        this.fecharModal()
      } catch (error) {
        console.error('Erro ao salvar aluno:', error)
        if (error.response?.data) {
          const mensagens = Object.entries(error.response.data)
            .map(([campo, erros]) => `${campo}: ${erros.join(', ')}`)
            .join('\n')
          alert(`Erro ao salvar aluno:\n${mensagens}`)
        } else {
          alert('Erro ao salvar aluno.')
        }
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
/* Mesmos estilos que já usava */

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
  color: #2d3748;
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
  border-color: #3490dc;
  box-shadow: 0 0 0 3px rgba(52, 144, 220, 0.1);
}

.modal__rodape {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #edf2f7;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.botao-primario {
  background-color: #3490dc;
  border: none;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.botao-primario:hover {
  background-color: #2779bd;
}

.botao-secundario {
  background-color: #e2e8f0;
  border: none;
  color: #4a5568;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 600;
  transition: background-color 0.3s;
}

.botao-secundario:hover {
  background-color: #cbd5e0;
}
</style>
