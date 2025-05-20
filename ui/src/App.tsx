
import { useEffect, useState } from 'react';
import io from 'socket.io-client';
const socket=io('/ws');
export default function App(){
  const[fps,setFps]=useState(0);
  const[lat,setLat]=useState(0);
  const[mode,setMode]=useState('net');
  useEffect(()=>{
    let count=0;
    socket.on('hud',(d)=>{count++; setLat(d.latency);} );
    const id=setInterval(()=>{setFps(count); count=0;},1000);
    return ()=>{clearInterval(id); socket.off('hud');}
  },[]);
  return <div className="p-4">
    <h1 className="text-xl font-bold">YOLO Aimbot HUD</h1>
    <p>FPS: {fps}</p>
    <p>Latency: {lat} ms</p>
    <button className="m-2 p-2 bg-gray-200 rounded" onClick={()=>setMode(m=>m=='net'?'serial':'net')}>
      Switch to {mode=='net'?'Serial':'NET'}
    </button>
  </div>
}
