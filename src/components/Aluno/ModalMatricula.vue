<template>
  <div class="modal-fundo">
    <div class="conteudo-modal">
      <div class="cabecalho-modal">
        <h3>Confirmar Matrícula</h3>
        <button class="botao-fechar-modal" @click="$emit('cancelar')">
          <i class="fas fa-times"></i>
        </button>
      </div>
      <div class="corpo-modal">
        <p>Deseja se matricular na disciplina:</p>
        <h4>{{ disciplina.nome }} ({{ disciplina.codigo }})</h4>
        <p><strong>Professor:</strong> {{ disciplina.professor }}</p>
        <p><strong>Horário:</strong> {{ disciplina.horario }}</p>
      </div>
      <div class="rodape-modal">
        <button class="botao-cancelar" @click="$emit('cancelar')">Cancelar</button>
        <button class="botao-confirmar" @click="$emit('confirmar')">Confirmar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalMatricula',
  props: {
    disciplina: Object
  }
}
</script>

<style scoped>
.modal-fundo {
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

.conteudo-modal {
  background-color: white;
  border-radius: 10px;
  width: 100%;
  max-width: 500px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
  animation: modalAparecer 0.3s ease;
}

@keyframes modalAparecer {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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

.botao-fechar-modal {
  background: none;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #95a5a6;
  transition: all 0.2s;
}

.botao-fechar-modal:hover {
  background-color: #f0f0f0;
  color: #e74c3c;
}

.corpo-modal {
  padding: 20px;
}

.corpo-modal h4 {
  color: #2c3e50;
  margin: 10px 0;
}

.corpo-modal p {
  color: #555;
  margin-bottom: 8px;
}

.corpo-modal strong {
  font-weight: 500;
}

.rodape-modal {
  padding: 15px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.botao-cancelar,
.botao-confirmar {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.botao-cancelar {
  background-color: white;
  border: 1px solid #e0e0e0;
  color: #555;
}

.botao-cancelar:hover {
  background-color: #f0f0f0;
}

.botao-confirmar {
  background-color: #2ecc71;
  border: 1px solid #2ecc71;
  color: white;
}

.botao-confirmar:hover {
  background-color: #27ae60;
}

@media (max-width: 576px) {
  .conteudo-modal {
    width: 95%;
  }
}
</style>