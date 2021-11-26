function openData(evt, dataName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(dataName).style.display = "block";
  evt.currentTarget.className += " active";
}















































// const header1 = document.querySelector('#header1')
// const header2 = document.querySelector('#header2')
// const header3 = document.querySelector('#header3')
// let orders_items = document.querySelector('#orders_items') // получаем данные всех заказов


// const button = document.querySelector('#button') 


// function cookieValue(cookie, key, data_type='str') {
// 	cookie = cookie.split('; ')
// 	let counter = '' 
// 	for (let i of cookie) {
// 		if (i.includes(key)) {
// 			counter = i.split('=')[1]
// 		}
// 	} 
// 	if (data_type === 'num') {
// 		return Number(counter)
// 	}
// 	else {
// 		return counter
// 	}
// }

// console.log(cookieValue(document.cookie, 'counter', 'num'))






// button.onclick = () => {
// 	if (cookieValue(document.cookie, 'counter') === 0) {
// 		addStylesTo(header1, 'Я', 'yellow')
// 		document.cookie = `counter=${1}` // Присваивание обрабатывается особым образом.
// 	}
// 	else {
// 		addStylesTo(header1, 'Я', 'grey')
// 		document.cookie = `counter=${0}` // Присваивание обрабатывается особым образом.
// 	}
// }


// header2.onclick = () => { 
// 	if (header2.style.backgroundColor === 'black') {
// 		header2.style.backgroundColor= 'white'
// 		header2.style.color = 'black'
// 	}
// 	else {
// 		header2.style.backgroundColor = 'black'
// 		header2.style.color = 'blue'
// 	}
// }

// // альтернатива on
// header3.addEventListener('dblclick', () => {
// 		if (header3.style.backgroundColor === 'black') {
// 		header3.style.backgroundColor= 'white'
// 		header3.style.color = 'black'
// 	}
// 	else {
// 		header3.style.backgroundColor = 'black'
// 		header3.style.color = 'red'
// 	}
// })





// // console.log(`Счетчик: ${counter}`)





// // Функция задает стиль для узла
// function addStylesTo(node, text, color='red') {
// 	node.style.color = color // Обращение к css свойствам элемента
// 	node.style.textAlign = 'center' // Обращение к css свойствам элемента
// 	node.style.backgroundColor = 'black' // Обращение к css свойствам элемента
// 	node.style.fontSize = '18px' // Обращение к css свойствам элемента
// 	node.style.display = 'block'
// 	node.style.width = '100%'
// 	node.textContent = text // Обращение к текстовому контенту внутри элемента
// }

// function delStylesAndText(node, text='') {
// 	node.style.all = 'none' // Обращение к css свойствам элемента
// 	node.textContent = text // Обращение к текстовому контенту внутри элемента
// }


// const link = header1.querySelector('a')
// link.addEventListener('click', (event) => {
// 	event.preventDefault() // отмена событий по умолчанию
// 	console.log('click on link', event) // event - выводится информация о том что произошло в момент клика
// 	console.log(event.altitudeAngle) // обращение к одному из атрибутов события
// 	console.log(event.target) // получение данных об узле
// 	console.log(event.target.getAttribute('href')) // получение атрибута узла (ссылка)
// 	console.log(event.target.getAttribute('target')) // получение атрибута узла
// 	console.log(event.target.setAttribute('target', '_blank')) // установка атрибута узла
// 	console.log(event.target.setAttribute('id', '126')) // установка атрибута узла
// 	window.location = event.target.getAttribute('href') // присвивание ссылки полученной из атрибутов узла
// })

// // время задержки выполнения( в милесекундах)
// setTimeout( () => {
// 	addStylesTo(header1.querySelector('a'), 'mozilla', 'white') // или header1.querySelector('a') = header1.children[0]
// }, 100)

// setTimeout( () => {
// 	addStylesTo(header2, 'Просто', 'blue')
// }, 200)

// setTimeout( () => {
// 	addStylesTo(header3, 'Охуенен!', 'red')
// }, 300)
