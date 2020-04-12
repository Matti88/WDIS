use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use rayon::prelude::*;
 

 
#[pyclass(subclass)]
#[derive(Debug, Clone)]
pub struct ScoreStrings {
    boundle_mc: String,
    boundle_order: String,
    score: f64
}


#[pymethods]
impl ScoreStrings {

     #[getter]
     fn score(&self) -> PyResult<f64> {
        Ok(self.score)
     }

     #[getter]
     fn boundle_mc(&self) -> PyResult<String> {
        Ok(self.boundle_mc.clone())
     }

     #[getter]
     fn boundle_order(&self) -> PyResult<String> {
        Ok(self.boundle_order.clone())
     }
}

 
#[pyfunction]
/// Formats the sum of two numbers as string
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}


#[pyfunction]
fn loop_two_lists(mcboundle: Vec<&str>, order_boundle: Vec<&str>)->Vec<ScoreStrings>{
     
    let mut vec_results : Vec<ScoreStrings> = Vec::new();
    for mc in mcboundle
    {
        for ord in &order_boundle
        {
            let _score =  hamming_score_rust(mc, ord);
            if _score > 0.8
            {
                vec_results.push(
                 ScoreStrings {   boundle_mc: mc.to_string().clone()
                                , boundle_order: ord.to_string().clone()
                                , score: _score
                              }
                            )
            }
        } 
    } 
    vec_results   
}


#[pyfunction]
fn loop_two_lists_rayon(mcboundle: Vec<&str>, order_boundle: Vec<&str>)->Vec<ScoreStrings>{
     
    let parallel_iterator =
        mcboundle
        .par_iter()
        .cloned()
        .flat_map( |mc| 
            {
            order_boundle.par_iter()
                         .map( move  |ord| 
                                ScoreStrings { boundle_mc: mc.to_string().clone()
                                            , boundle_order: ord.to_string().clone()
                                            , score: hamming_score_rust(mc, ord)
                                            }
                            )
            });                                    

    let vec_results: Vec<_> = parallel_iterator.collect();
    vec_results
         
}


/// Formats the sum of two numbers as string
 fn hamming_score_rust(c: &str, d: &str)->f64{

    let a: Vec<&str> = c.split(",").collect();
    let b: Vec<&str> = d.split(",").collect();
 
    let mut vec = Vec::new();
    let mut sum_vector = Vec::new();

    for i in &a{
        for j in &b{
            if *i == *j {
                vec.push(i);
            }        
        }
    }


    vec.sort();
    vec.dedup();
    let _matching = (vec.len())as f64; 

    for j in &b{
            sum_vector.push(j);
        }        
 
    for j in &a{
        sum_vector.push(j);
    }        

    sum_vector.sort();
    sum_vector.dedup();
 
   
    let all_distinct_items = (sum_vector.iter().count()) as f64;
    let common_items = (vec.len()) as f64;

    common_items /all_distinct_items
}

/// This module is a python module implemented in Rust.
#[pymodule]
fn string_sum(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(sum_as_string))?;
    m.add_class::<ScoreStrings>()?;
    m.add_wrapped(wrap_pyfunction!(loop_two_lists))?;
    m.add_wrapped(wrap_pyfunction!(loop_two_lists_rayon))?;
 
    Ok(())

    
}
 