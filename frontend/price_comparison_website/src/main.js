// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // 如果使用路由
import { createPinia } from 'pinia';
import axios from "axios"; // 如果使用 Pinia 作为状态管理

import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css';

const app = createApp(App);

app.use(ElementPlus);
app.use(router); // 如果使用路由
app.use(createPinia()); // 如果使用 Pinia

app.mount('#app');




