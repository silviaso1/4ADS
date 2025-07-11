<template>
  <div class="modal-overlay" @click.self="$emit('fechar')">
    <div class="modal-conteudo">
      <div class="cabecalho-modal">
        <h3>Nova Atividade</h3>
        <button class="botao-fechar" @click="$emit('fechar')">
          <i class="fas fa-times"></i>
        </button>
      </div>

      <form @submit.prevent="cadastrarAtividade">
        <div class="form-group">
          <label for="nome">Nome da Atividade</label>
          <input
            id="nome"
            v-model="novaAtividade.nome"
            type="text"
            placeholder="Ex: Prova Final"
            required
          />
        </div>

        <button type="submit" class="botao-salvar">
          <i class="fas fa-save"></i> Salvar Atividade
        </button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModalAtividades',
  props: {
    turmaId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      novaAtividade: {
        nome: ''
      }
    }
  },
  methods: {
    async cadastrarAtividade() {
      try {
        const payload = {
          nome: this.novaAtividade.nome,
          turma: this.turmaId
        }

        const response = await axios.post(
          'http://localhost:8000/api/turmas/atividades/',
          payload
        )

        this.$emit('atividade-cadastrada', response.data)
        this.$emit('fechar')
        this.novaAtividade.nome = ''
      } catch (error) {
        console.error('Erro ao cadastrar atividade:', error)
        alert('Erro ao cadastrar atividade.')
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
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}

.modal-conteudo {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  position: relative;
}

.cabecalho-modal {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cabecalho-modal h3 {
  font-size: 1.5rem;
  color: #2c3e50;
}

.botao-fechar {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #888;
  cursor: pointer;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.botao-salvar {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.botao-salvar:hover {
  background: #2980b9;
}
</style>
