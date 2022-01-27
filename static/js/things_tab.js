function delThing(elem_id) {
  // список id вещей изменяемый на странице
  let things_id =  JSON.parse(document.querySelector('#things_id_list').value)
  // список текущих id в БД (изменяются только после нажатия кнопки 'Сохранить')
  const const_things_id  = JSON.parse(document.querySelector('#const_things_id_list').value)

  let isInclude = false
  let isConfirm = true

  if (const_things_id.includes(Number(elem_id))) {
    isInclude = true
    if (!confirm('Вы уверены что хотите удалить элемент?')) {
      isConfirm = false
    }
  }

  if (isConfirm) {
    // определяем ряд который удаляем
    let row = document.querySelector(`.tr${elem_id}`)
    // удаляем ряд
    row.remove()
    // удаляем id элемент из изменяемого списка id вещей
    newIdList = things_id.filter((n) => {return n != elem_id});
    // обновляем изменяемый список id вещей, предварительно преобразовав его в json формат
    document.querySelector('#things_id_list').value = JSON.stringify(newIdList)    
  }

  if (isConfirm && isInclude) {
    // кликаем по кнопке сохранить, удаляя соответствующую строку из в БД
    document.querySelector('.save_things_data').click()
  } 

}



function delAllThings() {
  // записываем пустой список id для передачи на сервер
  document.querySelector('#things_id_list').value = JSON.stringify(['all']) 
  // кликаем по кнопке сохранить
  document.querySelector('.save_things_data').click()
}


function addThing(table, id_list) {
  // берем максимальное значение в things_id
  var id = 0
  if (id_list.length !== 0){
    id = Math.max.apply(null, id_list)+1
  } else {
    id = 1
  }
  // добавляем дополнительный id в список id вещей
  id_list.push(id)
  // создаем элемент 'tr'
  var tr = document.createElement('tr')
  tr.className = `thing_row tr${id}`
  //создаем 5 элементов 'td' внутри 'tr'
  for (var i = 0; i < 5; i++) { 
    var td = document.createElement('td')
    var elem = ''
    // если это первые 4 столбца то создаем 'input'
    if (i < 4) {
      elem = document.createElement("input")
      elem.required = true
      // 1-ый столбец
      if (i===0) {
      elem.className = `things_input1`   
      elem.type = "number"
      elem.name = `number_${id}`
        // 2-ой столбец
      } else { 
        if (i===1) {
          elem.className = `things_input2` 
          elem.type = "text"
          elem.name = `name_${id}`
        // 3-ий столбец
        } else { 
          if (i===2) {
            elem.className = `things_input3` 
            elem.type = "number"
            elem.name = `amount_${id}`
          // 4-ый столбец    
          } else { 
            elem.className = `things_input4` 
            elem.type = "number"
            elem.name = `cost_${id}` 
          }
        }
      }
    // иначе (последний 5-ый столбец) создаем 'div' 
    } else {
      elem = document.createElement("div")
      elem.innerText = 'X'
      elem.className = `btn`
      // привязывам кнопку к функции удаления
      elem.addEventListener("click", () => { delThing(id) });
    }
    // добавляем элемент ('input' или 'div') в элемент 'td'
    td.append(elem)
    // добавляем элемент 'td' в элемент 'tr'
    tr.append(td)
  }
  // добавляем 'tr' в таблицу
  table.append(tr)
  // обновляем список id вещей, предварительно преобразовав его в json формат
  document.querySelector('#things_id_list').value = JSON.stringify(id_list)
}




if (document.querySelector('#form_page_rental_object')) {
  // Кнопка события
  let btn = document.querySelector('#add_thing_btn')
  // Таблица для вставки
  let table = document.querySelector('#things_table')
  // Список id вещей, загруженный из БД
  let id_list =  JSON.parse(document.querySelector('#things_id_list').value)



  // Привязка с событию
  btn.addEventListener("click", () => { addThing(table, id_list) })
}