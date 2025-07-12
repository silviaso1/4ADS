<template>
  <div class="modal-overlay" @click.self="fecharModal">
    <div class="modal-conteudo">
      <header class="cabecalho-modal">
        <h3>{{ turma ? 'Editar Turma' : 'Adicionar Nova Turma' }}</h3>
        <button class="botao-fechar" @click="fecharModal" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </header>

      <section class="corpo-modal">
        <div class="grupo-formulario">
          <label for="nomeTurma">Nome da Turma:</label>
          <input
            type="text"
            id="nomeTurma"
            v-model="turmaLocal.nome"
            placeholder="Ex: Matemática Avançada"
          >
        </div>

        <div class="grupo-formulario">
          <label for="codigoTurma">Código:</label>
          <input
            type="text"
            id="codigoTurma"
            v-model="turmaLocal.codigo"
            placeholder="Ex: MAT-2024-1A"
          >
        </div>

        

        <div class="grupo-formulario">
          <label for="periodoTurma">Período:</label>
          <input
            type="text"
            id="periodoTurma"
            v-model="turmaLocal.periodo"
            placeholder="Ex: 2024.1"
          >
        </div>

        <div class="grupo-formulario">
          <label for="horarioTurma">Horário:</label>
          <input
            type="text"
            id="horarioTurma"
            v-model="turmaLocal.horario"
            placeholder="Ex: Segunda e Quarta, 14:00-16:00"
          >
        </div>

        <div class="grupo-formulario">
          <label for="salaTurma">Sala:</label>
          <input
            type="text"
            id="salaTurma"
            v-model="turmaLocal.sala"
            placeholder="Ex: Sala 203"
          >
        </div>
      </section>

      <footer class="rodape-modal">
        <button class="botao-cancelar" @click="fecharModal" :disabled="loading">Cancelar</button>
        <button class="botao-salvar" @click="salvar" :disabled="loading">
          {{ loading ? (turma ? 'Salvando...' : 'Cadastrando...') : (turma ? 'Salvar Alterações' : 'Cadastrar Turma') }}
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModalTurma',
  props: {
    turma: { type: Object, default: null },
    professores: { type: Array, required: true }
  },
  data() {
    return {
      turmaLocal: this.turma
        ? { ...this.turma }
        : {
            codigo: '',
            nome: '',
            professor_id: '',
            periodo: '',
            horario: '',
            sala: ''
          },
      loading: false
    }
  },
  methods: {
    fecharModal() {
      this.$emit('fechar')
    },
    async salvar() {
      if (!this.turmaLocal.nome.trim() || !this.turmaLocal.codigo.trim() || !this.turmaLocal.periodo.trim()) {
        alert('Preencha todos os campos obrigatórios: Nome, Código e Período.')
        return
      }

      this.loading = true

      try {
        const token = '039158ff2f7056df4a2d999c925afb79ee3cc8e0'
        const url = 'http://localhost:8000/api/turmas/'
        const dados = { ...this.turmaLocal }

        let response
        if (this.turma?.id) {
          response = await axios.put(`${url}${this.turma.id}/`, dados, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('Turma atualizada com sucesso!')
        } else {
          response = await axios.post(url, dados, {
            headers: { Authorization: `Bearer ${token}` }
          })
          alert('Turma cadastrada com sucesso!')
        }

        this.$emit('salvar', response.data)
        this.fecharModal()
      } catch (e) {
        console.error('Erro ao salvar turma:', e)
        alert('Erro ao salvar turma.')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600&display=swap');

.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1100;
}

.modal-conteudo {
  background: #fff;
  border-radius: 12px;
  max-width: 650px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.cabecalho-modal {
  background-color: #2c3e50;
  color: #fff;
  padding: 18px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.25rem;
  font-weight: 600;
}

.botao-fechar {
  background: none;
  border: none;
  color: #ecf0f1;
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.botao-fechar:hover {
  color: #e74c3c;
}

.corpo-modal {
  padding: 24px;
  overflow-y: auto;
  flex-grow: 1;
}

.grupo-formulario {
  margin-bottom: 24px;
}

.grupo-formulario label {
  display: block;
  margin-bottom: 8px;
  color: #2d3436;
  font-weight: 600;
  font-size: 0.95rem;
}

.grupo-formulario input,
.input-select {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1.5px solid #bdc3c7;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.grupo-formulario input:focus,
.input-select:focus {
  outline: none;
  border-color: #2980b9;
  box-shadow: 0 0 5px #2980b9aa;
}

.rodape-modal {
  padding: 16px 24px;
  background-color: #f1f2f6;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1.5px solid #dcdde1;
}

.botao-cancelar,
.botao-salvar {
  padding: 10px 28px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.25s;
}

.botao-cancelar {
  background-color: #dfe6e9;
  color: #2d3436;
  border: none;
}

.botao-cancelar:hover {
  background-color: #b2bec3;
}

.botao-salvar {
  background-color: #0984e3;
  color: white;
  border: 1.5px solid #0984e3;
}

.botao-salvar:disabled {
  background-color: #74b9ff88;
  border-color: #74b9ff88;
  cursor: not-allowed;
  color: #dfe6e9;
}

.botao-salvar:hover:not(:disabled) {
  background-color: #0652dd;
  border-color: #0652dd;
}
</style>
