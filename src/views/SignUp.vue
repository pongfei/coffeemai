<template>
  <div class="signup-container">
    <div class="image-side">
      <img src="https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg"
           alt="Coffee" class="background-image" />
      <p class="quote">"Espress Yourself."</p>
    </div>

    <div class="form-side">
      <h2>Create Account</h2>
      <br>
      <p>Sign up to start ordering your favorite coffee</p>

      <!-- Email -->
      <div class="input-group">
        <input type="email" class="form-control" placeholder="Email" v-model="formData.email" />
      </div>

      <!-- Password -->
      <div class="input-group">
        <input type="password" class="form-control" placeholder="Password" v-model="formData.password" />
      </div>

      <!-- Confirm Password -->
      <div class="input-group">
        <input type="password" class="form-control" placeholder="Confirm Password" v-model="formData.confirmPassword" />
      </div>

      <!-- Health Condition (Checkboxes) -->
      <label for="healthCondition" class="form-label">Health Condition (If Any)</label>
      <div class="checkbox-group">
        <label><input type="checkbox" value="Sleep Disorder" v-model="formData.healthCondition" /> Sleep Disorder</label>
        <label><input type="checkbox" value="Lactose Intolerance" v-model="formData.healthCondition" /> Lactose Intolerance</label>
        <label><input type="checkbox" value="Diabetes" v-model="formData.healthCondition" /> Diabetes</label>
        <label><input type="checkbox" value="High Pressure" v-model="formData.healthCondition" /> High Pressure</label>
        <label><input type="checkbox" value="Heart Disease" v-model="formData.healthCondition" /> Heart Disease</label>
        <label><input type="checkbox" value="Gas Reflux" v-model="formData.healthCondition" /> Gas Reflux</label>
        <label><input type="checkbox" value="Liver Disease" v-model="formData.healthCondition" /> Liver Disease</label>
      </div>

      <!-- Age -->
      <div class="input-group">
        <input type="number" class="form-control" placeholder="Age" v-model="formData.ageGroup" />
      </div>

      <!-- Preferences -->
      <label for="preferenceCaffeine" class="form-label">Preference (Caffeine)</label>
      <div class="input-group">
        <select id="preferenceCaffeine" class="form-control" v-model="formData.preferenceCaffeine">
          <option value=1>Light</option>
          <option value=2>Medium</option>
          <option value=3>Strong</option>
        </select>
      </div>

      <label for="preferenceSweet" class="form-label">Preference (Sweet)</label>
      <div class="input-group">
        <select id="preferenceSweet" class="form-control" v-model="formData.preferenceSweet">
          <option value=0>No Sweet</option>
          <option value=1>Less Sweet</option>
          <option value=2>Sweet</option>
          <option value=3>More Sweet</option>
        </select>
      </div>

      <label for="preferenceCream" class="form-label">Preference (Cream)</label>
      <div class="input-group">
        <select id="preferenceCream" class="form-control" v-model="formData.preferenceCream">
          <option value=0>No Cream</option>
          <option value=1>Creamy</option>
        </select>
      </div>

      <button class="button" @click="signUp">Sign Up</button>

      <div class="login">
        <p>Already have an account? <router-link to="/login">Log In</router-link></p>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword } from 'firebase/auth';
import { getFirestore, doc, setDoc } from 'firebase/firestore';
import CryptoJS from 'crypto-js';

export default {
  name: 'SignUp',
  data() {
    return {
      formData: {
        email: '',
        password: '',
        confirmPassword: '',
        healthCondition: [],
        ageGroup: '',
        preferenceCaffeine: '2',
        preferenceSweet: '2',
        preferenceCream: '0'
      },
      errorMessage: ''
    };
  },
  methods: {
    async signUp() {
      const auth = getAuth();
      const db = getFirestore();

      // Validate Password Match
      if (this.formData.password !== this.formData.confirmPassword) {
        this.errorMessage = "Passwords do not match";
        return;
      }

      const hashPassword = CryptoJS.MD5(this.formData.password).toString();

      try {
        const userCredential = await createUserWithEmailAndPassword(auth, this.formData.email, this.formData.password);
        const user = userCredential.user;
        const userDocRef = doc(db, 'users', user.uid);

        // Save user data to Firestore
        await setDoc(userDocRef, {  
          email: this.formData.email,
          password: hashPassword,
          healthCondition: this.formData.healthCondition,
          ageGroup: this.formData.ageGroup,
          preferences: {
            caffeine: this.formData.preferenceCaffeine,
            sweet: this.formData.preferenceSweet,
            cream: this.formData.preferenceCream
          }
        });

        console.log('Successfully signed up');
        this.$router.replace('/mainpage');

      } catch (error) {
        console.error("Signup Error:", error);
        this.errorMessage = error.code + '\n' + error.message;
      }
    }
  }
};
</script>

<style scoped>

</style>