import { useState, useEffect } from 'react'
import './App.css'
import axios from "axios";
import Header from './components/Header'
import DevicesTable from './components/DevicesTable'
import Chart from './components/Charts';
import { ResponsiveContainer } from 'recharts';
import Graph from './components/GraphPage';

function App() {

  return (
    <div>
      <Header />  

     
      <main>
        <DevicesTable />
      </main>
    </div>
       
  )
}

export default App
