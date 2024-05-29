<template>
  <div id="app">
    <div v-if="!isLoggedIn">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <input type="text" v-model="username" placeholder="Username" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <button type="submit">Login</button>
      </form>
    </div>
    <div v-else>
      <p>Welcome, {{ username }}!</p>
      <p>Current Time: {{ currentTime }}</p>
      <button @click="logout">Logout</button>
    </div>
  </div>
</template>

<script>
import api from '@/services/api';
import { getCurrentUser } from '@/services/api';

export default {
  data() {
    return {
      username: '',
      password: '',
      isLoggedIn: false,
      currentTime: null,
    };
  },
  methods: {
    async handleLogin() {
      try {
        const response = await api.login(this.username, this.password);
        localStorage.setItem('authToken', response.data.access_token);
        this.isLoggedIn = true;
        this.fetchCurrentUser();
      } catch (error) {
        alert('Login failed: Incorrect username or password');
        console.error('Login error:', error);
      }
    },
    async fetchCurrentUser() {
      try {
        console.log('Fetching current user...');
        const token = localStorage.getItem('authToken'); // Ensure key matches
        console.log(`Token from storage: ${token}`); // Log the retrieved token for debugging
        if (!token) {
          throw new Error("No token found");
        }
        const response = await getCurrentUser(token); // Pass token to function
        this.user = response;
        this.currentTime = response.current_time; 
        console.log(`Current Time: ${this.currentTime}`);
      } catch (error) {
        console.error('Error fetching current user:', error);
      }
    },
    logout() {
      localStorage.removeItem('authToken');
      this.isLoggedIn = false;
      this.username = '';
      this.password = '';
    },
  },
}
</script>

<style>
/* Add your styles here */
</style>
