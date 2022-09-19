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
var banner = `

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

`
var term = $('#term').terminal(function(cmd, term) {
  // help
  if (cmd == 'help') {
    term.echo(`\nAvailable commands are:
      command - Execute commands on the host
      payloads - Execute payloads on the host
      banner - Display awesome ASCII art
      help - List available commands
      exit - Return to the main menu\n`)
  }
  // display awesome ASCII art
  if (cmd == 'banner') {
    term.echo(banner)
  }

  if (cmd == 'payloads') {
    term.push(function(cmd, term) {
      if (cmd == 'exit') {
        term.pop();
      } else {
        var bot = window.location.pathname;
        $.jrpc("/api/1.1/fetch_payloads", bot, cmd, function(json) {
          if (!json.error) {
            term.echo(json.result);
          } else {
            term.echo(json.error.message);
          }
        })
      }
    }, {
      prompt: 'Payloads> ',
    })

  }

  // run commands on the system
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
  greetings: banner,
  prompt: 'Bifrost> ',
  checkArity: false
});
