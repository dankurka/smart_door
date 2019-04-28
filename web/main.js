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
  const encodedUsername = localStorage.getItem('username');
  const encodedPassword = localStorage.getItem('password');

  openDoorDiv.classList.add('hidden');

  const xhr = new XMLHttpRequest();
  xhr.open(
      "POST",
      `/open_door?username=${encodedUsername}&password=${encodedPassword}`);

  xhr.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE) {
      openDoorDiv.classList.remove('hidden');
      if (this.status !== 200) {
        alert(`Could not login: ${this.status}. Text: ${this.responseText}`);
      }
    }
  }
  xhr.send();
});

loginButton.addEventListener('click', () => {
  const username = usernameInput.value;
  const password = passwordInput.value;
  passwordInput.value = '';

  const encodedUsername = encodeURIComponent(username);
  const encodedPassword = encodeURIComponent(password);

  loginDiv.classList.add('hidden');

  const xhr = new XMLHttpRequest();
  xhr.open("POST",
           `/login?username=${encodedUsername}&password=${encodedPassword}`);

  xhr.onreadystatechange = function() {
    if (this.readyState === XMLHttpRequest.DONE) {
      if (this.status === 200) {
        localStorage.setItem('username', encodedUsername);
        localStorage.setItem('password', encodedPassword);
        openDoorDiv.classList.remove('hidden');
      } else {
        alert(`Could not login: ${this.status}. Text: ${this.responseText}`);
        loginDiv.classList.remove('hidden');
      }
    }
  }
  
  xhr.send();
});

clearButton.addEventListener('click', () => {
  localStorage.removeItem('username');
  localStorage.removeItem('password');
  openDoorDiv.classList.add('hidden');
  loginDiv.classList.remove('hidden');
});

// IOS 10+ hack to diable view port zooming
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
