<template>
  <div class="controle-matriculas">
    <div class="controle-matriculas__cabecalho">
      <h2 class="controle-matriculas__titulo">
        <i class="fas fa-calendar-alt icone-titulo"></i>
        Controle de Período de Matrículas
      </h2>
    </div>
    
    <div class="cartoes">
      <div class="cartao">
        <div class="cartao__cabecalho">
          <i class="fas fa-toggle-on icone-cartao"></i>
          <h3 class="cartao__titulo">Status do Período</h3>
        </div>
        
        <div class="status-toggle">
          <span :class="{ 'status-ativo': matriculasAbertas }">Aberto</span>
          <label class="interruptor">
            <input 
              type="checkbox"
              :checked="matriculasAbertas"
              @change="$emit('update:matriculasAbertas', $event.target.checked); $emit('alternar-status')"
            >
            <span class="interruptor__controle"></span>
          </label>
          <span :class="{ 'status-ativo': !matriculasAbertas }">Fechado</span>
        </div>
        
        <p class="cartao__descricao">
          Quando aberto, os alunos podem se matricular em novas disciplinas.
        </p>
      </div>
      
      
    </div>
  </div>
</template>

<script>
export default {
  name: 'ControleMatriculas',
  props: {
    periodoMatriculas: {
      type: Object,
      required: true
    },
    matriculasAbertas: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      periodoLocal: { ...this.periodoMatriculas }
    }
  },
  methods: {
    salvarPeriodo() {
      this.$emit('salvar-periodo', this.periodoLocal)
    }
  }
}
</script>

<style scoped>


.controle-matriculas {
  background-color: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
   margin-bottom: 40px;
  margin-top: 70px;
  max-width: 1400px;
  margin-left: 240px;
}

.controle-matriculas__cabecalho {
  margin-bottom: 1.5rem;
}

.controle-matriculas__titulo {
  font-size: 1.25rem;
  font-weight: 600;
  color: #2d3748;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.icone-titulo {
  color: #ed8936;
}

.cartoes {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.cartao {
  background-color: white;
  border-radius: 0.75rem;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #edf2f7;
}

.cartao__cabecalho {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.icone-cartao {
  font-size: 1.25rem;
  color: #ed8936;
}

.cartao__titulo {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.status-toggle {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.status-ativo {
  font-weight: 600;
  color: #2d3748;
}

.interruptor {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

.interruptor input {
  opacity: 0;
  width: 0;
  height: 0;
}

.interruptor__controle {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e53e3e;
  transition: .4s;
  border-radius: 34px;
}

.interruptor__controle:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  transition: .4s;
  border-radius: 50%;
}

input:checked + .interruptor__controle {
  background-color: #38a169;
}

input:checked + .interruptor__controle:before {
  transform: translateX(26px);
}

.cartao__descricao {
  color: #718096;
  font-size: 0.875rem;
  margin-top: 1rem;
}

.formulario-periodo {
  margin-bottom: 1.5rem;
}

.campo-data {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .cartoes {
    grid-template-columns: 1fr;
  }
}
</style>