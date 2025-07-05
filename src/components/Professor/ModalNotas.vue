<template>
  <div class="modal-overlay" @click.self="$emit('fechar')">
    <div class="modal-conteudo">
      <div class="cabecalho-modal">
        <h3>Lançar Notas</h3>
        <button class="botao-fechar" @click="$emit('fechar')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="corpo-modal">
        <div class="grupo-formulario">
          <label for="atividade">Atividade:</label>
          <select id="atividade" v-model="dadosNotas.atividade">
            <option value="">Selecione uma atividade</option>
            <option 
              v-for="atividade in atividades" 
              :key="atividade.id" 
              :value="atividade.id"
            >
              {{ atividade.nome }}
            </option>
          </select>
        </div>
        
        <div class="grupo-formulario">
          <label for="data">Data:</label>
          <input type="date" id="data" v-model="dadosNotas.data">
        </div>
        
        <div class="tabela-notas">
          <div class="cabecalho-notas">
            <div class="coluna-nome">Aluno</div>
            <div class="coluna-nota">Nota (0-10)</div>
          </div>
          
          <div 
            v-for="aluno in alunos" 
            :key="aluno.id" 
            class="linha-notas"
          >
            <div class="coluna-nome">{{ aluno.nome }}</div>
            <div class="coluna-nota">
              <input 
                type="number" 
                min="0" 
                max="10" 
                step="0.1" 
                v-model="dadosNotas.notas[aluno.id]"
                placeholder="0.0"
              >
            </div>
          </div>
        </div>
      </div>
      
      <div class="rodape-modal">
        <button class="botao-cancelar" @click="$emit('fechar')">
          Cancelar
        </button>
        <button class="botao-salvar" @click="salvarNotas">
          Salvar Notas
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalNotas',
  props: {
    alunos: {
      type: Array,
      required: true
    },
    atividades: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dadosNotas: {
        atividade: '',
        data: new Date().toISOString().split('T')[0],
        notas: {}
      }
    }
  },
  methods: {
    salvarNotas() {
      // Validar dados antes de emitir
      if (!this.dadosNotas.atividade) {
        alert('Selecione uma atividade');
        return;
      }
      
      this.$emit('salvar', this.dadosNotas);
      this.$emit('fechar');
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
}

.modal-conteudo {
  background-color: white;
  border-radius: 10px;
  width: 100%;
  max-width: 700px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}

.cabecalho-modal {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.cabecalho-modal h3 {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
}

.botao-fechar {
  background: none;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  color: #95a5a6;
}

.botao-fechar:hover {
  background-color: #f0f0f0;
}

.corpo-modal {
  padding: 20px;
}

.grupo-formulario {
  margin-bottom: 20px;
}

.grupo-formulario label {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
  font-weight: 500;
}

.grupo-formulario select,
.grupo-formulario input[type="date"] {
  width: 100%;
  padding: 10px 15px;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
}

.tabela-notas {
  margin-top: 20px;
  border: 1px solid #eee;
  border-radius: 6px;
}

.cabecalho-notas {
  display: flex;
  background-color: #f8f9fa;
  font-weight: 500;
  font-size: 13px;
}

.cabecalho-notas div {
  padding: 10px 15px;
}

.coluna-nome {
  flex: 2;
}

.coluna-nota {
  flex: 1;
}

.linha-notas {
  display: flex;
  border-bottom: 1px solid #eee;
  background-color: white;
}

.linha-notas:last-child {
  border-bottom: none;
}

.linha-notas div {
  padding: 12px 15px;
  display: flex;
  align-items: center;
}

.linha-notas input {
  width: 80px;
  padding: 8px 10px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.rodape-modal {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.botao-cancelar {
  padding: 10px 20px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  cursor: pointer;
}

.botao-salvar {
  padding: 10px 20px;
  background-color: #3498db;
  border: 1px solid #3498db;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

.botao-salvar:hover {
  background-color: #2980b9;
}
</style>