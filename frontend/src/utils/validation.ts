export const validateRequired = (value: string): string | undefined => {
  if (!value || value.trim() === '') {
    return 'Это поле обязательно';
  }
  return undefined;
};

export const validateEmail = (email: string): string | undefined => {
  if (!email) return undefined; // Let validateRequired handle empty case
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(email)) {
    return 'Некорректный email адрес';
  }
  return undefined;
};

export const validatePassword = (password: string): string | undefined => {
  if (!password) return undefined; // Let validateRequired handle empty case
  
  if (password.length < 8) {
    return 'Пароль должен быть не менее 8 символов';
  }
  
  if (!/[A-Z]/.test(password)) {
    return 'Пароль должен содержать хотя бы одну заглавную букву';
  }
  
  if (!/[a-z]/.test(password)) {
    return 'Пароль должен содержать хотя бы одну строчную букву';
  }
  
  if (!/[0-9]/.test(password)) {
    return 'Пароль должен содержать хотя бы одну цифру';
  }
  
  return undefined;
}; 