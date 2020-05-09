
// Plotting Functions
function simpleScatterplot(data_from_query, id_element, tranforming_function){
  
  var transformed_data = tranforming_function(data_from_query);
  var x_ = transformed_data[0]
  var y_ = transformed_data[1];

  var element_object = document.getElementById(id_element),
      hoverInfo = document.getElementById('hoverinfo'),
   
    data_ = [{
            x:x_
          , y:y_
          , type:'scatter'
          , name:'Trial 1'
          , mode:'markers'
          , marker:{size:20}}
        ],
    layout = {hovermode:'closest',  title:'Scatter List Price<br>VS Street Price'};

    Plotly.newPlot(id_element, data_, layout);
 
    element_object.on('plotly_hover', function(data_){
          var xaxis = data_.points[0].xaxis,  yaxis =  data_.points[1].yaxis;
          var infotext = data_.points.map(function(d){
              return ('width: '+xaxis.l2p(d.x)+', height: '+yaxis.l2p(d.y)); 
                                            });

          hoverInfo.innerHTML = infotext.join('<br/>');
    })
    .on('plotly_unhover', function(data_){
        hoverInfo.innerHTML = '';
    });

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
  
  var layout = {barmode: 'group'};
  
  Plotly.newPlot(id_element, data, layout);
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


function data_tansformation_CompAdvantage_lp(data){
  data = data['Competitor_LP_Advantage'];
 
  x = data.map(item => {  
      return item.q_by_Lp_0;
  })

   y = data.map(item => { 
      return item.q_by_Lp_1;
  })
  console.log(x, y);
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
    simpleScatterplot(data, 'scatter_1', data_tansformation_CompAdvantage_lp);
    // simpleScatterplot(data, 'scatter_2', data_tansformation_CompAdvantage_sp);
    // simpleScatterplot(data, 'scatter_3', data_tansformation_MyCompany_lp);
    // simpleScatterplot(data, 'scatter_4', data_tansformation_MyCompany_sp);
  }); 
}

updateGraphs();
 
 


 