<template>
  <div class="modal-overlay" @click.self="$emit('fechar')">
    <div class="modal-conteudo">
      <header class="cabecalho-modal">
        <h3>Lançar Notas</h3>
        <button class="botao-fechar" @click="$emit('fechar')" aria-label="Fechar modal">
          <i class="fas fa-times"></i>
        </button>
      </header>

      <section class="corpo-modal">
        <div class="grupo-formulario">
          <label for="atividade">Atividade:</label>
          <select id="atividade" v-model="dadosNotas.atividade" class="input-select">
            <option disabled value="">Selecione uma atividade</option>
            <option 
              v-for="atividade in atividades" 
              :key="atividade.id" 
              :value="atividade.id"
            >
              {{ atividade.nome }}
            </option>
          </select>
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
                v-model.number="dadosNotas.notas[aluno.id]"
                placeholder="--"
              >
            </div>
          </div>
        </div>
      </section>

      <footer class="rodape-modal">
        <button class="botao-cancelar" @click="$emit('fechar')">Cancelar</button>
        <button class="botao-salvar" @click="salvarNotas" :disabled="!dadosNotas.atividade">
          Salvar Notas
        </button>
      </footer>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ModalNotas',
  props: {
    alunos: { type: Array, required: true },
    atividades: { type: Array, required: true },
    turmaId: { type: Number, required: true }
  },
  data() {
    return {
      dadosNotas: {
        atividade: '',
        notas: {}
      },
      token: '52e42938087eea9afd4ec5f4a55de85da5d4d9c9'
    }
  },
  methods: {
    async salvarNotas() {
      if (!this.dadosNotas.atividade) {
        alert('Selecione uma atividade');
        return;
      }

      const promises = []
      for (const alunoId in this.dadosNotas.notas) {
        const nota = this.dadosNotas.notas[alunoId]

        // Só envia se a nota for número válido e diferente de vazio/null
        if (nota !== null && nota !== undefined && nota !== '' && !isNaN(nota)) {
          const payload = {
            nota: parseFloat(nota).toFixed(2),
            aluno: parseInt(alunoId),
            turma: this.turmaId,
            atividade: this.dadosNotas.atividade
          }
          promises.push(
            axios.post('http://localhost:8000/api/matriculas/notas/', payload, {
              headers: {
                Authorization: `Token ${this.token}`
              }
            })
          )
        }
      }

      try {
        await Promise.all(promises)
        alert('Notas lançadas com sucesso!')
        this.$emit('fechar')
      } catch (error) {
        console.error('Erro ao lançar notas:', error)
        alert('Erro ao lançar notas.')
      }
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.48);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1100;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.modal-conteudo {
  background-color: #fff;
  border-radius: 12px;
  width: 100%;
  max-width: 650px;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  overflow: hidden;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.cabecalho-modal {
  padding: 18px 24px;
  background-color: #2c3e50;
  color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  font-size: 1.25rem;
  user-select: none;
}

.botao-fechar {
  background: transparent;
  border: none;
  color: #ecf0f1;
  font-size: 1.2rem;
  cursor: pointer;
  transition: color 0.25s ease;
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
  margin-bottom: 28px;
}

.grupo-formulario label {
  font-weight: 600;
  font-size: 0.9rem;
  color: #34495e;
  display: block;
  margin-bottom: 10px;
}

.input-select {
  width: 100%;
  padding: 12px 16px;
  border-radius: 8px;
  border: 1.8px solid #bdc3c7;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

.input-select:focus {
  outline: none;
  border-color: #2980b9;
  box-shadow: 0 0 6px #2980b9aa;
}

.tabela-notas {
  border: 1.5px solid #dfe6e9;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: inset 0 0 8px #f1f2f6;
}

.cabecalho-notas {
  display: flex;
  background-color: #ecf0f1;
  font-weight: 700;
  font-size: 0.9rem;
  color: #2d3436;
  user-select: none;
}

.cabecalho-notas > div {
  padding: 14px 20px;
}

.coluna-nome {
  flex: 3;
}

.coluna-nota {
  flex: 1.5;
  text-align: center;
}

.linha-notas {
  display: flex;
  border-top: 1px solid #dcdde1;
  background-color: #fff;
  transition: background-color 0.2s ease;
}

.linha-notas:hover {
  background-color: #f5f6fa;
}

.linha-notas > div {
  padding: 14px 20px;
  display: flex;
  align-items: center;
}

.linha-notas input {
  width: 75px;
  margin: 0 auto;
  padding: 8px 10px;
  font-size: 1rem;
  border: 1.5px solid #bdc3c7;
  border-radius: 6px;
  text-align: center;
  transition: border-color 0.3s ease;
}

.linha-notas input::placeholder {
  color: #95a5a6;
}

.linha-notas input:focus {
  outline: none;
  border-color: #2980b9;
  box-shadow: 0 0 6px #2980b9aa;
}

.rodape-modal {
  padding: 16px 24px;
  background-color: #f1f2f6;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  border-top: 1.5px solid #dcdde1;
}

.botao-cancelar, .botao-salvar {
  padding: 10px 28px;
  font-weight: 600;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  user-select: none;
  transition: background-color 0.3s ease;
}

.botao-cancelar {
  background-color: #dfe6e9;
  color: #2d3436;
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
