<template>
    <div class="signup-container">
      <div class="image-side">
        <img src="https://img.freepik.com/free-photo/delicious-coffee-beans-cup_23-2150691429.jpg" alt="Coffee" class="background-image" />
        <p class="quote">"Espress Yourself."</p>
      </div>
      <div class="form-side">
        <h2>Create Account</h2>
        <br>
        <p>Sign up to start ordering your favorite coffee</p>

        <!-- email -->
        <div class="input-group">
          <input type="email" class="form-control" placeholder="Email" v-model="formData.email" />
        </div>
        <!-- password -->
        <div class="input-group">
          <input type="password" class="form-control" placeholder="Password" v-model="formData.password" />
        </div>
        <!-- confirm password -->
        <div class="input-group">
          <input type="password" class="form-control" placeholder="Confirm Password" v-model="formData.confirmPassword" />
        </div>
        <!-- health condition -->
        <label for="healthCondition" class="form-label">Health Condition (If Any)</label>
        <div class = "input-group">
          <select name="healthCondition" id="healthCondition" class="form-control"  v-model="formData.healthCondition">
          <option value="Sleep Disorder">Sleep Disorder</option>
          <option value="Lactose Intolerance">Lactose Intolerance</option>
          <option value="Diabetes">Diabetes</option>
          <option value="High Pressure">High Pressure</option>
          <option value="Heart Disease">Heart Disease</option>
          <option value="Diarrhea">Diarrhea</option>
          <option value="Gas Reflux">Gas Reflux</option>
          <option value="Liver Disease">Liver Disease</option>
          </select>
          </div>

          <label for="Age Group" class="form-label">Age Group</label>
        <div class = "input-group">
          <select name="ageGroup" id="ageGroup" class="form-control"  v-model="formData.ageGroup">
          <option value="4 to 13">4 to 13</option>
          <option value="14 to 22">14 to 22</option>
          <option value="23 to 59">23 to 59</option>
          <option value="60 and up">60 and up</option>
          </select>
          </div>

        <!-- preference -->
        <label for="preference" class="form-label">Preference (If Any)</label>
        <div class = "input-group">
          <select name="preference" id="preference" class="form-control"  v-model="formData.preference">
          <option value="Strong">Strong</option>
          <option value="Medium">Medium</option>
          <option value="Light">Light</option>
          <option value="Sweet">Sweet</option>
          <option value="Less Sweet">Less Sweet</option>
          <option value="No Sweet">No Sweet</option>
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
        formData: { //object to store input
          email: '',
          password: '',
          confirmPassword: '',
          healthCondition: '',
          ageGroup: '',
          preference:''
        },
        errorMessage: ''
      };
    },
    methods: {
      async signUp() {

        const auth = getAuth();
        const db = getFirestore();

        if(this.formData.password != this.formData.confirmPassword){
          this.errorMessage = "Password Do Not Match"
          // alert(this.errorMessage);
          // console.log("mismatch password")
          return;
        }

        const hashPassword = CryptoJS.MD5(this.formData.password).toString()

        try {
          const userCredential = await createUserWithEmailAndPassword(auth, this.formData.email, this.formData.password);
          const user = userCredential.user;
          const userDocRef = doc(db, 'users', user.uid);

          await setDoc(userDocRef, {  
            email: this.formData.email,
            // password: this.formData.password,
            password: hashPassword,
            healthCondition: this.formData.healthCondition,
            ageGroup: this.formData.ageGroup,
            preference: this.formData.preference
          });
          console.log('Successfully signed up');
          this.$router.replace('/mainpage');
        } catch (error) {
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
    display: flex;
    flex-direction: column; /* Stack the label and dropdown vertically */
    align-items: center; /* Center align the content horizontally */
    margin-bottom: 20px;
  }
  
  .input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    box-sizing: border-box;
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
  
  .login {
    margin-top: 20px;
  }
  
  .login p {
    color: #666;
  }
  
  .login a {
    color: #007bff;
    text-decoration: none;
  }
  
  .form-label {
  margin-bottom: 10px; /* Add space below the label */
  font-size: 16px;
  color: #666;
  text-align: center; /* Center the label text */
}

  .error-message {
    margin-top: 20px;
    color: red;
    text-align: center;
  }

  .form-control {
  width: 100%; /* Adjust the dropdown width */
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
}
  </style>