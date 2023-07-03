const registerBtn = document.querySelector('.register-btn');
const registerModal = document.getElementById('register-modal');
const closeModalBtn = document.querySelector('.close-modal');

registerBtn.addEventListener('click', () => {
  registerModal.style.display = 'flex';
});

window.addEventListener('click', (event) => {
  if (event.target === registerModal) {
    registerModal.style.display = 'none';
  }
});

const loginBtn = document.querySelector('.login-btn');
const loginModal = document.getElementById('login-modal');

loginBtn.addEventListener('click', () => {
  loginModal.style.display = 'flex';
});

window.addEventListener('click', (event) => {
  if (event.target === loginModal) {
    loginModal.style.display = 'none';
  }
});