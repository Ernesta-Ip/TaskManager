<!-- eslint-disable vue/multi-word-component-names
<template>
  <section class="section">
    <div class="container has-text-centered">

         <img
        src="/img/undraw_celebration_wtm8.svg"
        alt="Funny welcome"
        style="max-width: 300px; margin-bottom: 2rem;"
      />

      <h1 class="title">Welcome to Task Manager</h1>
      <p class="subtitle">Please sign in with your Google account</p>

      <div class="buttons is-centered mt-5">
        <button class="button is-primary" @click="redirectToGoogle">
        Sign in with Google
        </button>
        <button
          class="button is-light"
          @click="skipLogin"
          @mouseenter="showWarning = true"
          @mouseleave="showWarning = false"
        >
          Skip step
        </button>
      </div>

      Notification under the buttons -->
        <!-- <div class="notification-wrapper mt-4">
        <transition name="fade">
            <p
            v-show="showWarning"
            class="notification is-light"
            >
            If you skip login, you will only be able to view and create public boards accessible to all users.
            </p>
        </transition>
        </div>

    </div>
  </section>
</template>


<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '@/api';

const router = useRouter();
const showWarning = ref(false); 

function redirectToGoogle() {
  window.location.href = 'http://localhost:8001/accounts/google/login/';
}

const skip = new URLSearchParams(window.location.search).get('skipAuth');
if (skip === 'true') {
  localStorage.setItem('skipAuth', 'true');
}

function skipLogin() {
  localStorage.setItem('skipAuth', 'true');

  api.get('boards/')
    .then(res => {
      const boards = res.data;
      console.log('Boards from API:', boards);
      const first = boards.find(b => !b.is_archived && b.visibility === 'public');
      router.replace({ name: first ? 'BoardDetail' : 'Dashboard', params: { id: first?.id } });
    })
    .catch(err => {
      console.error('Failed to load boards:', err);
      router.replace({ name: 'Dashboard' });
    });
}

onMounted(() => {
  console.log('Login mounted');
});
</script>

<style scoped>
.section {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.notification-wrapper {
  position: relative;
  height: 3rem; 
}

.notification-wrapper .notification {
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: max-content;
  max-width: 100%;
  margin: 0;
}

</style> -->
