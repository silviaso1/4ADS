<template>
  <div class="gerenciamento">
    <div class="gerenciamento__cabecalho">
      <button class="botao-primario" @click="$emit('abrir-modal-turma', null)">
        <i class="fas fa-plus"></i>
        Nova Turma
      </button>
    </div>
    
    <div class="barra-pesquisa">
      <i class="fas fa-search icone-pesquisa"></i>
      <input
        type="text"
        class="campo-pesquisa"
        placeholder="Pesquisar turmas..."
        v-model="termoPesquisa"
      >
    </div>
    
    <div class="tabela-wrapper">
      <table class="tabela">
        <thead>
          <tr>
            <th class="coluna-codigo">Código</th>
            <th class="coluna-nome">Nome</th>
            <th class="coluna-professor">Professor</th>
            <th class="coluna-periodo">Período</th>
            <th class="coluna-acoes">Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="turma in turmasFiltradas" :key="turma.id">
            <td class="coluna-codigo">{{ turma.codigo }}</td>
            <td class="coluna-nome">{{ turma.nome }}</td>
            <td class="coluna-professor">{{ nomeProfessor(turma.professor) }}</td>
            <td class="coluna-periodo">{{ turma.periodo }}</td>
            <td class="coluna-acoes">
              <button 
                class="botao-icone botao-editar"
                @click="$emit('abrir-modal-turma', turma)"
                aria-label="Editar turma"
              >
                <i class="fas fa-edit"></i>
              </button>
              <button 
                class="botao-icone botao-excluir"
                @click="$emit('confirmar-exclusao', 'turma', turma.codigo)"
                aria-label="Excluir turma"
              >
                <i class="fas fa-trash-alt"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="loading" class="sem-resultados">
        <i class="fas fa-spinner fa-spin icone-vazio"></i>
        <p>Carregando turmas...</p>
      </div>

      <div v-else-if="!loading && turmasFiltradas.length === 0" class="sem-resultados">
        <i class="fas fa-door-closed icone-vazio"></i>
        <p>Nenhuma turma encontrada</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GerenciamentoTurmas',
  props: {
    professores: {
      type: Array,
      required: true
    }
  },
  data() {
    return {
      turmas: [],
      termoPesquisa: '',
      loading: false,
      erro: ''
    }
  },
  computed: {
    turmasFiltradas() {
      const termo = this.termoPesquisa.toLowerCase()
      return this.turmas.filter(turma => {
        return (
          (turma.codigo || '').toLowerCase().includes(termo) ||
          (turma.nome || '').toLowerCase().includes(termo) ||
          this.nomeProfessor(turma.professor).toLowerCase().includes(termo) ||
          (turma.periodo || '').toLowerCase().includes(termo)
        )
      })
    }
  },
  methods: {
    nomeProfessor(professorId) {
      if (!professorId) return 'Não atribuído'
      const prof = this.professores.find(p => p.id === professorId)
      return prof ? prof.nome : `ID ${professorId}`
    },
    async carregarTurmas() {
      this.loading = true
      this.erro = ''
      try {
        const response = await axios.get('http://localhost:8000/api/turmas/')
        this.turmas = response.data
      } catch (error) {
        this.erro = 'Erro ao carregar turmas.'
        console.error(error)
      } finally {
        this.loading = false
      }
    }
  },
  created() {
    this.carregarTurmas()
  }
}
</script>

<style scoped>
.gerenciamento {
  background: #ffffff;
  border-radius: 12px;
  padding: 32px 40px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.06);
  margin: 24px auto;
  max-width: 1400px;
  margin-left: 240px;
  margin-top: 70px;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
}

.gerenciamento__cabecalho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.titulo-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
}

.icone-titulo-container {
  width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(67, 97, 238, 0.2);
}

.icone-titulo {
  color: white;
  font-size: 1.2rem;
}

.gerenciamento__titulo {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

.botao-primario {
 background: #2563eb;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}


.barra-pesquisa {
  position: relative;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
}

.icone-pesquisa {
  position: absolute;
  left: 1rem;
  color: #718096;
}

.campo-pesquisa {
  width: 100%;
  padding: 14px 20px 14px 40px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.3s;
  background-color: #f8fafc;
}

.campo-pesquisa:focus {
  outline: none;
  border-color: #4361ee;
  box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.1);
  background-color: white;
}

.contador-resultados {
  position: absolute;
  right: 16px;
  font-size: 0.85rem;
  color: #718096;
}

.tabela-wrapper {
  overflow-x: auto;
  border-radius: 12px;
  border: 1px solid #edf2f7;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.tabela {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.tabela th {
  background-color: #f8fafc;
  color: #4a5568;
  font-weight: 600;
  text-align: left;
  padding: 16px 20px;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #e2e8f0;
}

.tabela td {
  padding: 16px 20px;
  border-bottom: 1px solid #edf2f7;
  color: #4a5568;
  font-size: 0.95rem;
  vertical-align: middle;
}

.tabela tr:last-child td {
  border-bottom: none;
}

.tabela tr:hover {
  background-color: #f8fafc;
}

.sort-icon {
  margin-left: 8px;
  color: #cbd5e0;
  font-size: 0.8rem;
  cursor: pointer;
  transition: color 0.2s;
}

.sort-icon:hover {
  color: #718096;
}

.badge-matricula {
  background-color: #e0e7ff;
  color: #4338ca;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.aluno-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-placeholder {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #3a0ca3;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.periodo-badge {
  background-color: #ecfdf5;
  color: #065f46;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.coluna-acoes {
  width: 160px;
}

.acoes-wrapper {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.botao-icone {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  color: white;
  position: relative;
}

.botao-icone:hover {
  transform: translateY(-2px);
}

.botao-icone:active {
  transform: translateY(0);
}

.botao-icone::after {
  content: attr(data-tooltip);
  position: absolute;
  bottom: -30px;
  left: 50%;
  transform: translateX(-50%);
  background: #2d3748;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.75rem;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s;
  white-space: nowrap;
}

.botao-icone:hover::after {
  opacity: 1;
}

.botao-editar {
  background-color: #3b82f6;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.3);
}

.botao-editar:hover {
  background-color: #2563eb;
}

.botao-excluir {
  background-color: #ef4444;
  box-shadow: 0 2px 6px rgba(239, 68, 68, 0.3);
}

.botao-excluir:hover {
  background-color: #dc2626;
}

.botao-visualizar {
  background-color: #10b981;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3);
}

.botao-visualizar:hover {
  background-color: #059669;
}

.sem-resultados {
  padding: 3rem 1rem;
  text-align: center;
  color: #64748b;
}

.empty-state {
  max-width: 400px;
  margin: 0 auto;
  padding: 2rem 0;
}

.icone-vazio {
  font-size: 3.5rem;
  margin-bottom: 1.5rem;
  color: #e2e8f0;
  background: linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.empty-state h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.empty-state p {
  margin-bottom: 1.5rem;
  color: #64748b;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .gerenciamento {
    padding: 1.5rem;
    margin: 16px;
  }
  
  .gerenciamento__cabecalho {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  
  .barra-pesquisa {
    flex-direction: column;
    align-items: stretch;
  }
  
  .contador-resultados {
    position: static;
    margin-top: 8px;
    align-self: flex-end;
  }
  
  .empty-state {
    padding: 1rem 0;
  }
}
</style>