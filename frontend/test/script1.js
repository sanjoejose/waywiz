import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import { getDatabase, get, ref, child } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-database.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

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
        
        let Email = document.getElementById("loginEmail");
        let Password = document.getElementById("loginPassword");

            let signInUser = evt => {
                evt.preventDefault();
                
                signInWithEmailAndPassword(auth, Email.value, Password.value)
                    .then((credentials) =>{
                        auth.currentUser.getIdToken()
                        .then((idToken) => {
                            console.log("ID token:", idToken);
                            window.location.href = 'index1.html';
                        })
                        .catch((error) => {
                            console.error("Error getting ID token:", error);
                        });
                    })
                    .catch((error) => {
                        alert(error.message);
                        console.error("Error signing in:", error.code, error.message);
                    });
            };
        ruser.addEventListener('click',signInUser);