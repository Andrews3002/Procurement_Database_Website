const buttons = document.querySelectorAll('.btn');
buttons.forEach(btn => {
  btn.addEventListener('click', function(e) {
    const rect = e.target.getBoundingClientRect();
    const scale = rect.width / e.target.offsetWidth;

    let x = (e.clientX - rect.left) / scale;
    let y = (e.clientY - rect.top) / scale;

    let ripples = document.createElement('span');
    ripples.style.left = x + 'px';
    ripples.style.top = y + 'px';
    this.appendChild(ripples);

    setTimeout(() => {
      ripples.remove()
    },1000);
  })
})

function updateFavorite(companyName) {
  const form = document.getElementById(`favorite-form-${companyName}`);
  const checkbox = form.querySelector('input[type="checkbox"]');

  if (checkbox.checked) {
    checkbox.value = "1";  
  } else {
    checkbox.value = "0";  
  }
  
  form.submit();
}
