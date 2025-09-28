import { useState } from 'react'
import './assets/css/style.css'
import Main from './components/Main'
import File from './components/FIle'
import Footer from './components/Footer'
import Header from './components/Header'


function App() {


  return (
    <>
    <div className='app'>
      <Footer />
      <Main/>
      <File/>
      <Header/>


    </div>

    </>
  )
}

export default App;
