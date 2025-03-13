<template>
  <div class="done-page">
    <h1>Order Done</h1>
    <img src="/logo.png" />
    <h2>Your order is done. Enjoy your coffee(mai)!</h2>
    <p>________</p>
    <hr>

    <button type="button" @click="logOut">I got my order!</button>
  </div>

  <div class="mt-4" />
</template>

<script>
import { getFirestore, doc, setDoc } from 'firebase/firestore';
import { getAuth, signOut, onAuthStateChanged } from 'firebase/auth';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'DonePage',
  setup() {
    const auth = getAuth();
    const db = getFirestore();
    const router = useRouter();
    const isUserLoggedIn = ref(false);

    onMounted(() => {
      onAuthStateChanged(auth, (user) => {
        isUserLoggedIn.value = !!user;
      });
    });

    const logOut = async () => {
      try {
        await signOut(auth);
        isUserLoggedIn.value = false;

        const globalSessionRef = doc(db, 'globalSession', 'currentSession');
        await setDoc(globalSessionRef, { isLoggedIn: false }, { merge: true });

        router.push('/login');
      } catch (error) {
        console.error('Sign out error:', error);
      }
    };

    return {
      logOut,
      isUserLoggedIn
    };
  }
};
</script>

<style>

</style>
