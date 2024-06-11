function init(input, shadow) {
    oninput()
    var lastLen = input.value.length
  
    const style = getComputedStyle(input);
    const exclude = /\b(fill|stroke|color)\b/;
    Array.from(style).forEach(
      property => !exclude.test(property) && (shadow.style[property] = style[property])
    )
  
    // input скролится при переполнении, учитываем это
    function onscroll() {
        shadow.querySelector('.text').style = 'margin-left: ' + -input.scrollLeft + 'px';
    }
    
    function oninput() {
        shadow.innerHTML = ''
      if(!input.value) return;
      shadow.append(input.value.slice(0, -1));
      shadow.innerHTML = '<span class="text">' + shadow.innerHTML + '</span>'
      
      const span = document.createElement('span');
      span.append(input.value.slice(-1));
      
      if (lastLen <= input.value.length) { 
        span.className = 'last-symbol';
      }
      lastLen = input.value.length
      shadow.append(span);
    }
  
    input.addEventListener('scroll', onscroll)
    input.addEventListener('input', oninput)
  }
  
init(document.querySelector('.email'), document.querySelector('.email-shadow'));