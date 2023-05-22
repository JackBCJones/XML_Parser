import React, { useState, useEffect } from 'react'
import './App.css'
import FileDrop from './components/FileDrop'

function App() {

  // const [data, setData] = useState([{}])

  // useEffect(() => {
  //   const fetchData = async () => {
  //     try {
  //       const response = await fetch('http://127.0.0.1:5000/hello');
  //       if (!response.ok) {
  //         throw new Error('Request failed');
  //       }
  //       const jsonData = await response.json();
  //       setData(jsonData);
  //       console.log(jsonData);
  //     } catch (error) {
  //       console.log(error)
  //     }
  //   };
  //   fetchData();
  // }, []);
  

    return (
      <div>
        <FileDrop />
      </div>
    );
  }

export default App;

