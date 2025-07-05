<template>
  <div class="portal-professor">
    <CabecalhoProfessor @sair="sair" />
    
    <div class="conteiner-principal">
   
      
      <main class="conteudo-principal">
        <ListaTurmas 
          v-if="!turmaSelecionada" 
          :turmas="turmas"
          @selecionar-turma="selecionarTurma"
        />
        
        <DetalhesTurma
          v-else
          :turma="turmaSelecionada"
          @voltar="turmaSelecionada = null"
          @abrir-modal-notas="mostrarModalNotas = true"
        />
      </main>
    </div>
    
    <ModalNotas
      v-if="mostrarModalNotas"
      :alunos="turmaSelecionada.alunos"
      :atividades="atividades"
      @fechar="mostrarModalNotas = false"
      @salvar="salvarNotas"
    />
  </div>
</template>

<script>
import CabecalhoProfessor from '../components/Professor/CabecalhoProfessor.vue'

import ListaTurmas from '../components/Professor/ListaTurmas.vue'
import DetalhesTurma from '../components/Professor/DetalhesTurma.vue'
import ModalNotas from '../components/Professor/ModalNotas.vue'


export default {
  name: 'PortalProfessor',
  components: {
    CabecalhoProfessor,
    ListaTurmas,
    DetalhesTurma,
    ModalNotas
  },
  data() {
    return {
      turmaSelecionada: null,
      mostrarModalNotas: false,
      turmas: [
        {
          codigo: "MAT-2023-1A",
          nome: "Matemática Avançada",
          periodo: "2023 - 1º Semestre",
          horario: "Segunda e Quarta, 14:00-16:00",
          sala: "Sala 203",
          atividades: 5,
          alunos: [
            { id: "2023001", nome: "Ana Clara Souza", nota: 8.5 },
            { id: "2023002", nome: "Bruno Oliveira", nota: 7.2 },
            { id: "2023003", nome: "Carla Mendes", nota: 9.1 },
            { id: "2023004", nome: "Daniel Costa", nota: 6.8 },
            { id: "2023005", nome: "Eduarda Santos", nota: 8.9 }
          ]
        },
        {
          codigo: "FIS-2023-2B",
          nome: "Física Moderna",
          periodo: "2023 - 2º Semestre",
          horario: "Terça e Quinta, 10:00-12:00",
          sala: "Laboratório 105",
          atividades: 3,
          alunos: [
            { id: "2023008", nome: "Helena Fernandes", nota: 9.3 },
            { id: "2023009", nome: "Igor Ribeiro", nota: 6.5 },
            { id: "2023010", nome: "Juliana Almeida", nota: 8.1 }
          ]
        },
        {
          codigo: "QUI-2024-1C",
          nome: "Química Orgânica",
          periodo: "2024 - 1º Semestre",
          horario: "Sexta, 08:00-12:00",
          sala: "Laboratório 201",
          atividades: 4,
          alunos: [
            { id: "2023011", nome: "Lucas Mendes", nota: 7.8 },
            { id: "2023012", nome: "Mariana Gonçalves", nota: 9.5 },
            { id: "2023013", nome: "Nathália Castro", nota: 8.9 },
            { id: "2023014", nome: "Otávio Rocha", nota: 6.2 }
          ]
        }
      ],
      atividades: [
        { id: "quiz1", nome: "Quiz 1 - Introdução" },
        { id: "projeto1", nome: "Projeto de Pesquisa" },
        { id: "prova1", nome: "Prova Bimestral" },
        { id: "atividade1", nome: "Atividade em Grupo" },
        { id: "trabalho1", nome: "Trabalho Final" }
      ]
    }
  },
  methods: {
    selecionarTurma(turma) {
      this.turmaSelecionada = turma
    },
    salvarNotas(dadosNotas) {
      // Encontra o aluno na turma e atualiza a nota
      this.turmaSelecionada.alunos.forEach(aluno => {
        if (dadosNotas.notas[aluno.id] !== undefined) {
          aluno.nota = parseFloat(dadosNotas.notas[aluno.id]) || null
        }
      })
      this.mostrarModalNotas = false
      alert('Notas salvas com sucesso!')
    },
    sair() {
      this.$router.push('/login')
    }
  }
}

</script>

<style scoped>
.portal-professor {
  font-family: 'Poppins', sans-serif;
  background-color: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.conteiner-principal {
  display: flex;
  flex: 1;
}

.conteudo-principal {
  flex: 1;
  padding: 20px;
  background-color: #f5f7fa;
}
</style>