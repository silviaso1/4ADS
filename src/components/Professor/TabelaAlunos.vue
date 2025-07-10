<template>
  <div class="tabela-alunos-container">
    <div class="cabecalho-tabela">
      <h3>Alunos Matriculados na Turma {{ turmaAtual.codigo }}</h3>
      <div class="acoes-tabela">
        <button class="botao-ordenar" @click="ordenar('nome')">
          <i class="fas fa-sort-alpha-down"></i> Nome
        </button>
        <button class="botao-ordenar" @click="ordenar('nota')">
          <i class="fas fa-sort-numeric-down"></i> Nota
        </button>
        <button class="botao-atualizar" @click="carregarDados">
          <i class="fas fa-sync-alt"></i> Atualizar
        </button>
      </div>
    </div>
    
    <div class="tabela-alunos">
      <div class="linha-tabela cabecalho">
        <div class="coluna numero">#</div>
        <div class="coluna nome">Nome</div>
        <div class="coluna matricula">Matrícula</div>
        <div class="coluna status">Status</div>
        <div class="coluna nota">Nota</div>
        <div class="coluna acoes">Ações</div>
      </div>
      
      <div v-if="carregando" class="linha-carregando">
        <div class="coluna-cheia">Carregando dados...</div>
      </div>
      
      <div v-else-if="erro" class="linha-erro">
        <div class="coluna-cheia">{{ erro }}</div>
      </div>
      
      <div v-else-if="matriculasFiltradas.length === 0" class="linha-vazia">
        <div class="coluna-cheia">Nenhum aluno matriculado nesta turma</div>
      </div>
      
      <template v-else>
        <div 
          v-for="(matricula, indice) in matriculasOrdenadas" 
          :key="matricula.id" 
          class="linha-tabela"
        >
          <div class="coluna numero">{{ indice + 1 }}</div>
          <div class="coluna nome">{{ getNomeAluno(matricula.aluno) }}</div>
          <div class="coluna matricula">{{ matricula.aluno }}</div>
          <div class="coluna status">
            <span class="badge-status" :class="matricula.status.toLowerCase()">
              {{ matricula.status }}
            </span>
          </div>
          <div class="coluna nota">
            <span class="badge-nota" :class="classeNota(matricula.media_final)">
              {{ matricula.media_final !== null ? matricula.media_final.toFixed(1) : '-' }}
            </span>
          </div>
          <div class="coluna acoes">
            <button class="botao-acao" @click="editarNota(matricula)">
              <i class="fas fa-edit"></i>
            </button>
          </div>
        </div>
      </template>
    </div>

    <!-- Modal para edição de nota -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="fecharModal">
      <div class="modal">
        <div class="modal-cabecalho">
          <h3>Editar Nota</h3>
          <button class="modal-fechar" @click="fecharModal">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div class="modal-corpo">
          <div class="campo-formulario">
            <label>Aluno:</label>
            <p>{{ alunoEditando.nome }}</p>
          </div>
          <div class="campo-formulario">
            <label for="novaNota">Nova Nota:</label>
            <input
              id="novaNota"
              type="number"
              v-model="novaNota"
              min="0"
              max="10"
              step="0.1"
              placeholder="0.0 a 10.0"
            >
          </div>
        </div>
        <div class="modal-rodape">
          <button class="botao-secundario" @click="fecharModal">Cancelar</button>
          <button class="botao-primario" @click="salvarNota" :disabled="salvando">
            {{ salvando ? 'Salvando...' : 'Salvar' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TabelaAlunosTurma',
  props: {
    turmaId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      turmaAtual: {},
      matriculas: [],
      alunos: [],
      carregando: false,
      erro: null,
      campoOrdenacao: 'nome',
      direcaoOrdenacao: 'asc',
      modalAberto: false,
      alunoEditando: {},
      matriculaEditando: {},
      novaNota: null,
      salvando: false
    }
  },
  computed: {
    matriculasFiltradas() {
      return this.matriculas.filter(matricula => matricula.turma === this.turmaId)
    },
    matriculasOrdenadas() {
      return [...this.matriculasFiltradas].sort((a, b) => {
        let valorA, valorB
        
        if (this.campoOrdenacao === 'nome') {
          valorA = this.getNomeAluno(a.aluno).toLowerCase()
          valorB = this.getNomeAluno(b.aluno).toLowerCase()
        } else {
          valorA = a.media_final !== null ? a.media_final : -1
          valorB = b.media_final !== null ? b.media_final : -1
        }
        
        if (valorA < valorB) return this.direcaoOrdenacao === 'asc' ? -1 : 1
        if (valorA > valorB) return this.direcaoOrdenacao === 'asc' ? 1 : -1
        return 0
      })
    }
  },
  created() {
    this.carregarDados()
  },
  methods: {
    async carregarDados() {
      this.carregando = true
      this.erro = null
      
      try {
        await Promise.all([
          this.carregarTurmaAtual(),
          this.carregarMatriculas(),
          this.carregarAlunos()
        ])
      } catch (error) {
        this.erro = 'Erro ao carregar dados. Tente novamente.'
        console.error('Erro ao carregar dados:', error)
      } finally {
        this.carregando = false
      }
    },
    
    async carregarTurmaAtual() {
      try {
        const response = await axios.get(`http://localhost:8000/api/turmas/${this.turmaId}/`)
        this.turmaAtual = response.data
      } catch (error) {
        console.error('Erro ao carregar turma:', error)
        throw error
      }
    },
    
    async carregarMatriculas() {
      try {
        const response = await axios.get('http://localhost:8000/api/matriculas/')
        this.matriculas = response.data
      } catch (error) {
        console.error('Erro ao carregar matrículas:', error)
        throw error
      }
    },
    
    async carregarAlunos() {
      try {
        const response = await axios.get('http://localhost:8000/api/usuarios/')
        this.alunos = response.data.filter(user => user.tipo === 'aluno')
      } catch (error) {
        console.error('Erro ao carregar alunos:', error)
        throw error
      }
    },
    
    getNomeAluno(idAluno) {
      const aluno = this.alunos.find(a => a.id === idAluno)
      return aluno ? aluno.nome : 'Aluno não encontrado'
    },
    
    ordenar(campo) {
      if (this.campoOrdenacao === campo) {
        this.direcaoOrdenacao = this.direcaoOrdenacao === 'asc' ? 'desc' : 'asc'
      } else {
        this.campoOrdenacao = campo
        this.direcaoOrdenacao = 'asc'
      }
    },
    
    classeNota(nota) {
      if (nota === null) return 'sem-nota'
      if (nota >= 9) return 'excelente'
      if (nota >= 7) return 'boa'
      if (nota >= 5) return 'media'
      return 'baixa'
    },
    
    editarNota(matricula) {
      this.matriculaEditando = matricula
      this.alunoEditando = this.alunos.find(a => a.id === matricula.aluno) || {}
      this.novaNota = matricula.media_final
      this.modalAberto = true
    },
    
    fecharModal() {
      this.modalAberto = false
      this.matriculaEditando = {}
      this.alunoEditando = {}
      this.novaNota = null
    },
    
    async salvarNota() {
      this.salvando = true
      
      try {
        const dadosAtualizados = {
          ...this.matriculaEditando,
          media_final: this.novaNota !== null ? parseFloat(this.novaNota) : null
        }
        
        await axios.put(
          `http://localhost:8000/api/matriculas/${this.matriculaEditando.id}/`,
          dadosAtualizados
        )
        
        // Atualiza a matrícula localmente
        const index = this.matriculas.findIndex(m => m.id === this.matriculaEditando.id)
        if (index !== -1) {
          this.matriculas.splice(index, 1, dadosAtualizados)
        }
        
        this.fecharModal()
      } catch (error) {
        console.error('Erro ao salvar nota:', error)
        alert('Erro ao salvar nota. Tente novamente.')
      } finally {
        this.salvando = false
      }
    }
  }
}
</script>

<style scoped>
.tabela-alunos-container {
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
  margin: 20px 0;
}

.cabecalho-tabela {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cabecalho-tabela h3 {
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
  margin: 0;
}

.acoes-tabela {
  display: flex;
  gap: 10px;
}

.botao-ordenar, .botao-atualizar {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.botao-ordenar:hover, .botao-atualizar:hover {
  background-color: #f0f0f0;
}

.botao-atualizar {
  background-color: #f8f9fa;
}

.tabela-alunos {
  width: 100%;
}

.linha-tabela {
  display: flex;
  border-bottom: 1px solid #eee;
}

.linha-tabela.cabecalho {
  font-weight: 600;
  font-size: 13px;
  color: #7f8c8d;
  background-color: #f8f9fa;
}

.linha-carregando, .linha-erro, .linha-vazia {
  padding: 15px;
  text-align: center;
  color: #666;
}

.linha-erro {
  color: #e74c3c;
}

.coluna {
  padding: 12px 10px;
  display: flex;
  align-items: center;
}

.coluna-cheia {
  width: 100%;
  text-align: center;
}

.numero {
  width: 50px;
}

.nome {
  flex: 2;
}

.matricula, .status, .nota {
  flex: 1;
}

.acoes {
  width: 80px;
}

.badge-nota, .badge-status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  text-align: center;
  min-width: 50px;
}

.badge-nota.excelente {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-nota.boa {
  background-color: #e3f2fd;
  color: #1565c0;
}

.badge-nota.media {
  background-color: #fff8e1;
  color: #ff8f00;
}

.badge-nota.baixa {
  background-color: #ffebee;
  color: #c62828;
}

.badge-nota.sem-nota {
  background-color: #f5f5f5;
  color: #757575;
}

.badge-status.ativo {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.badge-status.inativo {
  background-color: #ffebee;
  color: #c62828;
}

.badge-status.trancado {
  background-color: #fff8e1;
  color: #ff8f00;
}

.botao-acao {
  background: none;
  border: none;
  color: #3498db;
  cursor: pointer;
  font-size: 14px;
  padding: 5px;
}

.botao-acao:hover {
  color: #2980b9;
}

/* Modal styles */
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

.modal {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.modal-cabecalho h3 {
  margin: 0;
  font-size: 18px;
  color: #2c3e50;
}

.modal-fechar {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #7f8c8d;
}

.modal-corpo {
  margin-bottom: 20px;
}

.campo-formulario {
  margin-bottom: 15px;
}

.campo-formulario label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #2c3e50;
}

.campo-formulario input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.modal-rodape {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.botao-primario {
  background: #3498db;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.botao-primario:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
}

.botao-secundario {
  background: #ecf0f1;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}
</style>