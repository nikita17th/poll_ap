import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:5000';

const app = createApp(App);

app.config.globalProperties.$axios = axios;
const baseFrontendUrl = `${window.location.protocol}//${window.location.hostname}${window.location.port ? ':' + window.location.port : ''}`;
app.config.globalProperties.$baseUrl = baseFrontendUrl;
app.use(router);

app.mount('#app');