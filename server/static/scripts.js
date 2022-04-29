/*!
* Start Bootstrap - Simple Sidebar v6.0.5 (https://startbootstrap.com/template/simple-sidebar)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-simple-sidebar/blob/master/LICENSE)
*/
// 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

  // Toggle the side navigation
  const sidebarToggle = document.body.querySelector('#sidebarToggle');
  if (sidebarToggle) {
    // Uncomment Below to persist sidebar toggle between refreshes
    // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
    //     document.body.classList.toggle('sb-sidenav-toggled');
    // }
    sidebarToggle.addEventListener('click', event => {
      event.preventDefault();
      document.body.classList.toggle('sb-sidenav-toggled');
      localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
    });
  }

});

//keyboardeventKeyPolyfill.polyfill();
var term = $('#term').terminal(function(cmd, term) {
  if (cmd == 'command') {
    term.push(function(cmd, term) {
      if (cmd == 'exit') {
        term.pop();
      } else {
        var bot = window.location.pathname;
        $.jrpc("/api/1.1/add_command", bot, cmd, function(json) {
          if (!json.error) {
            term.echo(json.result);
          } else {
            term.echo(json.error.message);
          }
        })
      }
    }, {
      prompt: 'RCE> ',
    })
  }
}, {
  name: 'autocomplete_error_example',
  greetings: `

 ▄▄▄▄    ██▓  █████▒██▀███   ▒█████    ██████ ▄▄▄█████▓
▓█████▄ ▓██▒▓██   ▒▓██ ▒ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
▒██▒ ▄██▒██▒▒████ ░▓██ ░▄█ ▒▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
▒██░█▀  ░██░░▓█▒  ░▒██▀▀█▄  ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
░▓█  ▀█▓░██░░▒█░   ░██▓ ▒██▒░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
░▒▓███▀▒░▓   ▒ ░   ░ ▒▓ ░▒▓░░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
▒░▒   ░  ▒ ░ ░       ░▒ ░ ▒░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
 ░    ░  ▒ ░ ░ ░     ░░   ░ ░ ░ ░ ▒  ░  ░  ░    ░      
 ░       ░            ░         ░ ░        ░           
      ░

`,
  prompt: '> ',
  completion: ["autocomplete001", "autocomplete002", "autocomplete003", "autocomplete004"],
  checkArity: false
});
