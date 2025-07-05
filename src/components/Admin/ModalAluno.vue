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
        <div class="campo-formulario">
          <label for="nomeAluno">Nome Completo:</label>
          <input
            type="text"
            id="nomeAluno"
            v-model="alunoLocal.nome"
            placeholder="Digite o nome completo"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="matriculaAluno">Matrícula:</label>
          <input
            type="text"
            id="matriculaAluno"
            v-model="alunoLocal.id"
            placeholder="Número de matrícula"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="periodoAluno">Período de Ingresso:</label>
          <input
            type="text"
            id="periodoAluno"
            v-model="alunoLocal.periodo"
            placeholder="Ex: 2024.1"
          >
        </div>
      </div>
      
      <div class="modal__rodape">
        <button class="botao-secundario" @click="fecharModal">
          Cancelar
        </button>
        <button class="botao-primario" @click="salvar">
          {{ aluno ? 'Salvar Alterações' : 'Cadastrar Aluno' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
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
      alunoLocal: this.aluno ? { ...this.aluno } : { id: '', nome: '', periodo: '' }
    }
  },
  methods: {
    fecharModal() {
      this.$emit('fechar')
    },
    salvar() {
      if (!this.alunoLocal.nome || !this.alunoLocal.id || !this.alunoLocal.periodo) {
        alert('Preencha todos os campos obrigatórios')
        return
      }
      this.$emit('salvar', this.alunoLocal)
      this.fecharModal()
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
</style>