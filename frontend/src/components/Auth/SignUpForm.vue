<template>
<div class="text-center" style="padding:50px 0">
	<div class="logo">Sign Up</div>
	<div class="login-form-1">
		<form class="text-left"  @submit.prevent="register">
			<div class="login-form-main-message"></div>
			<div class="main-login-form">
        <div v-if="errMessage != ''"> 
            <p class="danger">{{errMessage}}</p>
        </div>  
				<div class="login-group">
					<div class="form-group">
						<label for="lg_email" class="sr-only">email</label>
						<input v-model="email" type="text" class="form-control"  placeholder="email" required>
					</div>
					<div class="form-group">
						<label for="lg_password" class="sr-only">Password</label>
						<input v-model="password" type="password" class="form-control"  placeholder="password" required>
					</div>
					<div class="form-group">
						<label for="lg_email" class="sr-only">first name</label>
						<input v-model="firstName" type="text" class="form-control"  placeholder="first name" required>
					</div>
            <div class="form-group">
						<label for="lg_email" class="sr-only">last name</label>
						<input v-model="lastName" type="text" class="form-control"  placeholder="last name" required>
            <div>
              <b-btn type="submit" size="sm" class="register-btn" variant="outline-success">Register</b-btn>
            </div>
				</div>
      
			</div>
			</div>
		</form>
	</div>
</div>
</template>



<script>
import {REGISTER_REQUEST} from './../../utils/auth_const.js'
import funcs from '../../utils/auth_funcs.js'

export default {
    name: 'SignInForm',
    data: function () {
      return {
        email: 'Rexarrior@yandex.ru', 
        password: 'sTame_342', 
        firstName: 'Ksandr', 
        lastName: 'renderon', 
        organization: 'none',
        errMessage: '',
      }
      
    },
    methods: {
        register: function () {
            const model = {
              email: this.email, 
              password: this.password, 
              firstName: this.firstName, 
              lastName: this.lastName,
              organization: this.organization
            };
            if (!funcs.CheckRegModel(model))
            {
              return;
            }

            this.$store.dispatch(REGISTER_REQUEST, model).then(()=>{
              this.$router.push('/');
            }, 
            (err)=>{
              if (funcs.isUserExistError(err))
                this.errMessage = err;
            });
         }
}

}
</script>



<style scoped>
.register-btn{
  margin:1%; 
  width: 100%;
  padding: 1%;
}
</style>
