<template>
  <div class="modal-overlay" @click.self="fecharModal">
    <div class="modal modal--pequeno">
      <div class="modal__cabecalho">
        <h3 class="modal__titulo">
          <i class="fas fa-exclamation-triangle icone-alerta"></i>
          Confirmar Exclusão
        </h3>
        <button class="modal__fechar" @click="fecharModal" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </div>
      
      <div class="modal__corpo">
        <p class="mensagem-confirmacao">
          Tem certeza que deseja excluir este {{ textoItem }}? Esta ação não pode ser desfeita.
        </p>
      </div>
      
      <div class="modal__rodape">
        <button class="botao-secundario" @click="fecharModal">
          Cancelar
        </button>
        <button class="botao-perigo" @click="confirmar">
          <i class="fas fa-trash-alt"></i>
          Confirmar Exclusão
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalConfirmacao',
  props: {
    tipo: {
      type: String,
      required: true
    }
  },
  computed: {
    textoItem() {
      switch(this.tipo) {
        case 'aluno': return 'aluno'
        case 'professor': return 'professor'
        case 'turma': return 'turma'
        default: return 'item'
      }
    }
  },
  methods: {
    fecharModal() {
      this.$emit('cancelar')
    },
    confirmar() {
      this.$emit('confirmar')
      this.fecharModal()
    }
  }
}
</script>

<style scoped>
.modal--pequeno {
  max-width: 450px;
}

.modal__titulo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #e53e3e;
}

.icone-alerta {
  font-size: 1.25rem;
}

.mensagem-confirmacao {
  color: #4a5568;
  line-height: 1.5;
  text-align: center;
}

.botao-perigo {
  background-color: #e53e3e;
  border: 1px solid #e53e3e;
  color: white;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.botao-perigo:hover {
  background-color: #c53030;
}
</style>