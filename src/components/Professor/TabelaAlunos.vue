<template>
  <div class="tabela-alunos-container">
    <div class="cabecalho-tabela">
      <h3>Alunos Matriculados</h3>
      <div class="acoes-tabela">
        <button class="botao-ordenar" @click="ordenar('nome')">
          <i class="fas fa-sort-alpha-down"></i> Nome
        </button>
        <button class="botao-ordenar" @click="ordenar('nota')">
          <i class="fas fa-sort-numeric-down"></i> Nota
        </button>
      </div>
    </div>
    
    <div class="tabela-alunos">
      <div class="linha-tabela cabecalho">
        <div class="coluna numero">#</div>
        <div class="coluna nome">Nome</div>
        <div class="coluna matricula">Matrícula</div>
        <div class="coluna nota">Nota</div>
      </div>
      
      <div 
        v-for="(aluno, indice) in alunosOrdenados" 
        :key="aluno.id" 
        class="linha-tabela"
      >
        <div class="coluna numero">{{ indice + 1 }}</div>
        <div class="coluna nome">{{ aluno.nome }}</div>
        <div class="coluna matricula">{{ aluno.id }}</div>
        <div class="coluna nota">
          <span class="badge-nota" :class="classeNota(aluno.nota)">
            {{ aluno.nota !== null ? aluno.nota.toFixed(1) : '-' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TabelaAlunos',
  props: {
    alunos: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      campoOrdenacao: 'nome',
      direcaoOrdenacao: 'asc'
    }
  },
  computed: {
    alunosOrdenados() {
      return [...this.alunos].sort((a, b) => {
        let valorA, valorB
        
        if (this.campoOrdenacao === 'nome') {
          valorA = a.nome.toLowerCase()
          valorB = b.nome.toLowerCase()
        } else {
          valorA = a.nota !== null ? a.nota : -1
          valorB = b.nota !== null ? b.nota : -1
        }
        
        if (valorA < valorB) return this.direcaoOrdenacao === 'asc' ? -1 : 1
        if (valorA > valorB) return this.direcaoOrdenacao === 'asc' ? 1 : -1
        return 0
      })
    }
  },
  methods: {
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
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
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
}

.acoes-tabela {
  display: flex;
  gap: 10px;
}

.botao-ordenar {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 12px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.botao-ordenar:hover {
  background-color: #f0f0f0;
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

.coluna {
  padding: 12px 10px;
}

.numero {
  width: 50px;
}

.nome {
  flex: 2;
}

.matricula {
  flex: 1;
}

.nota {
  width: 100px;
}

.badge-nota {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
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
</style>