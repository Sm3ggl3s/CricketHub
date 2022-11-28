
let darkMode = localStorage.getItem('dark'); 

const checkbox = document.getElementById('checkbox');

const enableDarkMode = () => {
  // 1. Add the class to the body
  document.body.classList.toggle('dark');
  // 2. Update darkMode in localStorage
  localStorage.setItem('dark', 'enabled');
}

const disableDarkMode = () => {
  // 1. Remove the class from the body
  document.body.classList.toggle('dark');
  // 2. Update darkMode in localStorage 
  localStorage.setItem('dark', null);
}
 
// If the user already visited and enabled darkMode
// start things off with it on
if (darkMode === 'enabled') {
  enableDarkMode();
}

// When someone clicks the button
checkbox.addEventListener('change', () => {
  // get their darkMode setting
  darkMode = localStorage.getItem('dark'); 
  
  // if it not current enabled, enable it
  if (darkMode !== 'enabled') {
    enableDarkMode();
  // if it has been enabled, turn it off  
  } else {  
    disableDarkMode(); 
  }
});

