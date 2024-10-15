document.addEventListener('DOMContentLoaded', () => {
  const ta = document.querySelector('textarea')

  const storedTxt = localStorage.getItem('text')
  if (storedTxt) ta.value = storedTxt
  ta.style.height = localStorage.getItem('height')

  ta.addEventListener('input', () => {
    localStorage.setItem('text', ta.value)
  })

  new ResizeObserver(() => {
    localStorage.setItem('height', ta.style.height)
  }).observe(ta)

  const comparator = document.querySelector('.comparator')
  const pCopy = document.createElement('p')
  pCopy.innerText = comparator.querySelector('p').innerText
  comparator.appendChild(pCopy)

  fetch('../generated/fonts.json')
    .then(res => res.json())
    .then(data => {
      const para = document.querySelector('.paragraphs')
      const sel = document.querySelector('select')
      const preloader = document.querySelector('#preloader')
      
      data.forEach(font => {
        const opt = document.createElement('option')
        opt.innerText = font
        sel.appendChild(opt)
        const span = document.createElement('span')
        span.style.fontFamily = font
        preloader.appendChild(span)
      })

      const recalculate = () => {
        comparator.style.height = pCopy.getBoundingClientRect().height + 'px'
      }
      new ResizeObserver(recalculate).observe(comparator)

      sel.addEventListener('change', () => {
        const setFont = (el, round) => {
          if (sel.value === 'Default') {
            el.style.removeProperty('font-family')
            return
          }
          el.style.fontFamily = sel.value + (round ? ' R' : '')
        }

        setFont(ta)
        para.querySelectorAll('p').forEach((el, i) => {
          setFont(el, i % 2 === 0)
        })

        comparator.querySelector('p:first-child').style.fontFamily = sel.value
        comparator.querySelector('p:last-child').style.fontFamily = sel.value + ' R'
        setTimeout(recalculate, 500);
      })
    })
})
