import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // importa o router
import './style.css'
import '@fortawesome/fontawesome-free/css/all.min.css'

const app = createApp(App)

app.use(router) // usa o router

app.mount('#app')
