<template>
  <div class="modal-overlay" @click.self="fecharModal">
    <div class="modal modal--grande">
      <div class="modal__cabecalho">
        <h3 class="modal__titulo">
          {{ turma ? 'Editar Turma' : 'Adicionar Nova Turma' }}
        </h3>
        <button class="modal__fechar" @click="fecharModal" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal__corpo">
        <div class="campo-formulario">
          <label for="nomeTurma">Nome da Turma:</label>
          <input
            type="text"
            id="nomeTurma"
            v-model="turmaLocal.nome"
            placeholder="Ex: Matemática Avançada"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="codigoTurma">Código:</label>
          <input
            type="text"
            id="codigoTurma"
            v-model="turmaLocal.codigo"
            placeholder="Ex: MAT-2024-1A"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="professorTurma">Professor:</label>
          <select
            id="professorTurma"
            v-model="turmaLocal.professorId"
          >
            <option value="">Selecione um professor</option>
            <option 
              v-for="prof in professores" 
              :key="prof.id" 
              :value="prof.id"
            >
              {{ prof.nome }}
            </option>
          </select>
        </div>
        
        <div class="campo-formulario">
          <label for="periodoTurma">Período:</label>
          <input
            type="text"
            id="periodoTurma"
            v-model="turmaLocal.periodo"
            placeholder="Ex: 2024.1"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="horarioTurma">Horário:</label>
          <input
            type="text"
            id="horarioTurma"
            v-model="turmaLocal.horario"
            placeholder="Ex: Segunda e Quarta, 14:00-16:00"
          >
        </div>
        
        <div class="campo-formulario">
          <label for="salaTurma">Sala:</label>
          <input
            type="text"
            id="salaTurma"
            v-model="turmaLocal.sala"
            placeholder="Ex: Sala 203"
          >
        </div>
      </div>
      
      <div class="modal__rodape">
        <button class="botao-secundario" @click="fecharModal">
          Cancelar
        </button>
        <button class="botao-primario" @click="salvar">
          {{ turma ? 'Salvar Alterações' : 'Cadastrar Turma' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalTurma',
  props: {
    turma: {
      type: Object,
      default: null
    },
    professores: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      turmaLocal: this.turma 
        ? { ...this.turma } 
        : { 
            codigo: '', 
            nome: '', 
            professorId: '', 
            periodo: '', 
            horario: '', 
            sala: '' 
          }
    }
  },
  methods: {
    fecharModal() {
      this.$emit('fechar')
    },
    salvar() {
      if (!this.turmaLocal.nome || !this.turmaLocal.codigo || !this.turmaLocal.periodo) {
        alert('Preencha todos os campos obrigatórios')
        return
      }
      this.$emit('salvar', this.turmaLocal)
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
.modal--grande {
  max-width: 600px;
}

.modal__titulo {
  color: #38b2ac;
}

.botao-primario {
  background-color: #38b2ac;
  border-color: #38b2ac;
}

.botao-primario:hover {
  background-color: #2c7a7b;
}

select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
  background-color: white;
  transition: all 0.2s;
}

select:focus {
  outline: none;
  border-color: #38b2ac;
  box-shadow: 0 0 0 3px rgba(56, 178, 172, 0.1);
}
</style>