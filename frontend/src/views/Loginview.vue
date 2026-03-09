<template>
    <div class ="container-fluid">
        <div class="row justify-content-center">
            <form v-on:submit.prevent="login">
                <div class="mb-3">
                    <label for="exampleInputEmail1" class="form-label">Username</label>
                    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                    <div id="emailHelp" class="form-text">We'll never share your username with anyone else.</div>
                </div>
                <div class="mb-3">
                    <label for="exampleInputPassword1" class="form-label">Password</label>
                    <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" @input="validatePassword">
                    <div id="passwordHelp" class="form-text text-danger">{{ PasswordError }}</div>
                </div>
                
                <button type="submit" class="btn btn-primary">Submit</button>
            </form>
        </div>
    </div>
</template>     


<script setup>
import {ref} from 'vue';

const email = ref('');
const password = ref('');

const PasswordError = ref('');

const validatePassword = () => {
    if (password.value.length < 6){
        PasswordError.value = "password must be atleast 6 characters"
        return false;
    } else{
        PasswordError.value = '';
        return true;
    }    
}

async function login(){
    if (!validatePassword()){
        alert('Invalid password length')
        return;
    }

    if (email.value === '' || password.value === ''){
        alert('Please fill in all fields');
        return;
    }

    const user = {
        email: email.value,
        password: password.value
    }

    const response = await fetch("http://127.0.0.1:5000/api/login",{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(user)
    });

    console.log(response);

    if (!response.ok){
        const errorData = await response.json();
        console.error(errorData);
        console.error(`Login failed: ${errorData.message}`);
    }
    else{
        const data = await response.json();
        console.log( data);

        localStorage.setItem('token',data.user_details.auth_token);
        alert(data.message);
        return;
    }
}
</script>