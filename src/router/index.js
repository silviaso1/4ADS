import { createRouter, createWebHistory } from 'vue-router'

// Importe as páginas existentes
import Login from '../Pages/Login.vue'
import Admin from '../Pages/Admin.vue'
import Alunos from '../Pages/Alunos.vue'
import Professor from '../Pages/Professor.vue'

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/admin',
    name: 'Admin',
    component: Admin
  },
  {
    path: '/alunos',
    name: 'Alunos',
    component: Alunos
  },
  {
    path: '/professor',
    name: 'Professor',
    component: Professor
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
