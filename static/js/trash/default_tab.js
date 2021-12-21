/*
 * Извлекает данные из cookie по ключу
 *
 * @param {string} name - ключ для поиска значения ()

 */
function getCookie(name) {
	cookie = document.cookie.split('; ')
	let value = '' 
	for (let i of cookie) {
		if (i.includes(name)) {
			value = i.split('=')[1]
		}
	} 
	return value
}

// -----------------------------------------------------------------------------


if (getCookie('lastPressedButton')) {
	document.getElementById(getCookie('lastPressedButton')).click()
} else {tablinks = document.getElementsByClassName("tablinks");
		document.getElementById(tablinks[0].id).click()
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
