const openDoorButton = document.getElementById('opendoor_button');
const openDoorDiv = document.getElementById('opendoor_div');
const loginDiv = document.getElementById('login_div');
const loginButton = document.getElementById('login_button');
const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const clearButton = document.getElementById('clear_button');


if (localStorage.getItem('username')) {
  openDoorDiv.classList.remove('hidden');
} else {
  loginDiv.classList.remove('hidden');
}

openDoorButton.addEventListener('click', () => {

});

loginButton.addEventListener('click', () => {
  const username = usernameInput.value;
  const password = passwordInput.value;
  usernameInput.value = '';
  passwordInput.value = '';
  localStorage.setItem('username', username);
  localStorage.setItem('password', password);
  openDoorDiv.classList.remove('hidden');
  loginDiv.classList.add('hidden');
});

clearButton.addEventListener('click', () => {
  localStorage.removeItem('username');
  localStorage.removeItem('password');
  openDoorDiv.classList.add('hidden');
  loginDiv.classList.remove('hidden');
});
