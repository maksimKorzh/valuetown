$(document).ready(function() {
  // Load datatable
  properties = initTable();
  
  // Init city selector
  var cityTags = $('#city-selector').tagator({
    autocomplete: ['London', 'Birnimgham', 'Slough']
  });
  
  // City selector on change event handler
  cityTags.on('change', function() {
    //properties.ajax.reload();
  });
  
  // On city change
  $('#city').on('change', function() {
    properties.ajax.reload();
  });
  
  // On distance change
  $('#distance').on('change', function() {
    properties.ajax.reload();
  });
  
  // On distance change
  $('#property').on('change', function() {
    properties.ajax.reload();
  });
  
  // On distance change
  $('#bedrooms').on('change', function() {
    properties.ajax.reload();
  });
});

function initTable() {
  return $('#properties').DataTable({
    // Make HTTP GET requests with parameters to API
    "ajax": {
        "url": "/api/active",
        "data": function(args) {
          // Extract form data
          args['city'] = $('#city option:selected').text();
          args['distance'] = $('#distance option:selected').text();
          args['property'] = $('#property option:selected').text();
          args['bedrooms'] = $('#bedrooms option:selected').text();
        }
     },
    
    "columns": [
      {"data": "title"},
      {"data": "address"},
      {"data": "price"},
      {"data": "date"},
      {"data": "seller"},
      {"data": "description"},
      {"data": "image"},
      {"data": ''}
    ],
    
    columnDefs: [
      {
          render: function (data, type, full, meta) {
            return "<div class='text-wrap'>" + data + "</div>";
          },
          targets: 5
      },
      {
          render: function (data, type, full, meta) {
            return '<button type="button" data="' + data + '" onclick="showImage(this)" class="btn btn-primary" data-toggle="modal" data-target="#modalImage">View image...</button>';
          },
          targets: 6
      },
      {
          render: function (data, type, full, meta) {
            return '<button type="button" onclick="salesHistory(this)" class="btn btn-secondary" data-toggle="modal" data-target="#modalHistory">Sale history...</button>';
          },
          targets: 7
      }
    ]
    
  });
}

function salesHistory(button) {
  $('#modal-body').empty().text('Loading results...')
  
  var features = $($(button).closest('tr').prev().find('td')[1]);
  var query = $(features).text();
  var city = $('#city option:selected').text();

  $.get('/api/sold?q=' + query + '&city=' + city, function (data) {    
    $('#modal-body').text('')
    
    if (data.data.length == 0)
      $('#modal-body').text('No results found')
      
    for (var index = 0; index < data.data.length; index++) {
      var table = `
        <table class="display table mt-4">
          <thead>
            <tr>
              <th>Price</th>
              <th>Type</th>
              <th>Date</th>
              <th>Bedrooms</th>
            </tr>
          </thead>
          <tbody>
      `
      
      data.data[index].history.forEach((item) => {
        table += `        
          <tr>
            <td>${item.price}</td>
            <td>${item.type}</td>
            <td>${item.date}</td>
            <td>${item.bedrooms}</td>
          <tr>
        `
      })
      
      table += "</tbody></table>"

      $('#modal-body').append(
        '<div class="col">' +
          '<strong>' + data.data[index].address + '</strong>' + table +
          
        '<div>');
    }
  });
  
}

function showImage(button) {
  $('#image-title').empty()
  $('#image-body').empty()
  
  var features = $($(button).closest('tr').prev().find('td')[1]);
  var title = $(features).text()
  var image = $(button).attr('data')      

  $('#image-title').append('<strong>' + title + '</strong>')
  $('#image-body').append('<img src="'+ image + '">')
}













