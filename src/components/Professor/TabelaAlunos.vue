<template>
  <div class="tabela-alunos-container">
    <div class="cabecalho-tabela">
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
        <div class="coluna status">Status</div>
        <div class="coluna nota">Nota</div>
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
        <div v-for="(matricula, index) in matriculasOrdenadas" :key="matricula.id" class="linha-tabela">
          <div class="coluna numero">{{ index + 1 }}</div>
          <div class="coluna nome">
            {{ getNomeAluno(matricula.aluno) }}
          </div>
          <div class="coluna status">
            <span class="badge-status" :class="matricula.status.toLowerCase()">
              {{ matricula.status }}
            </span>
          </div>
          <div class="coluna nota">
            <span class="badge-nota" :class="classeNota(matricula.media_final)">
              {{ matricula.media_final !== null ? Number(matricula.media_final).toFixed(1) : '-' }}
            </span>
          </div>
        </div>
      </template>
    </div>

    <div v-if="matriculasFiltradas.length > 0" class="media-turma">
      Média da turma: <strong>{{ mediaTurma.toFixed(2) }}</strong>
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
      direcaoOrdenacao: 'asc'
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
          valorA = a.media_final !== null ? Number(a.media_final) : -1
          valorB = b.media_final !== null ? Number(b.media_final) : -1
        }

        if (valorA < valorB) return this.direcaoOrdenacao === 'asc' ? -1 : 1
        if (valorA > valorB) return this.direcaoOrdenacao === 'asc' ? 1 : -1
        return 0
      })
    },
    mediaTurma() {
      const notas = this.matriculasFiltradas
        .map(m => (m.media_final !== null ? Number(m.media_final) : null))
        .filter(n => n !== null)
      if (notas.length === 0) return 0
      const soma = notas.reduce((acc, cur) => acc + cur, 0)
      return soma / notas.length
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
    }
  }
}
</script>

<style scoped>
.tabela-alunos-container {
  background-color: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-top: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #2c3e50;
}

.cabecalho-tabela {
  display: flex;
  justify-content: right;
  margin-bottom: 20px;
}


.acoes-tabela {
  display: flex;
  gap: 12px;
}

.botao-ordenar,
.botao-atualizar {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  border: 1px solid #2980b9;
  background-color: #f0f7fb;
  color: #2980b9;
  transition: background-color 0.3s ease;
}

.botao-ordenar:hover,
.botao-atualizar:hover {
  background-color: #d0e7f5;
}

.tabela-alunos {
  width: 100%;
  border-collapse: collapse;
}

.linha-tabela {
  display: flex;
  border-bottom: 1px solid #e1e8ed;
  padding: 12px 0;
  align-items: center;
}

.linha-tabela.cabecalho {
  font-weight: 700;
  font-size: 14px;
  color: #506d85;
  background-color: #f9fbfd;
  border-bottom: 2px solid #2980b9;
}

.linha-carregando,
.linha-erro,
.linha-vazia {
  padding: 20px;
  text-align: center;
  font-style: italic;
  color: #7f8c8d;
}

.linha-erro {
  color: #e74c3c;
  font-weight: 700;
}

.coluna {
  padding: 0 12px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  min-height: 40px;
}

.coluna-cheia {
  width: 100%;
  text-align: center;
}

.numero {
  width: 40px;
  justify-content: center;
  color: #34495e;
}

.nome {
  flex: 2;
  font-weight: 600;
  font-size: 15px;
}

.status,
.nota {
  flex: 1;
  font-size: 14px;
  color: #34495e;
}

.badge-nota,
.badge-status {
  padding: 6px 10px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
  text-align: center;
  min-width: 55px;
  display: inline-block;
}

.badge-nota.excelente {
  background-color: #e6f4ea;
  color: #27ae60;
}

.badge-nota.boa {
  background-color: #e3f2fd;
  color: #2980b9;
}

.badge-nota.media {
  background-color: #fff9e5;
  color: #f39c12;
}

.badge-nota.baixa {
  background-color: #fceaea;
  color: #c0392b;
}

.badge-nota.sem-nota {
  background-color: #ecf0f1;
  color: #7f8c8d;
}

.badge-status.ativo {
  background-color: #d5f4dd;
  color: #27ae60;
  font-weight: 700;
}

.badge-status.inativo {
  background-color: #f9d6d5;
  color: #c0392b;
  font-weight: 700;
}

.badge-status.trancado {
  background-color: #fcf4d5;
  color: #f39c12;
  font-weight: 700;
}

.media-turma {
  margin-top: 18px;
  font-size: 17px;
  font-weight: 700;
  color: #34495e;
  text-align: right;
}
</style>