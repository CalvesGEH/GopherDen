export function usePasswordField() {
  const show = ref(false);

  const passwordIcon = computed(() => {
    return show.value ? 'mdi-eye-off' : 'mdi-eye';
  });
  const inputType = computed(() => (show.value ? "text" : "password"));

  const togglePasswordShow = () => {
    show.value = !show.value;
  };

  return {
    inputType,
    togglePasswordShow,
    passwordIcon,
  };
}