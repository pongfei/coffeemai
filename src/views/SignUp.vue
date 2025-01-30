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
          <option value="Strong">Strong</option>
          <option value="Medium">Medium</option>
          <option value="Light">Light</option>
        </select>
      </div>

      <label for="preferenceSweet" class="form-label">Preference (Sweet)</label>
      <div class="input-group">
        <select id="preferenceSweet" class="form-control" v-model="formData.preferenceSweet">
          <option value="Sweet">Sweet</option>
          <option value="Less Sweet">Less Sweet</option>
          <option value="No Sweet">No Sweet</option>
        </select>
      </div>

      <label for="preferenceCream" class="form-label">Preference (Cream)</label>
      <div class="input-group">
        <select id="preferenceCream" class="form-control" v-model="formData.preferenceCream">
          <option value="Creamy">Creamy</option>
          <option value="No Cream">No Cream</option>
        </select>
      </div>

      <button class="btn btn-success" @click="signUp">Sign Up</button>

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
        preferenceCaffeine: '',
        preferenceSweet: '',
        preferenceCream: ''
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
.signup-container {
  display: flex;
  height: 100vh;
}

.image-side {
  flex: 1;
  position: relative;
  background: url('https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg') no-repeat center center;
  background-size: cover;
}

.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.quote {
  position: absolute;
  bottom: 20px;
  left: 20px;
  color: white;
  font-size: 24px;
}

.form-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 40px;
  padding-top: 100px;
  background: white;
}

.form-side h2 {
  margin-bottom: 10px;
}

.form-side p {
  margin-bottom: 20px;
  color: #666;
}

.input-group {
  width: 100%;
  margin-bottom: 20px;
}

.checkbox-group {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 15px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 10px;
}

.btn {
  width: 100%;
  padding: 10px;
  background: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.btn:hover {
  background: #218838;
}

.error-message {
  margin-top: 20px;
  color: red;
  text-align: center;
}
</style>