const loginButton=document.getElementById('loginButton');
const signupButton=document.getElementById('signupButton');
const signInForm=document.getElementById('signIn');
const signUpForm=document.getElementById('signUp');

loginButton.addEventListener('click',function(){
    signUpForm.style.display="none";
    signInForm.style.display="block";
})

signupButton.addEventListener('click',function(){
    signInForm.style.display="none";
    signUpForm.style.display="block";
})