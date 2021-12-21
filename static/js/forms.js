/*
 * Добавляет элементы option в select 

 * @param {string} slct_id - id select'a в который происодит вставка options
 * @param {string} list_of_options_id - id элементa (input: hidden) содержащего в качестве value json-формат списка списков [[id, type],[],[]]
 * @param {string} current_value_id - id элементa (input: hidden) содержащего в качестве value текущее установленное значение
 */

function addOptions(slct_id, list_of_options_id, current_value_id) {
  for (let type of JSON.parse(document.querySelector(list_of_options_id).value)) {
    option = document.createElement('option')
    if (type[1] === document.querySelector(current_value_id).value) {
      option.selected = 'selected'
      }
    option.value = type[0]
    option.innerText = type[1]
    if (type[1] === 'не указано') {
      document.querySelector(slct_id).prepend(option)
    } else {
      document.querySelector(slct_id).append(option)
    }
  }
}



/*
 * Отмечает checked в элементе (input: radio) в зависимости от текущего значения в БД 
 *
 * @param {string} control_element_id - элемент (input: hidden) с value равным текущему значению
 * @param {string} no_elem_id - элемент (input: radio) с value='0'
 * @param {string} yes_elem_id - элемент (input: radio) с value='1'
 */

function setCurrentRadio(control_element_id, no_elem_id, yes_elem_id) {
  if (document.querySelector(control_element_id).value === '0') {
    document.querySelector(no_elem_id).checked = true;
  } else {
    document.querySelector(yes_elem_id).checked = true;
  }
}

/*
 * Отмечает checked в элементе (input: checkbox) в зависимости от текущего значения в БД 
 *
 * @param {node} control_element - элемент (input: hidden) с value равным текущему значению
 * @param {number} checkbox - элемент (input: checkbox) для которого определяется есть метка или нет
 */
function setCurrentCheckbox(control_element_id, checkbox_id) {
    if (document.querySelector(control_element_id).value === '1') {
    document.querySelector(checkbox_id).checked = true;
  } 
}


 /*
 * Присваевает значение вспомогательному элементу (input: hidden) 
 * в зависимости от значения checked (true, false) у основного элемента (input: checkbox)
 *
 * @auxiliary_elem {node} - вспомогательный элемент
 * @checkbox {node} - основной элемент
 */

function setAuxiliaryElem(auxiliary_elem_id, checkbox_id) {  
  if (document.querySelector(checkbox_id).checked) {
    document.querySelector(auxiliary_elem_id).value = '1'
  } else {
    document.querySelector(auxiliary_elem_id).value = '0'
    }
}




// --edit_rental_object.html-- 
// выполняется только если на странице есть элемент с id: form_page_rental_object
if (document.querySelector('#form_page_rental_object')) {

  // ADDS OPTIONS TO SELECT
  // object
  addOptions('#bathroom_select', '#db_bathroom_types', '#db_bathroom_type') 
  addOptions('#wash_place_select', '#db_wash_place_types', '#db_wash_place_type') 
  // building
  addOptions('#building_type_select', '#db_building_types', '#db_building_type') 

  // SETS CURRENT VALUE TO RADIO
  // object
  setCurrentRadio('#balcony', '#balconyNo', '#balconyYes')
  setCurrentRadio('#air_conditioner', '#air_conditionerNo', '#air_conditionerYes')
  setCurrentRadio('#wi_fi', '#wi_fiNo', '#wi_fiYes')
  setCurrentRadio('#furniture', '#furnitureNo', '#furnitureYes')
  // building
  setCurrentRadio('#garbage_disposal_db', '#garbage_disposalNo', '#garbage_disposalYes')
  setCurrentRadio('#intercom_db', '#intercomNo', '#intercomYes')
  setCurrentRadio('#concierge_db', '#conciergeNo', '#conciergeYes')
  // appliances
  setCurrentRadio('#db_fridge', '#fridgeNo', '#fridgeYes')
  setCurrentRadio('#db_dishwasher', '#dishwasherNo', '#dishwasherYes')
  setCurrentRadio('#db_washer', '#washerNo', '#washerYes') 
  setCurrentRadio('#db_television', '#televisionNo', '#televisionYes')
  setCurrentRadio('#db_vacuum', '#vacuumNo', '#vacuumYes')
  setCurrentRadio('#db_teapot', '#teapotNo', '#teapotYes')
  setCurrentRadio('#db_iron', '#ironNo', '#ironYes')
  setCurrentRadio('#db_microwave', '#microwaveNo', '#microwaveYes') 


  // SETS CURRENT VALUE TO CHECKBOX
  // object
  setCurrentCheckbox('#db_street_overlook', '#checkbox_street_overlook')
  setCurrentCheckbox('#db_yard_overlook', '#checkbox_yard_overlook')
  setCurrentCheckbox('#db_wood_frame', '#checkbox_wood_frame')
  setCurrentCheckbox('#db_plastic_frame', '#checkbox_plastic_frame')
  setCurrentCheckbox('#db_electric_cooking_range', '#checkbox_electric_cooking_range')
  setCurrentCheckbox('#db_gas_cooking_range', '#checkbox_gas_cooking_range')
  // building
  setCurrentCheckbox('#db_passenger_elevator', '#checkbox_passenger_elevator')
  setCurrentCheckbox('#db_freight_elevator', '#checkbox_freight_elevator')




  // SETS VALUE TO AUXILIARY ELEMENT DEPENDING ON FLAG 'CHECKED' IN CHECKBOX BEFORE SENDING TO THE SERVER
  // object
  let save_object_data_btn = document.querySelector('.save_object_data')
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#street_overlook', '#checkbox_street_overlook') });
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#yard_overlook', '#checkbox_yard_overlook') });
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#wood_frame', '#checkbox_wood_frame') });
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#plastic_frame', '#checkbox_plastic_frame') });
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#electric_cooking_range', '#checkbox_electric_cooking_range') });
  save_object_data_btn.addEventListener("click", () => { setAuxiliaryElem('#gas_cooking_range', '#checkbox_gas_cooking_range') });
  // building
  let save_building_data_btn = document.querySelector('.save_building_data')
  save_building_data_btn.addEventListener("click", () => { setAuxiliaryElem('#passenger_elevator', '#checkbox_passenger_elevator') });
  save_building_data_btn.addEventListener("click", () => { setAuxiliaryElem('#freight_elevator', '#checkbox_freight_elevator') });

}






