const fileInput = document.getElementById('file-input');
const fileContent = document.getElementById('file-content');
const fileUploadLabel = document.querySelector('.file-upload-label');

fileInput.addEventListener('change', handleFile);

function handleFile(event) {
  const file = event.target.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function (e) {
      const data = new Uint8Array(e.target.result);
      const workbook = XLSX.read(data, { type: 'array' });

      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      const htmlTable = formatDataToTable(jsonData);

      fileContent.innerHTML = htmlTable;
      fileContent.style.display = 'block';
      fileInput.style.display = 'none';
      fileUploadLabel.style.display = 'none';

      const tableCells = document.querySelectorAll('td');
      tableCells.forEach((cell) => {
        cell.addEventListener('click', (event) => {
          openModal(event, jsonData);
        });
      });
    };

    reader.readAsArrayBuffer(file);
  }
}

function formatDataToTable(data) {
  const headers = data[0];
  const numRows = Math.ceil(headers.length / 7);

  let tableHtml = '<table>';
  let dataIndex = 0;
  for (let i = 0; i < numRows; i++) {
    tableHtml += '<tr>';

    for (let j = 0; j < 7; j++) {
      if (dataIndex < data[0].length) {
        tableHtml += '<td>' + (dataIndex + 1) + '</td>';
        dataIndex++;
      } else {
        tableHtml += '<td></td>';
      }
    }

    tableHtml += '</tr>';
  }

  tableHtml += '</table>';

  return tableHtml;
}
function getValues(arr) {
  const aux = arr.split(' ');
  const x = aux[0].replace('[', '');
  const y = aux[1];
  const z = aux[2].replace(']', '');
  const array = [];
  if (x == 1) {
    array.push('Mañana');
  }
  if (y == 1) {
    array.push('Tarde');
  }
  if (z == 1) {
    array.push('Noche');
  }
  return array.length > 0 ? array : 'Sin asignación';
}
function openModal(event, jsonData) {
  const [_, person1, person2, person3, person4, person5] = jsonData;
  const modal = document.getElementById('modal');
  const modalContent = document.getElementById('modal-content');

  const text =
    'Dia: ' +
    event.target.innerHTML +
    '<br>' +
    '<br>' +
    'Persona 1: ' +
    getValues(person1[event.target.innerHTML - 1]) +
    '<br>' +
    '<br>' +
    'Persona 2: ' +
    getValues(person2[event.target.innerHTML - 1]) +
    '<br>' +
    '<br>' +
    'Persona 3: ' +
    getValues(person3[event.target.innerHTML - 1]) +
    '<br>' +
    '<br>' +
    'Persona 4: ' +
    getValues(person4[event.target.innerHTML - 1]) +
    '<br>' +
    '<br>' +
    'Persona 5: ' +
    getValues(person5[event.target.innerHTML - 1]) +
    '<br>' +
    '<br>';

  modalContent.innerHTML = text;

  modal.style.display = 'flex';

  const closeButton = document.querySelector('.close');
  closeButton.addEventListener('click', closeModal);
}

function closeModal() {
  const modal = document.getElementById('modal');

  modal.style.display = 'none';

  const closeButton = document.querySelector('.close');
  closeButton.removeEventListener('click', closeModal);
}
