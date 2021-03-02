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

function parser(cadena){
  return cadena.split("|");
}

for(let image_container of images_containers){
  image_container.addEventListener('click', () => {
    var item_data = parser(image_container.id);
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

    var item_obverse_image_path_image_tag;
    var item_reverse_image_path_image_tag;

    if(item_product_type == "Moneda"){
      item_obverse_image_path_image_tag = document.createElement('img');
      item_obverse_image_path_image_tag.classList.add("obverse_side_coin_img_preview");
      // item_obverse_image_path_image_tag.src = item_obverse_image_path; // <-----------------------------
      item_obverse_image_path_image_tag.src = "https://coin-brothers.com/photos/United_States_of_America_(USA)_Cents_10/1965-2016_24.02.2016_15.19.jpg"; // ----------------------------->
  
      item_reverse_image_path_image_tag = document.createElement('img');
      item_reverse_image_path_image_tag.classList.add("reverse_side_coin_img_preview");
      // item_reverse_image_path_image_tag.src = item_reverse_image_path; // <-----------------------------
      item_reverse_image_path_image_tag.src = "https://s3.amazonaws.com/ngccoin-production/world-coin-price-guide/82716b.jpg"; // ----------------------------->
    }
    else{
      item_obverse_image_path_image_tag = document.createElement('img');
      item_obverse_image_path_image_tag.classList.add("obverse_side_bill_img_preview");
      // item_obverse_image_path_image_tag.src = item_obverse_image_path; // <-----------------------------
      item_obverse_image_path_image_tag.src = "https://upload.wikimedia.org/wikipedia/commons/2/23/US_one_dollar_bill%2C_obverse%2C_series_2009.jpg"; // ----------------------------->
  
      item_reverse_image_path_image_tag = document.createElement('img');
      item_reverse_image_path_image_tag.classList.add("reverse_side_bill_img_preview");
      // item_reverse_image_path_image_tag.src = item_reverse_image_path; // <-----------------------------
      item_reverse_image_path_image_tag.src = "https://www.uscurrency.gov/sites/default/files/styles/bill_version/public/denominations/1_1963-present-back.jpg?itok=-_dI8Duo"; // ----------------------------->
    }

    const images_preview_container = createCustomElement('div', {class: 'images_preview_container'}, [item_obverse_image_path_image_tag, item_reverse_image_path_image_tag])


    var h1_tag = "<h3><b>Características:</b></h3>"
    var list_tag = "<ul><li>Tipo: " + item_product_type + "</li><li>País: " + item_country +  "</li><li>Denominación: " + item_denomination + "</li><li>Año: " + item_year + "</li><li>Composición: " + item_composition + "</li></ul>"
    var h1_tag_description = "<h4><b>Descripción:</b></h4>";
    var description_text_div = "<div style='margin-left:7%; white-space: pre-line;'>" + item_description + "</div>"
    const details_preview = createCustomElement('div', {class: 'details_preview_container'}, [h1_tag, list_tag, h1_tag_description, description_text_div]);


    const item_details_div_tag = createCustomElement('div', {class: 'item_details'}, [images_preview_container, details_preview]);
    printModal(item_details_div_tag);
  });
}