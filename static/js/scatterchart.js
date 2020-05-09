
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
  
  Plotly.newPlot(id_element, data, layout);
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
    title: "Split Violin Plot",
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


//old transformation
function data_tansformation_CompAdvantage_lp(data){
  data = data['Competitor_LP_Advantage'];
 
  x = data.map(item => {  
      return item.q_by_Lp_0;
  })

   y = data.map(item => { 
      return item.q_by_Lp_1;
  })

  return  [x ,  y]
}

function data_tansformation_CompAdvantage_sp(data){
  data = data['Competitor_SP_Advantage'];
 
  x = data.map(item => {  
      return item.q_by_Sp_0;
  })

   y = data.map(item => { 
      return item.q_by_Sp_1;
  })

  return  [x ,  y]
}

function data_tansformation_MyCompany_lp(data){
  data = data['MyCompany_LP_Advantage'];
 
  x = data.map(item => {  
      return item.q_by_Lp_0;
  })

   y = data.map(item => { 
      return item.q_by_Lp_1;
  })

  return  [x ,  y]
}

function data_tansformation_MyCompany_sp(data){
  data = data['MyCompany_SP_Advantage'];
 
  x = data.map(item => {  
      return item.q_by_Sp_0;
  })

   y = data.map(item => { 
      return item.q_by_Sp_1;
  })

  return  [x ,  y]
}

//jQuery call functions 
function updateGraphs(){
  $.get( '/advantages', 
  function( data ) { 
    compare_histogram(data,'barChart_1' , dtransf_LP_advantages);
    compare_histogram(data,'barChart_2' , dtransf_SP_advantages);
  }); 

  $.get( '/confronts', 
  function( data ) { 
    $(document).ready(function() {
      for(var i = 0; i <= data.length-1 ; i++) {
       $('#scatter_section').append('<div id="scatter_' + i + '"></ div>' );
      }
      for(var i = 0; i <= data.length-1 ; i++) {
        scatter_avg_category_comparison(data[i], "scatter_" + i, dtransf_confrontation_scatterplot );

       }
     }
     ); 
    });

  $.get( '/sales_analysis', 
  function( data ) {  
    console.log(data);
    violin_history(data);
    });
  }


updateGraphs();
 
 