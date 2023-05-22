import React, { useState, useEffect } from 'react'
import './App.css'
import FileDrop from './components/FileDrop'
function App() {

    return (
      <div className='flex flex-col justify-center align-center'>
        <h1 className='text-2xl'>Upload xml files</h1>
        <FileDrop />
      </div>
    );
  }

export default App;

