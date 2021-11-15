// Accordion
function myFunction(id) {
  var x = document.getElementById(id);
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
    x.previousElementSibling.className += " w3-theme-d1";
  } else { 
    x.className = x.className.replace("w3-show", "");
    x.previousElementSibling.className = 
    x.previousElementSibling.className.replace(" w3-theme-d1", "");
  }
}

// Used to toggle the menu on smaller screens when clicking on the menu button
function openNav() {
  var x = document.getElementById("navDemo");
  if (x.className.indexOf("w3-show") == -1) {
    x.className += " w3-show";
  } else { 
    x.className = x.className.replace(" w3-show", "");
  }
}

const createCustomElement = (element, attributes, children) => {
  let customElement = document.createElement(element);
  if(children !== undefined) children.forEach(e => {
      if(e.nodeType){
          if(e.nodeType == 1 || e.nodeType == 11) customElement.appendChild(e);
      }
      else{
          customElement.innerHTML += e;
      }
  });
  addAttributes(customElement, attributes);
  return customElement;
};

const addAttributes = (element, attrObj) => {
  for(let attr in attrObj){
      if(attrObj.hasOwnProperty(attr)) element.setAttribute(attr, attrObj[attr]);
  }
};

const printModal = content => {
  const modalContentElement = createCustomElement('div', {
      id: 'ed-modal-content',
      class: 'ed-modal-content w3-container w3-card w3-round w3-white'
  }, [content]);
  const modalContainerElement = createCustomElement('div', {
      id: 'ed-modal-container',
      class: 'ed-modal-container'
  }, [modalContentElement]);
  // document.getElementsByClassName("publications-list")[0].appendChild(modalContainerElement);
  document.body.appendChild(modalContainerElement);
  document.querySelector('.ed-modal-container').style.top = window.scrollY +'px';
  document.querySelector('html').style.overflow = "hidden";
  const removeModal = () => document.body.removeChild(modalContainerElement);
  modalContainerElement.addEventListener('click', e => {
      if(e.target == modalContainerElement){
        removeModal();
        document.querySelector('html').style.overflow = "visible";
      }
  });
};

var images_containers = document.getElementsByClassName("images_container");
console.log(images_containers);

function parser(cadena, c){
  return cadena.split(c);
}

for(let image_container of images_containers){
  image_container.addEventListener('click', () => {
    var item_data = parser(image_container.id, "|");
    let item_id =  item_data[0];
    let item_product_type = item_data[1];
    let item_country = item_data[2];
    let item_denomination = item_data[3];
    let item_year = item_data[4];
    let item_composition = item_data[5];
    let item_description = item_data[6];
    let item_obverse_image_path = item_data[7];
    let item_reverse_image_path = item_data[8];
    let item_owner_name = item_data[9];
    let item_owner_profile_picture_path = item_data[10];
    let user_email = item_data[11];
    let item_num_views = item_data[12];

    var item_obverse_image_path_image_tag;
    var item_reverse_image_path_image_tag;
    var images_preview_container;

    if(item_product_type == "Moneda"){
      item_obverse_image_path_image_tag = document.createElement('img');
      item_obverse_image_path_image_tag.classList.add("obverse_side_coin_img_preview");
      item_obverse_image_path_image_tag.src = item_obverse_image_path; // <-----------------------------
      // item_obverse_image_path_image_tag.src = "https://coin-brothers.com/photos/United_States_of_America_(USA)_Cents_10/1965-2016_24.02.2016_15.19.jpg"; // ----------------------------->
  
      item_reverse_image_path_image_tag = document.createElement('img');
      item_reverse_image_path_image_tag.classList.add("reverse_side_coin_img_preview");
      item_reverse_image_path_image_tag.src = item_reverse_image_path; // <-----------------------------
      // item_reverse_image_path_image_tag.src = "https://s3.amazonaws.com/ngccoin-production/world-coin-price-guide/82716b.jpg"; // ----------------------------->

      images_preview_container = createCustomElement('div', {class: 'images_preview_container_coin'}, [item_obverse_image_path_image_tag, item_reverse_image_path_image_tag])
    }
    else{
      item_obverse_image_path_image_tag = document.createElement('img');
      item_obverse_image_path_image_tag.classList.add("obverse_side_bill_img_preview");
      item_obverse_image_path_image_tag.src = item_obverse_image_path; // <-----------------------------
      // item_obverse_image_path_image_tag.src = "https://upload.wikimedia.org/wikipedia/commons/2/23/US_one_dollar_bill%2C_obverse%2C_series_2009.jpg"; // ----------------------------->
  
      item_reverse_image_path_image_tag = document.createElement('img');
      item_reverse_image_path_image_tag.classList.add("reverse_side_bill_img_preview");
      item_reverse_image_path_image_tag.src = item_reverse_image_path; // <-----------------------------
      // item_reverse_image_path_image_tag.src = "https://www.uscurrency.gov/sites/default/files/styles/bill_version/public/denominations/1_1963-present-back.jpg?itok=-_dI8Duo"; // ----------------------------->

      images_preview_container = createCustomElement('div', {class: 'images_preview_container_bill'}, [item_obverse_image_path_image_tag, item_reverse_image_path_image_tag])
    }

    var h1_tag = "<h4><b>Características:</b></h4>"
    var list_tag = "<ul><li>Tipo: " + item_product_type + "</li><li>País: " + item_country +  "</li><li>Denominación: " + item_denomination + "</li><li>Año: " + item_year + "</li><li>Composición: " + item_composition + "</li><li>Número de visitas: " + item_num_views + "</li></ul>"
    var list_div = createCustomElement('div', {class: 'list_div'}, [h1_tag, list_tag])
    var h1_tag_description = "<h4><b>Descripción:</b></h4>";
    var description_text_div = "<div style='margin-left:7%; white-space: pre-line;'>" + item_description + "</div>"
    var description_div = createCustomElement('div', {class: 'description_div'}, [h1_tag_description, description_text_div])
    const details_preview = createCustomElement('div', {class: 'details_preview_container'}, [list_div, description_div]);

    var comments;
    fetch(`/get_comments/${item_id}`)
    .then(function (response) {
        item_num_views = item_num_views + 1
        return response.text();
    }).then(function (text) {
      console.log(text)
      comments = parser(text, "|");
      var i = 0;
      while(i < comments.length){
        comments[i] = parser(comments[i], '*');
        i++;
      }
      console.log(comments)
      var html_comments = ''
      i = 0;
      while(i < comments.length && comments[0] != ""){
        html_comments += `
        <div class="user_comment">
          <img src="${comments[i][1]}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:30px">
          <h4>${comments[i][0]}</h4>
          <p class="user_text_comment">${comments[i][2]}</p>
        </div>
        `
        i++;
      }
      const comments_container_div = `
      <div class="comments_container">
        <h3>Comentarios</h3>
        <hr>
        <div class="user_comments">
          ${html_comments}
        </div>
        <form method="POST">
          <div class="user_input_comment">
            <textarea class="input_text_comment" name="input_text_comment|${item_id}|${user_email}" placeholder="Deja aquí tu comentario..."></textarea>
            <input type="submit" class="w3-button w3-theme-d1 w3-margin-left" value="Comentar">
          </div>
        <form>
      </div>
    `
    
    const exchange_item_div = `
      <div class="message_container">
        <h3>Deja un mensaje al propietario</h3>
        <hr style="width: 70%">
        <img src="${item_owner_profile_picture_path}" alt="Avatar" class="w3-left w3-circle w3-margin-right" style="width:40px">
        <div class="message_form">
          <textarea class="message" name="message" placeholder=""></textarea>
          <input type="submit" class="w3-button w3-theme-d1 w3-margin-left" value="Enviar">
        <div>
      </div>
    `

    var item_details_div_tag;
    if(item_product_type == "Moneda"){
      item_details_div_tag = createCustomElement('div', {class: 'item_details_coin'}, [images_preview_container, details_preview]);
    }
    else{
      item_details_div_tag = createCustomElement('div', {class: 'item_details_bill'}, [images_preview_container, details_preview]);
    }
    const main_details_div_tag = createCustomElement('div', {class: 'main_details_div_tag'}, [item_details_div_tag, comments_container_div])
    printModal(main_details_div_tag);
    });
  });
}

function onlyNumberKey(evt) {
          
  // Only ASCII character in that range allowed
  var ASCIICode = (evt.which) ? evt.which : evt.keyCode
  if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57))
      return false;
  return true;
}