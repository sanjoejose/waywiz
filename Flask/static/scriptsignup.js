import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getDatabase, get, ref, child } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyBdrhRx3XTT2tG5LRTdomCQeInVS3LFlrE",
    authDomain: "waywiz-b2334.firebaseapp.com",
    projectId: "waywiz-b2334",
    storageBucket: "waywiz-b2334.firebasestorage.app",
    messagingSenderId: "958400511753",
    appId: "1:958400511753:web:d5b5d80efd66ea8749ddd8"
};

const app = initializeApp(firebaseConfig);
const db = getDatabase();
const auth = getAuth(app);
const dbref = ref(db);

// Get the login email and password fields by their IDs
// let Email = document.getElementById("signupEmail");
// let Password = document.getElementById("signupPassword");

let signupbtn = document.getElementById("signbtn");
const email = document.getElementById("signupEmail");
const password = document.getElementById("signupPassword");



// Define the function for signing in the user
signupbtn.addEventListener("click", function (e) {
    e.preventDefault();
    // alert("Clicked");
    // Ensure Email and Password are properly defined
    // if (!email || !password) {
    //     alert("Please enter both email and password!");
    //     return;
    // }
    console.log(email.value, password.value);

    createUserWithEmailAndPassword(auth, email.value, password.value)
        .then((userCredential) => {
            // Signed up 
            const user = userCredential.user;
            window.location.href = "{{ url_for('sign_up') }}";  // Redirect after successful login
        })
        .catch((error) => {
            const errorCode = error.code;
            const errorMessage = error.message;
            console.error("Error getting ID token:", error);
            // ..
        });
});
