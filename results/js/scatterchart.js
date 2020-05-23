
var file_in_MyCompany_uploaded = false;
var file_in_Competitor_uploaded = false;

function checkTheFile(side){
  if(side == 'MyCompany'){
    console.log('My Company checking side');
    $.ajax({
      url: '/checker/Checker_OCpR_file' ,
      headers : { 'Side':file_in_MyCompany_uploaded},
      success: function(data){
        console.log(data);
      }
     }
    )

  }
  else{
    console.log('Competitor checking side');
    $.ajax({
      url: '/checker/Checker_OCpR_file' ,
      headers : { 'Side':file_in_Competitor_uploaded},
      success: function(data){
        console.log(data);
      }
     }
    )

  }

}


Dropzone.autoDiscover = false;
var myDropzone1 = new Dropzone("form#my-awesome-dropzone1", { 
    url: '/checker/upload-OCpR_file',
    headers: {
      'side': 'MyCompany'
    },
    maxFiles:1,
    init: function() {
      this.on('success', function(file) {
        file_in_MyCompany_uploaded = file.upload.filename;
      }), 
      this.on("maxfilesexceeded", function(file) {
            this.removeAllFiles();
            this.addFile(file);
      }); } 
    }) 
  
var myDropzone2 = new Dropzone("form#my-awesome-dropzone2", { 
    url: '/checker/upload-OCpR_file',
    headers: {
      'side': 'Competitor'
    },
    maxFiles:1,

    init: function() {
      this.on('success', function(file) {
        file_in_Competitor_uploaded = file.upload.filename;
      }), 
      this.on("maxfilesexceeded", function(file) {
            this.removeAllFiles();
            this.addFile(file);
      }); } }) 
    




//elements for the Analaysis Report
const top_elements_analysis_ = 
`<div class="row" id="basic_analysis">
<div class="col-xl-4 col-lg-4">
  <div class="card shadow mb-4">
    <!-- Card Header - Dropdown -->
    <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
      <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
    </div>
    <!-- Card Body -->
    <div class="card-body">
      <div id="violin_" class="chart-area"></div>
    </div>
  </div>
</div>

<div class="col-xl-4 col-lg-4">
  <div class="card shadow mb-4">
    <!-- Card Header - Dropdown -->
    <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
      <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
    </div>
    <!-- Card Body -->
    <div class="card-body">
      <div id="barChart_2" class="chart-area"></div>
    </div>
  </div>
</div>

<div class="col-xl-4 col-lg-4">
  <div class="card shadow mb-4">
    <!-- Card Header - Dropdown -->
    <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
      <h6 class="m-0 font-weight-bold text-primary">Earnings Overview</h6>
    </div>
    <!-- Card Body -->
    <div class="card-body">
      <div id="barChart_1" class="chart-area"></div>
    </div>
  </div>
</div>
</div>
<!-- Content Row : scatter plots -->
<div class="row" id="scatter_section"></div>`


// Plotting Functions
function scatter_avg_category_comparison(data_from_query, id_element, tranforming_function){
  
  var transformed_data = tranforming_function(data_from_query);
  var x_1 = transformed_data[0]
  var y_1 = transformed_data[1];
  var label_1 = transformed_data[2]
  var x_2 = transformed_data[3];
  var y_2 = transformed_data[4]
  var label_2 = transformed_data[5];
  var Title_ = transformed_data[6];
  var avg_lp_1_ = transformed_data[7];
  var avg_sp_1_ = transformed_data[8];
  var avg_lp_2_ = transformed_data[9];
  var avg_sp_2_ = transformed_data[10];


  var trace1 = {
    x: x_1,
    y: y_1,
    mode: 'markers+text',
    type: 'scatter',
    name: 'My Company',
    text: label_1,
    textposition: 'top center',
    textfont: {
      family:  'Raleway, sans-serif'
    },
    marker: { size: 12 }
  };
  var trace2 = {
    x: x_2,
    y: y_2,
    mode: 'markers+text',
    type: 'scatter',
    name: 'Competitor',
    text: label_2,
    textfont : {
      family:'Times New Roman'
    },
    textposition: 'bottom center',
    marker: { size: 12 }
  };
  var avg_lp_1 = {
    x: avg_lp_1_,
    y: y_1,
    name: 'avg_lp_MyC',
    mode: 'lines',
    type: 'scatter'
  };
  var avg_sp_1 = {
    x: x_1,
    y: avg_sp_1_,
    name: 'avg_sp_MyC',
    mode: 'lines',
    type: 'scatter'
  };
  var avg_lp_2 = {
    x: avg_lp_2_,
    y: y_2,
    name: 'avg_lp_Com',
    mode: 'lines',
    type: 'scatter'
  };
  var avg_sp_s = {
    x: x_2,
    y: avg_sp_2_,
    name: 'avg_sp_Com',
    mode: 'lines',
    type: 'scatter'
  };

  var data = [ trace1, trace2, avg_lp_1, avg_sp_1,  avg_lp_2, avg_sp_2, avg_sp_s ];
  

  var layout = {

    legend: {
      y: 0.5,
      yref: 'paper',
      font: {
        family: 'Arial, sans-serif',
        size: 20,
        color: 'grey',
      }
    },
    title: Title_
  };
  
  Plotly.newPlot(id_element, data, layout);

  }     

function compare_histogram(data_from_query, id_element, tranforming_function){

  const hist_data = tranforming_function(data_from_query);
  var x_ = hist_data[0];  
  var y1 = hist_data[1];
  var y2 = hist_data[2];

  var trace1 = {
    x: x_,
    y: y1,
    name: 'MyCompany',
    type: 'bar'
  };
  
  var trace2 = {
    x: x_,
    y: y2,
    name: 'Competitor',
    type: 'bar'
  };
  
  var data = [trace1, trace2];

  var all_values = y1.concat(y2); 
  all_values = all_values.filter(function( element ) {  return element !== undefined; });
 
var min = Math.min( ...all_values ),
    max = Math.max( ...all_values );
 
  var layout = {
    yaxis: {
      range: [min*0.99, max*1.01 ],
      title: 'Average prices per Category'
    }, 
    barmode: 'group'};
  
  Plotly.newPlot(id_element, data, layout );
}
  
function violin_history(data_){
  
  function unpack(rows, key, side_criteria) {
 
      function side_chek (row) { return side_criteria == row['Competitive_Flag']; }

      rows = rows.filter(side_chek);

      return rows.map(function(row) { return row[key]; });
  }
  


  var data = [{
    type: 'violin',
    x: unpack(data_, 'Month', 'Advantage' ),
    y: unpack(data_, 'unit_Price_QTY', 'Advantage'),
    legendgroup: 'Advantages',
    scalegroup: 'Advantages',
    name: 'Advantages',
    side: 'negative',
    box: {
      visible: false
    },
    line: {
      color: 'blue',
      width: 2
    },
    meanline: {
      visible: true
    }
  }, {
    type: 'violin',
  x: unpack(data_, 'Month', 'Disadvantage'),
  y: unpack(data_, 'unit_Price_QTY', 'Disadvantage'),
    legendgroup: 'Disadvantages',
    scalegroup: 'NDisadvantageso',
    name: 'Disadvantages',
    side: 'positive',
    box: {
      visible: false
    },
    line: {
      color: 'green',
      width: 2
    },
    meanline: {
      visible: true
    }
  }]
  
  var layout = {
    title: "Dist Competitive Offer VS Non-Competitive by Month",
    yaxis: {
      zeroline: false
    },
    violingap: 0,
    violingroupgap: 0,
    violinmode: "overlay",
  }

Plotly.newPlot('violin_', data, layout);

}

// transformation functions 
function dtransf_LP_advantages(data){
  data = data['Competitor_LP_Advantage'].concat(data['MyCompany_LP_Advantage']);

  var ks_ = Object.keys(data[0]);
  var PATTERN = '_tag'
  var tags_fields = ks_.filter(function (str) { return !(str.indexOf(PATTERN) === -1); });
  var non_tags_fields = ks_.filter(function (str) { return !(str.indexOf(PATTERN) === -1); });
  var non_tags_fields = ['q_by_Lp_0','q_by_Lp_1'];
 
  x = data.map(item => { 

      category_strings = tags_fields.map( cat_ => {return item[cat_]} );
      return category_strings.join("_");
  })

  y1 = data.map(item => { 
    return item[non_tags_fields[0]];
  })

  y2 = data.map(item => { 
  return item[non_tags_fields[1]];
  })

  return [x, y1, y2]
}

function dtransf_SP_advantages(data){
  data = data['Competitor_SP_Advantage'].concat(data['MyCompany_SP_Advantage']);

  var ks_ = Object.keys(data[0]);
  var PATTERN = '_tag'
  var tags_fields = ks_.filter(function (str) { return !(str.indexOf(PATTERN) === -1); });
  var non_tags_fields = ks_.filter(function (str) { return !(str.indexOf(PATTERN) === -1); });
  var non_tags_fields = ['q_by_Sp_0','q_by_Sp_1'];
 
  x = data.map(item => { 

      category_strings = tags_fields.map( cat_ => {return item[cat_]} );
      return category_strings.join("_");
  })

  y1 = data.map(item => { 
    return item[non_tags_fields[0]];
  })

  y2 = data.map(item => { 
  return item[non_tags_fields[1]];
  })

  return [x, y1, y2]
}

function dtransf_confrontation_scatterplot(data){
 
  var ks_ = Object.keys(data);
  var Title_ = ks_[0]
  data = data[Title_]

  //MyCompany section
  x_1 = data.map(item => {
    if (item['Vendor'] == 'MyCompany') {
      return item['q_by_Lp'];
    }
  })

  y_1 = data.map(item => {
    if (item['Vendor'] == 'MyCompany') {
      return item['q_by_Sp'];
    }
  })

  label_1 = data.map(item => {
    if (item['Vendor'] == 'MyCompany') {
      return item['code'];
    }
  })

  avg_lp_1 = data.map(item => {
    if (item['Vendor'] == 'MyCompany') {
      return item['q_by_Lp_0'];
    }
  })	

  avg_sp_1 = data.map(item => {
    if (item['Vendor'] == 'MyCompany') {
      return item['q_by_Sp_0'];
    }
  })	


  //competitor section
  x_2 = data.map(item => {
    if (item['Vendor'] == 'Competitor') {
      return item['q_by_Lp'];
    }
  })
 
  y_2 = data.map(item => {
    if (item['Vendor'] == 'Competitor') {
      return item['q_by_Sp'];
    }
  })

  label_2 = data.map(item => {
    if (item['Vendor'] == 'Competitor') {
      return item['code'];
    }
  })

  avg_lp_2 = data.map(item => {
    if (item['Vendor'] == 'Competitor') {
      return item['q_by_Lp_1'];
    }
  })	

  avg_sp_2 = data.map(item => {
    if (item['Vendor'] == 'Competitor') {
      return item['q_by_Sp_1'];
    }
  })	

  return [x_1, y_1, label_1,  x_2, y_2 , label_2, Title_, avg_lp_1, avg_sp_1, avg_lp_2, avg_sp_2]
}


//jQuery call functions 
function updateGraphs(){

  $('#Analysis_Area').append(top_elements_analysis_ );
  $(".loading").fadeIn("slow");
  
  
  top_elements_analysis_

  $.get( '/checker/sales_analysis', 
  function( data ) {   
    violin_history(data);
    });

chart_part_1 = 
`<div class="col-xl-6 col-lg-6">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary"> _code_for_title_ </h6>
      </div>
    <div class="card-body">
  <div id="scatter_`
        
chart_part_2 = `" class="chart-area"></div></div></div></div>`
   
  $.ajax({
    url: '/checker/advantages',
    type: 'GET',
    headers: { Authorization: $`Bearer ${localStorage.getItem("token")}` },
    data: {},
    success:  function( data ) { 
      compare_histogram(data,'barChart_1' , dtransf_LP_advantages);
      compare_histogram(data,'barChart_2' , dtransf_SP_advantages);
    },
    error: function (data) { console.log('did not have access') },
    });
 



  $.get( '/checker/confronts', 
  function( data ) { 
    $(document).ready(function() {
      for(var i = 0; i <= data.length-1 ; i++) {
        var new_card_with_graph = chart_part_1 + i + chart_part_2;
        var title_of_card_with_plot = Object.keys(data[i])[0];
        new_card_with_graph = new_card_with_graph.replace('_code_for_title_', title_of_card_with_plot  );
       $('#scatter_section').append(new_card_with_graph , data[i]);
      }
      for(var i = 0; i <= data.length-1 ; i++) {
        scatter_avg_category_comparison(data[i], "scatter_" + i, dtransf_confrontation_scatterplot );
 
        $(".loading").fadeOut("slow"); 
      
      }
     }
     ); 
    });




  
  }


 