<template>
  <div class="modal-overlay" @click.self="$emit('fechar')">
    <div class="modal-conteudo">
      <div class="cabecalho-modal">
        <h3>Registrar Frequência</h3>
        <button class="botao-fechar" @click="$emit('fechar')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="corpo-modal">
        <div class="grupo-formulario">
          <label for="data-frequencia">Data:</label>
          <input 
            type="date" 
            id="data-frequencia" 
            v-model="dadosFrequencia.data"
          >
        </div>
        
        <div class="tabela-frequencia">
          <div class="cabecalho-frequencia">
            <div class="coluna-nome">Aluno</div>
            <div class="coluna-status">Presente</div>
          </div>
          
          <div 
            v-for="aluno in alunos" 
            :key="aluno.id" 
            class="linha-frequencia"
          >
            <div class="coluna-nome">{{ aluno.nome }}</div>
            <div class="coluna-status">
              <label class="switch">
                <input 
                  type="checkbox" 
                  v-model="dadosFrequencia.presencas[aluno.id]"
                >
                <span class="slider round"></span>
              </label>
            </div>
          </div>
        </div>
      </div>
      
      <div class="rodape-modal">
        <button class="botao-cancelar" @click="$emit('fechar')">
          Cancelar
        </button>
        <button class="botao-salvar" @click="salvarFrequencia">
          Salvar Frequência
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalFrequencia',
  props: {
    alunos: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      dadosFrequencia: {
        data: new Date().toISOString().split('T')[0],
        presencas: {}
      }
    }
  },
  methods: {
    salvarFrequencia() {
      this.$emit('salvar', this.dadosFrequencia)
      this.$emit('fechar')
    }
  }
}
</script>

<style scoped>
/* Estilos similares ao ModalNotas com pequenas adaptações */
.switch {
  position: relative;
  display: inline-block;
  width: 50px;
  height: 24px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e74c3c;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2ecc71;
}

input:checked + .slider:before {
  transform: translateX(26px);
}

.slider.round {
  border-radius: 24px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>