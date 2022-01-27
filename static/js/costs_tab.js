function delCost(elem_id) {
  // Список id вещей на странице (подгруженных из БД и добавенных)
  let all_costs_id =  JSON.parse(document.querySelector('#all_costs_id').value)
   // Список добавленных id вещей на странице
  let added_costs_id = JSON.parse(document.querySelector('#added_costs_id').value)
  // список текущих id в БД 
  const db_costs_id  = JSON.parse(document.querySelector('#db_costs_id').value)

  let isInclude = false
  let isConfirm = true

  if (db_costs_id.includes(Number(elem_id))) {
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
    // удаляем id элемент из списка всех id
    let newAll = all_costs_id.filter((n) => {return n != elem_id});
    // обновляем изменяемый список id вещей, предварительно преобразовав его в json формат
    document.querySelector('#all_costs_id').value = JSON.stringify(newAll)
    // удаляем id элемент из списка добавленных id
    let newAdded = added_costs_id.filter((n) => {return n != elem_id});   
     // обновляем изменяемый список id вещей, предварительно преобразовав его в json формат
    document.querySelector('#added_costs_id').value = JSON.stringify(newAdded)
  }

  if (isConfirm && isInclude) {
    // добавляем id удаляемого элемента в соответствующий инпут
    document.querySelector('#del_cost_id').value = JSON.stringify(Number(elem_id))
    // кликаем по кнопке сохранить, удаляя соответствующую строку из в БД
    document.querySelector('.save_costs_data').click()
  } 

}


function addCost() {
    // Таблица для вставки
  let table = document.querySelector('#costs_table')
  // Список id вещей на странице (подгруженных из БД и добавенных)
  let all_costs_id =  JSON.parse(document.querySelector('#all_costs_id').value)
   // Список добавленных id вещей на странице
  let added_costs_id = JSON.parse(document.querySelector('#added_costs_id').value)

  // берем максимальное значение в things_id
  let id = 0
  if (all_costs_id.length !== 0) {
    id = Math.max.apply(null, all_costs_id)+1
  } else {
    id = 1
  }
  // добавляем id в список id расходов (то что пришло из БД + добавлено через js)
  all_costs_id.push(id)
  document.querySelector('#all_costs_id').value = JSON.stringify(all_costs_id)

  // добавляем id в список id расходов (только то что добавлено через js)
  added_costs_id.push(id)
  document.querySelector('#added_costs_id').value = JSON.stringify(added_costs_id)

  // создаем элемент 'tr'
  let tr = document.createElement('tr')
  tr.className = `cost_row tr${id}`
  //создаем 3 элементов 'td' внутри 'tr'
  for (var i = 0; i < 3; i++) { 
    let td = document.createElement('td')
    let elem = ''
    // 1-ый столбец ('input')
    if (i == 0) {
      elem = document.createElement("input")
      elem.type = "text"
      elem.className = 'costs_input'
      elem.name = `name_${id}`
      elem.required = true
      // 2-ой столбец ('radio')
      } else { 
        if (i == 1) {
          elem = document.createElement("div")
          
          radio1 = document.createElement("input")
          radio1.type = 'radio'
          radio1.name = `is_payer_landlord_${id}`
          radio1.value = '0'
          radio1.checked = true

          radio2 = document.createElement("input")
          radio2.type = 'radio'
          radio2.name = `is_payer_landlord_${id}`
          radio2.value = '1'

          label1 = document.createElement("label")
          label1.append(radio1)
          label1.append('Наниматель')

          label2 = document.createElement("label")
          label2.append(radio2)
          label2.append('Наймодатель')

          elem.append(label1)
          elem.append(label2)
        // 3-ий столбец ('div')
        } else {
          elem = document.createElement("div")
          elem.innerText = 'X'
          elem.className = `btn`
          // привязывам кнопку к функции удаления
          elem.addEventListener("click", () => { delCost(id) })
        }
      }
      // добавляем элемент ('input' или 'div') в элемент 'td'
      td.append(elem)
      // добавляем элемент 'td' в элемент 'tr'
      tr.append(td)
  }
  // добавляем 'tr' в таблицу
  table.append(tr)
  // обновляем список id вещей, предварительно преобразовав его в json формат
  

}






if (document.querySelector('#form_page_rental_object')) {
  // Кнопка события
  let btn = document.querySelector('#add_cost_btn')

  // Привязка с событию
  btn.addEventListener("click", () => { addCost() })
}