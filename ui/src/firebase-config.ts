// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from 'firebase/auth';
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD3UsxAOjrfsAYH7Re87mT-dT88iLWXmkE",
  authDomain: "irrigation-mvp-ajgc.firebaseapp.com",
  projectId: "irrigation-mvp-ajgc",
  storageBucket: "irrigation-mvp-ajgc.appspot.com",
  messagingSenderId: "9228221367",
  appId: "1:9228221367:web:8eb0787e88f4d2c551c632",
  measurementId: "G-PGR3V5J8E7"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
export const auth = getAuth(app);