<template>
  <div class="detalhes-turma">
    <div class="cabecalho-turma">
      <button class="botao-voltar" @click="$emit('voltar')">
        <i class="fas fa-arrow-left"></i>
      </button>
      <h2>{{ turma.nome }} - {{ turma.codigo }}</h2>
      <div class="acoes-turma">
        <button class="botao-acao" @click="$emit('abrir-modal-notas')">
          <i class="fas fa-plus"></i> Lançar Notas
        </button>
      </div>
    </div>

    <div class="conteudo-turma">
      <div class="cartoes-informacao">
        <CartaoInformacoes :turma="turma" />
        <CartaoEstatisticas :turma="turma" />
      </div>

      <TabelaAlunos 
        :alunos="turma.alunos" 
        @ordenar="ordenarAlunos"
      />
    </div>
  </div>
</template>

<script>
import CartaoInformacoes from './CartaoInformacoes.vue'
import CartaoEstatisticas from './CartaoEstatisticas.vue'
import TabelaAlunos from './TabelaAlunos.vue'

export default {
  name: 'DetalhesTurma',
  components: {
    CartaoInformacoes,
    CartaoEstatisticas,
    TabelaAlunos
  },
  props: {
    turma: {
      type: Object,
      required: true
    }
  },
  emits: ['voltar', 'abrir-modal-notas', 'ordenar'],
  methods: {
    ordenarAlunos(campo) {
      this.$emit('ordenar', campo)
    }
  }
}
</script>

<style scoped>
.detalhes-turma {
  background-color: #f5f7fa;
  padding: 20px;
  border-radius: 10px;
}

.cabecalho-turma {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 25px;
}

.botao-voltar {
  background: none;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  cursor: pointer;
  color: #555;
}

.botao-voltar:hover {
  background-color: #e0e0e0;
}

.cabecalho-turma h2 {
  color: #2c3e50;
  font-size: 22px;
  font-weight: 600;
}

.acoes-turma {
  margin-left: auto;
}

.botao-acao {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.botao-acao:hover {
  background-color: #3498db;
  color: white;
}

.cartoes-informacao {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 25px;
}
</style>