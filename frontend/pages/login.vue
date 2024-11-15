<script setup lang="ts">
definePageMeta({
  auth: {
    unauthenticatedOnly: true,
    navigateAuthenticatedTo: '/',
  },
  layout: 'form',
});

const { passwordIcon, inputType, togglePasswordShow } = usePasswordField();
const { loginState, snackbarAlerts, usernameRules, passwordRules, redirectToRootIfAuthenticated, signInWithCredentials } = useLoginField();

// Call during setup to redirect user if already authenticated
redirectToRootIfAuthenticated()

</script>

<!-- We need to wrap entire template in a <div> otherwise transitions complains. -->
<template>
    <v-container
    fill-height
    fluid
    class="d-flex justify-center align-center flex-column"
    >
      <v-card class="mx-auto" width="600px">
        <v-card-title primary-title class="mb-8 pa-4 bg-blue justify-center">
          <div class="text-center">
            <h3 class="headline"><b> GopherDen </b></h3>
          </div>
        </v-card-title>
        <div class="icon-container">
          <v-divider role="presentation" class="icon-divider"></v-divider>
          <v-avatar ref="avatar" class="pa-2 icon-avatar" color="primary" size="100" loading="lazy" alt="housbuddy-logo" image="~/assets/images/GopherDen-logo.png" />
        </div>
        <v-form :state="loginState" v-model="loginState.valid" class="space-y-4" @submit.prevent="signInWithCredentials">
          <v-card-text class="pb-0">

            <v-text-field 
              v-model="loginState.username" 
              prepend-inner-icon="mdi-account-circle"
              label="Username or Email"
              :rules="usernameRules"
            />

            <v-text-field 
              v-model="loginState.password"
              icon="i-heroicons-lock-closed"
              :type="inputType"
              label="Password"
              :rules="passwordRules"
              prepend-inner-icon="mdi-lock"
              :append-inner-icon="passwordIcon"
              @click:append-inner="togglePasswordShow"
            />

            <v-checkbox 
              v-model="loginState.remember_me" 
              label="Remember Me" 
            />
          </v-card-text>
          <v-card-actions class="justify-center pt-0">
            <v-col cols="5">
              <v-btn color="white" type="submit" rounded class="rounded-xxl bg-primary" :loading="loginState.loading" block>
                login
              </v-btn>
            </v-col>
          </v-card-actions>
        </v-form>

        <v-card-text class="d-flex justify-center flex-column flex-sm-row">
          <div
            v-for="link in [
              {
                text: 'Github',
                icon: 'mdi-github',
                href: 'https://github.com/CalvesGEH/GopherDen'
              },
              {
                text: 'Docs',
                icon: 'mdi-book',
                href: 'https://github.com/CalvesGEH/GopherDen'
              }
            ]"
            :key="link.text"
            class="text-center pa-0"
          >
            <v-btn :href="link.href" rounded elevation="0">
              <v-icon left>
                {{ link.icon }}
              </v-icon>
                {{ link.text }}
            </v-btn>
          </div>
        </v-card-text>
      </v-card>
      <div
        v-for="alert in snackbarAlerts"
        :key="alert.key"
      >
        <HBSnackbar
          v-model="alert.show"
          :text="alert.text"
          :type="alert.type"
          :timeout="alert.timeout"
        />
      </div>
    </v-container>
</template>

<style scoped>
.icon-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  position: relative;
  margin-top: 4rem;
}

.icon-divider {
  width: 100%;
  margin-bottom: -3.2rem;
}
</style>