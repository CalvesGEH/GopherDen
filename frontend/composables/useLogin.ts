export function useLoginField() {
    const loginState = reactive({
        username: "",
        password: "",
        remember_me: false,
        loading: false,
        valid: false,
    })

    const snackbarAlerts = ref({
        loginError: {
          text: 'placeholder',
          type: 'error',
          timeout: 5000,
          show: false,
        },
      });

    const usernameRules = [
        (v: string) => !!v || "Username is required",
        (v: string) => (v && v.length <= 256) || "Username must be less than 256 characters",
        (v: string) => (v && v.length > 3) || "Username must be more than 3 characters",
    ]
    const passwordRules = [
        (v: string) => !!v || "Password is required",
        (v: string) => (v && v.length >= 8) || "Password must be more than 8 characters",
    ]
    
    const { signIn, status } = useAuth()
    const redirectToRootIfAuthenticated = () => {
        if (status.value === "authenticated") {
            navigateTo("/");
        }
    }
    const signInWithCredentials = async () => {
        // This is the object that our backend expects for the `signIn` endpoint
        // NOTE: It must be a URLSearchParams object as that is how the data is encoded for
        //       the `Content-Type: application/x-www-form-urlencoded` header
        loginState.loading = true;

        // Check if the form validation is true
        if (!loginState.valid) {
            loginState.loading = false;
            snackbarAlerts.value.loginError.text = "Form is invalid!";
            return;
        }

        const formData = new URLSearchParams();
        formData.append("username", loginState.username);
        formData.append("password", loginState.password);
        formData.append("remember_me", String(loginState.remember_me));
        
        try {
            // This sends a POST request to the `auth.provider.endpoints.signIn` endpoint with `credentials` as the body
            let res = await signIn(formData, { callbackUrl: '/' });
            navigateTo("/");
        } catch (error: any) {
            loginState.loading = false;
            if (error.response.status === 401) {
                snackbarAlerts.value.loginError.text = "Invalid username or password!";
            }
            else if (error.response.status === 423) {
                snackbarAlerts.value.loginError.text = "Account is locked!";
            }
            else {
                snackbarAlerts.value.loginError.text = "An error occurred!";
            }
            snackbarAlerts.value.loginError.show = true;
        }
    }
  
    return {
        loginState,
        snackbarAlerts,
        usernameRules,
        passwordRules,
        redirectToRootIfAuthenticated,
        signInWithCredentials,
    };
  }